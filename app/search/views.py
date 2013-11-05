from flask import Blueprint, render_template, current_app, flash
from ..core import es
from ..helpers import lat_lon
from ..models import Provider, Address
from .forms import SearchForm

search = Blueprint('search', __name__, template_folder='templates',
    url_prefix='/search')

def searched_out_objects(ids):
    objects = []
    for _id in ids:
        p = Provider.query.get(_id)
        if p:
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
        current_app.logger.info(a.zip_code)

        # TODO lat_lon expects an address object. this is perhaps silly
        lat, lon = lat_lon(a)[0]

        current_app.logger.info(str(lat) + ' ' + str(lon))
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
                    }, # /query
                    "filter": {
                        "geo_distance": {
                            "distance": "50mi",
                            "location": {
                                "lat": lat,
                                "lon": lon
                            }
                        }
                    } # /filter
                }
            },
            "size": 20
        }
        results = es.search(query, index='providers', doc_type='provider')
        current_app.logger.info(results)
        ids = []
        if results['hits']['total'] > 0:
            for result in results['hits']['hits']:
                ids.append(result['_id'])

            current_app.logger.info('hits: %s' % results['hits']['total'])
            current_app.logger.info(ids)

            providers = searched_out_objects(ids)

            return render_template('search/serp.html', providers=providers)

        else:
            current_app.logger.info('No results found!')
            flash('No results found!', 'error')
            return render_template('search/serp.html')
    # TODO flash errors and get them rendered
    return render_template('search/serp.html')
