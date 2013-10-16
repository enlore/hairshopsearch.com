from app.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.user.models import Provider
from pyelasticsearch import ElasticSearch
from app.helpers import JSONEncoder

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
sess = Session(bind=engine)

# put_mapping(type, {type: {"properties": {"name": {"type": "string", "store": "yes"}}}})
# index(index, type, document, id)  # pass the id
# count("prop:value")
# get(index, type, id)
# morelikethis(index, type, id, [term], min_term_freq=1, min_doc_freq=1)
# search("prop:value OR prop:value", index=index)
# search(query, index=index)
# delete(index, type, id)
# delete_by_query(index, type, query)

# create_index(index)
# refresh([index, index..])
# status([index])
# flush([index])
# optimize([index])
# terms(['term'])
# terms(['term'], indexes=['index', 'index'...])
# terms(['term'], min_freq=2)
# delete_index("index")

# query is a dict written in the style of the ES query DSL

es = ElasticSearch('http://localhost:9200/')
es.json_encoder = JSONEncoder
es.delete_index('providers')
es.create_index('providers')


def indexer():
    res = sess.query(Provider).all()[0:1000]
    for p in res:
        resp = es.index('providers', 'provider', p, p.id)
        if resp:
            print "inserted doc into %s at id %s" % (resp['_index'], resp['_id'])
indexer()
