import tornado.ioloop
import tornado.web

from api_service.api_stats import ApiStats
from db_service.db_python import DbPython
from loader_service.load_attack_surface_data import load_attack_surface_data
from api_service.views import v1Handler, StatsHandler


def make_app(db: DbPython):
    v1_handler_paramters = {"database": db}
    ApiStats.update_vms_count(db.get_vms_count())
    
    return tornado.web.Application([
        (r"/v1/attack", v1Handler, v1_handler_paramters),
        (r"/v1/stats", StatsHandler)]
    )


def praper_db_for_tornado(input_file: str) -> DbPython:
    db = DbPython()
    load_attack_surface_data(input_file, db)
    return db


def main(input_file: str):
    db = praper_db_for_tornado(input_file)
    
    app = make_app(db)
    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
