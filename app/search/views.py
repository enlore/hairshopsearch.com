from flask import Blueprint, render_template, current_app
from ..core import es
from ..helpers import lat_lon
from ..user.models import Provider, Address
from .forms import SearchForm

search = Blueprint('search', __name__, template_folder='templates',
    url_prefix='/search')


def searched_out_objects(ids):
    objects = []
    for _id in ids:
        p = Provider.query.get(_id)
        objects.append(p)

    return objects

@search.route('/test')
def _search_test():
    p = Provider.query.first()
    return render_template('search/serp.html', providers=[p])

@search.route('/', methods=['POST'])
def _search():
    form = SearchForm()
    if form.validate_on_submit():
        a = Address()
        a.zip_code = form.zip_code.data
        lat, lon = lat_lon(a)[0]
        query = {
            "query": {
                "filtered": {
                    "query": {
                        "nested": {
                            "path": "menus",
                            "query": {
                                "bool": {
                                    "must": {
                                        "term": { "menus.menu_type": form.menu_type.data }
                                    },
                                    "should": {
                                        "nested": {
                                            "path": "menus.menu_items",
                                            "query": {
                                                "match": { "name": form.service.data }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "filter": {
                        "geo_distance": {
                            "distance": "50mi",
                            "location": {
                                "lat": lat,
                                "lon": lon
                            }
                        }
                    }
                }
            },
            "size": 20
        }
        results = es.search(query, index='providers', doc_type='provider')
        ids = []
        for result in results['hits']['hits']:
            ids.append(result['_source']['id'])

        current_app.logger.info('hits: %s' % results['hits']['total'])

        providers = searched_out_objects(ids)
        current_app.logger.info(providers[0].business_name)
        return render_template('search/serp.html', providers=providers)
    return 'Butts', 404
