import requests
import simplejson as json
from pyelasticsearch.client import _iso_datetime
from six import PY3

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
    for ch in (char for char in string.strip()):
        # replace as single whitespace with a single hyphen
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
    params['address'] = str(address)
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

    elif decoded_resp['status'] == u'ZERO_RESULTS':
        raise HSSError("We couldn't find your address.  Please try again.")

    elif decoded_resp['status'] == 'UNKOWN_ERROR':
        raise HSSError('Service error.  Try again later.')

    elif decoded_resp['stats'] == 'OVER_QUERY_LIMIT':
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
