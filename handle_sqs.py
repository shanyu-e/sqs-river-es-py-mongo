# coding=utf-8
import json
import boto3
from elasticsearch import Elasticsearch

__author__ = 'dengjing'

es = Elasticsearch([{'host': '182.92.220.227', 'port': 8008}])


def main():
    sqs = boto3.resource('sqs')
    queue = sqs.Queue(url='https://us-west-2.queue.amazonaws.com/052792705405/river')
    while queue.receive_messages():
        ms = queue.receive_messages()
        message = ms[0]
        m1 = message.body
        m_body = json.loads(m1)
        print m_body.get('en_title')
        doc_body = json.dumps(m_body)
        res = es.index(index="test-index", doc_type='tweet', body=doc_body)
        print(res['created'])
        message.delete()


if __name__ == '__main__':
    main()
    # res = es.get(index="test-index", doc_type='tweet', id=1)
    # print(res['_source'])
    #
    # print es.search(index='test-index', q='text:所有新增和过往的文稿都可以在这里查看',
    # filter_path=['hits.hits._id', 'hits.hits._source["id"]'])
    # print es.search(index='test-index', doc_type='tweet', q='text:"所有新增和过往的文稿都可以在这里查看"')
    # j = json.loads('''
    # {
    #    "query" : {
    #        "match_phrase" : {
    #            "text" : "Windows/Mac/Linux"
    #        }
    #    },
    #    "highlight": {
    #        "fields" : {
    #            "text" : {}
    #        }
    #    }
    # }
    # ''')
    # print es.search(index='test-index', doc_type='tweet', body=j, size=1)
