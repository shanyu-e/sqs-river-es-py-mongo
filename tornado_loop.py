# coding=utf-8
from tornado import ioloop
from tornado import queues
from tornado import gen

from SQSBase import get_message

__author__ = 'dengjing'

q = queues.Queue(maxsize=3)


@gen.coroutine
def consumer():
    while True:
        print(u'消费者等待中...')
        item = yield q.get()
        try:
            print('Get %s' % item[0].body)
            yield gen.sleep(0.01)
            print(u'消费者当前队列中等待消费的数目%d' % q.qsize())
        finally:
            q.task_done()


@gen.coroutine
def producer():
    while True:  # 之后改为消息是否联通
        item = get_message()
        if len(item) == 0:
            print(u'生产者当前队列中等待消费的数目%d' % q.qsize())
            yield gen.sleep(0.01)
            continue
        print('Put %s' % item[0].body)
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