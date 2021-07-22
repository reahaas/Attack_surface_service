# views.py
import datetime
import json
from tornado.web import RequestHandler, HTTPError

from api_service.api_stats import ApiStats
from common_utils import logger


class MonitoredRequestHandler(RequestHandler):
    async def prepare(self):
        self.start_time = datetime.datetime.utcnow()
        ApiStats.increase_counter()
    
    def on_finish(self):
        self.end_time = datetime.datetime.utcnow()
        ApiStats.update_averga_request_time(self.end_time - self.start_time)


class v1Handler(MonitoredRequestHandler):
    def initialize(self, database):
        self.db = database
    
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
    
    def get(self):
        """Construct and send a JSON response with appropriate status code."""
        
        vm_id = self.get_argument('vm_id')
        
        try:
            potentially_attackers = self.db.get_potentially_attackers(vm_id)
        except KeyError:
            raise HTTPError(status_code=404, log_message=f"vm_id [{vm_id}] not exists in the db.")
        self.write(json.dumps(potentially_attackers))


class StatsHandler(MonitoredRequestHandler):
    
    def get(self):
        # take a look at this one:
        # https://gist.github.com/DmitryBe/07305b2fa0f5809f5016e8e29df50f11
        self.write(ApiStats.get_stats_data())
