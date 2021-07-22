import tornado.ioloop
import tornado.web

import sys
print(sys.path)

from api_service.views import v1Handler, StatsHandler


#
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/v1/attack", v1Handler),
        (r"/v1/stats", StatsHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
