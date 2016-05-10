# coding=utf-8
import json
from ESBase import ESBase
from tornado import ioloop
from tornado import queues
from tornado import gen

from SQSBase import get_message

__author__ = 'dengjing'

q = queues.Queue(maxsize=3)
es = ESBase()


@gen.coroutine
def handle_es_create_index(message):
    body = message[0].body
    j_body = json.loads(body)
    print j_body['op_type']
    if j_body['op_type'] == 'add':
        res = es.index(j_body)
        if res['created']:
            message[0].delete()
            return True
        return False
    if j_body['op_type'] == 'change':
        res = es.upgrade(body={"doc": j_body}, doc_id=j_body['id'])
        return type(res['_version']) == int
    if j_body['op_type'] == 'remove':
        res = es.remove(doc_id=j_body['id'])
        return type(res['_version']) == int


@gen.coroutine
def consumer():
    while True:
        print('consumer waiting...')
        item = yield q.get()
        try:
            print('Get %s' % item)
            res = yield handle_es_create_index(item)
            if res:
                print 'success handle item[0].body'
            else:
                print 'fail in handle item[0].body'
            yield gen.sleep(0.01)
            print('the number of consumer qsize %d' % q.qsize())
        finally:
            q.task_done()


@gen.coroutine
def producer():
    while True:  # change to whether connect sqs
        item = get_message()
        if len(item) == 0:
            print('the number of producer qsize %d' % q.qsize())
            yield gen.sleep(0.01)
            continue
        print('Put %s' % item)
        yield q.put(item)
        yield gen.sleep(0.01)


@gen.coroutine
def main():
    while True:
        ioloop.IOLoop.current().spawn_callback(consumer)
        yield producer()
        yield q.join()       # Wait for consumer to finish all tasks.
        print('Done')


if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)