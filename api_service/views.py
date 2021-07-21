# views.py
import json
from tornado.web import RequestHandler, HTTPError

from common_utils import logger
from db_service.db_python import setup_db
from loader_service.load_attack_surface_data import load_attack_surface_data


class v1Handler(RequestHandler):
    """Only allow GET requests."""
    # SUPPORTED_METHODS = ["GET"]

    def initialize(self):
        input_file = "data/input-0.json"
        self.db = setup_db()
        load_attack_surface_data(input_file, self.db)

    def on_finish(self):
        pass
        
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

