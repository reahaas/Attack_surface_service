def setup_db():
    return DbPython()


class DbPython():
    def __init__(self):
        self.vms_to_potentially_attackers = {}
        self.requests_stats = {}
        
    def add_vm(self, vm_id, potential_attackers):
        self.vms_to_potentially_attackers[vm_id] = potential_attackers
