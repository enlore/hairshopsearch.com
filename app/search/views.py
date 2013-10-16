from flask import Blueprint, render_template, current_app
from ..core import es
from .forms import SearchForm

search = Blueprint('search', __name__, template_folder='templates',
    url_prefix='/search')

@search.route('/', methods=['POST'])
def _search():
    form = SearchForm()
    if form.validate_on_submit():
        current_app.logger.info(form.business_name.data)
        resp = es.search('business_name:%s' % form.business_name.data, index='providers',
                doc_type='provider')
        if resp:
            names = []
            for hit in resp['hits']['hits']:
                names.append(hit['_source']['business_name'])
            return render_template('search/serp.html', names=names)
    return 'Butts', 404
