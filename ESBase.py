# coding=utf-8
from elasticsearch import Elasticsearch

__author__ = 'dengjing'


# INDEX = 'test-index'
INDEX = 'just-test'
DOC_TYPE = 'tweet'


class ESBase:
    def __init__(self):
        self.es = Elasticsearch([{'host': '182.92.220.227', 'port': 8008}])

    def index(self, body, index=INDEX, doc_type=DOC_TYPE):
        doc_id = body['id']
        return self.es.index(index=index, doc_type=doc_type, body=body, id=doc_id)

    def upgrade(self, body, doc_id, index=INDEX, doc_type=DOC_TYPE):
        return self.es.update(index=index, body=body, doc_type=doc_type, id=doc_id)

    def search(self, body, index=INDEX, doc_type=DOC_TYPE):
        return self.es.search(index=index, doc_type=doc_type, body=body)

    def remove(self, doc_id, index=INDEX, doc_type=DOC_TYPE):
        return self.es.delete(index=index, doc_type=doc_type, id=doc_id)

    # index delete
    def delete(self, index):
        return self.es.indices.delete(index=index)


if __name__ == '__main__':
    es = ESBase()
    # print es.delete(index='test-index')
    # print es.upgrade(index=INDEX, body={"doc" :{"text":"hahass","id": "736ff38b946db55e52487bd75ccf5d66",
    # "en_title": "dengjing-test","op_type": "add"}}, doc_id='736ff38b946db55e52487bd75ccf5d66')
    # print es.remove(doc_id='ca931e2bbc0aae7210b745a17e0cf8d0')
    b = {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": u"text:me"}},
                ]
            }
        },
    }
    print es.search(body=b)
