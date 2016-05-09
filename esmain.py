# coding=utf-8
import sys
from ESBase import ESBase
import tornado
import tornado.web
import tornado.options
import tornado.ioloop

__author__ = 'dengjing'


class ESIndexDel(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(ESIndexDel, self).__init__(*args, **kwargs)
        self.es = ESBase()

    def data_received(self, chunk):
        print chunk

    def get(self):
        index = self.get_argument('index')
        if not index:
            self.write('index is illegal')
        ret_dict = self.es.delete(index=index)
        if ret_dict['acknowledged']:
            self.write('success')
        else:
            self.write(ret_dict)


def es_app():
    """
    main function

    :return: app
    """
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/es/index-del", ESIndexDel),
    ])
    return app


def main():
    es_app().listen(int(sys.argv[1]), address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()