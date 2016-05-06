# coding=utf-8
from elasticsearch import Elasticsearch

__author__ = 'dengjing'


INDEX = 'test-index'


class ESBase:

    def __init__(self):
        self.es = Elasticsearch([{'host': '182.92.220.227', 'port': 8008}])

    def index(self, body, index=INDEX, doc_type="tweet"):
        return self.es.index(index=index, doc_type=doc_type, body=body)

    def search(self, body, index=INDEX, doc_type="tweet"):
        return self.es.search(index=index, doc_type=doc_type, body=body)