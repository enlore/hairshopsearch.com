from ..config import Config
from pyelasticsearch import ElasticSearch
from ..helpers import JSONEncoder
from .mappings import MAPPINGS

# need mappings storage
es = ElasticSearch(Config.ELASTICSEARCH_SERVER)
es.json_encoder = JSONEncoder

def index_one(entity, id):
    # doc = JSONEncoder().encode(entity)
    doc_type = 'provider'
    index = 'hairshopsearch'
    resp = es.index(index, doc_type, entity, id=id)
    return resp

def index_many():
    # bulk_index()
    pass

def create_index(doc_type):
    resp = es.create_index('hairshopsearch', settings=None)
    print resp

    resp1 = es.put_mapping('hairshopsearch',
            doc_type=doc_type,
            mapping=MAPPINGS['PROVIDER'])
    print resp1

def reset_index(doc_type):
    resp = es.delete_index('hairshopsearch')
    print resp

    create_index(doc_type)

