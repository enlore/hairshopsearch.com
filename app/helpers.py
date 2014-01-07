from flask import current_app, g
import requests
import simplejson as json
from pyelasticsearch.client import _iso_datetime
from six import PY3

from PIL import Image

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import os

def info(msg):
    current_app.logger.info(msg)

def _get_bucket():
    # return bucket from app.g or make a new one
    if not g.get('bucket', False):
        g.bucket = S3Connection(
                current_app.config['AWS_KEY'],
                current_app.config['AWS_SECRET']
            )._get_bucket( current_app.config['BUCKET_NAME'])
    return g.bucket 


def put_s3(file_name):
    k = Key(_get_bucket())
    k.key = 'uploads/{}'.format(file_name)
    bytes_up = k.set_contents_from_file(open(os.path.join(
        current_app.config['UPLOAD_DIR'],
        file_name
        )))
    k.set_acl('public-read')
    info('~~~| Put {} bytes at key {}'.format(bytes_up, k.key))
    return k.key

def generate_thumbs(filename, sizes):
    """Read a file from disk, size it down to thumbnail size and
    save it in the uploads dir

    :param filename: name of the file
    :param sizes: sizes we intend to make thumbnails of
    :type sizes: tuple or list of tuples, width by height
    :rtype thumbs: list of locally saved filenames of thumbs
    """
    thumbs = []

    if not type(sizes) == list:
        sizes = [sizes]

    path = os.path.join(current_app.config['UPLOAD_DIR'], filename)
    for size in sizes:
        image = Image.open(path)
        image.thumbnail(size)
        save_name = '{}x{}_{}'.format(size[0], size[1], filename)
        save_path = os.path.join( current_app.config['UPLOAD_DIR'], save_name)
        image.save(save_path)
        thumbs.append(save_name)
    return thumbs

def ellipsize(string, limit=50):
    """Jinja template filter
    Ellipsize that text! Craps out up to limit characters
    """
    return '{}{}'.format(string[0: limit], '...')

def acceptable_url_string(string, proto_string):
    """Clean a string of all it's unnacceptable chars.

    :param string: business name to be cleaned
    :param proto_string: acceptable charset
    """

    res = []
    test_string = string.strip().lower()
    for ch in (char for char in test_string):
        # replace as single whitespace with a single period
        if ch == ' ':
            ch = '.'
        if ch in proto_string:
            res.append(ch)

    res_string = u''.join(res)

    if res_string[-1] == '.':
        return res_string[0:-1]

    return res_string

def lat_lon(address, sensor='false'):
    """Access the Google Geocoding API to return lat and lon given an address.

    :param address: instance of :class:Address
    :param sensor: 'false' or 'true': tells google api if loc data is
        generated from a device sensor
    :type sensor: string
    :rtype: array of tuples of the format (lat, lon)
    """

    params = {}
    # address builder: take address object, for each attr if not none,
    # insert into address string
    address_string = ' '.join([
                address.street_1 or '',
                address.street_2 or '',
                address.city or '',
                address.state or '',
                str(address.zip_code or ''),
                ])

    params['address'] = address_string.strip()

    params['sensor'] = sensor

    geo_uri = 'http://maps.googleapis.com/maps/api/geocode/json'
    resp = requests.get(geo_uri, params=params)

    decoded_resp = resp.json()

    if decoded_resp['status'] == 'OK':
        locs = []
        for res in decoded_resp['results']:
            locs.append(
                    (res['geometry']['location']['lat'],
                     res['geometry']['location']['lng'])
                )
        return locs

    elif decoded_resp['status'] == 'REQUEST_DENIED':
        if decoded_resp['error_message']:
            raise HSSError("GEOLOC req denied: %s" % decoded_resp['error_message'])
        else:
            raise HSSError("GEOLOC req denied")

    elif decoded_resp['status'] == 'ZERO_RESULTS':
        raise HSSError("We couldn't find your address.  Please try again.")

    elif decoded_resp['status'] == 'UNKOWN_ERROR':
        raise HSSError('Service error.  Try again later.')

    elif decoded_resp['status'] == 'OVER_QUERY_LIMIT':
        raise HSSError('Over query limit.')

    else:
        raise HSSError(decoded_resp['status'])

class JSONSerializer():
    """Smart mixin that tags a SQLAlchemy model as serializable"""

    __json_public__     = None
    __json_hidden__     = None
    __json_modifiers__  = None

    def get_attrs(self):
        for name in self.__mapper__.iterate_properties:
            yield name.key

    def to_json(self):
        names = self.get_attrs()
        public = self.__json_public__ or names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        ret = dict()
        for key in public:
            ret[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            val = modifier(getattr(self, key))
            ret[key] = val
        for key in hidden:
            ret.pop(key, None)
        return ret

class JSONEncoder(json.JSONEncoder):
    def default(self, value):
        """Convert more Python data types to ES-understandable JSON."""
        iso = _iso_datetime(value)
        if iso:
            return iso

        if not PY3 and isinstance(value, str):
            return unicode(value, errors='replace')  # TODO: Be stricter.

        if isinstance(value, set):
            return list(value)

        if isinstance(value, JSONSerializer):
            return value.to_json()

        return super(JSONEncoder, self).default(value)


class HSSError(Exception):
    def __init__(self, msg):
        self.msg = msg
