from elasticsearch import Elasticsearch
import certifi

try:
    # create connection
    # es = Elasticsearch(
    #     ['hostname'],
    #     http_auth=('YOUR_USERNAME', 'YOUR_PASSWORD'),
    #     port=9200,
    #     use_ssl=False,
    #     verify_certs=False,
    #     ca_certs=certifi.where(),
    # )

    es = Elasticsearch([{'host': 'hostname', 'port': 9200}])

    print "Connected", es.info()

    # get a doc by id
    print es.get(index='myindex', id='105')

    # get a doc by DSL
    result = es.search(index='myindex', body={
        'query': {
            'match': {
             "attachment.content": "Postpuller"
            }
        }
    })
    # print result
    print 'ok'

    # delete a doc
    # es.delete(index='myindex', doc_type='post', id=1)


except Exception as ex:
    print "Error:", ex
