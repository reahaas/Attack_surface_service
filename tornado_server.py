import tornado.ioloop
import tornado.web

import sys

from db_service.db_python import setup_db
from loader_service.load_attack_surface_data import load_attack_surface_data

print(sys.path)

from api_service.views import v1Handler, StatsHandler


def make_app():
    v1_handler_paramters = {"database": praper_db_for_tornado()}
    
    return tornado.web.Application([(r"/v1/attack", v1Handler, v1_handler_paramters), (r"/v1/stats", StatsHandler)])


def praper_db_for_tornado():
    input_file = "data/input-0.json"
    db = setup_db()
    load_attack_surface_data(input_file, db)
    return db


if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
