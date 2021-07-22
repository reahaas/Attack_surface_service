import itertools

import networkx as nx

from common_utils import flatten, remove_duplication


class DbPython():
    def __init__(self):
        self.vm_to_potentially_attackers = {}
        self.tag_to_potentially_attackers = {}
        
        # For more information visit: https://networkx.org/documentation/stable/reference/classes/digraph.html
        self.tags_directed_graph = nx.DiGraph()
    
    def get_potentially_attackers(self, vm_id: str) -> list:
        if vm_id not in self.vm_to_potentially_attackers:
            raise KeyError(f"{vm_id} not exists in the db.")
        
        potentially_attackers = self.vm_to_potentially_attackers.get(vm_id)
        potentially_attackers_ids = [vm.get("vm_id") for vm in potentially_attackers]
        return potentially_attackers_ids
    
    def get_vms_count(self):
        return len(self.vm_to_potentially_attackers)


def save_tag_to_vms(db, tags_to_vms):
    for tag in tags_to_vms:
        db[tag] = tags_to_vms[tag]


def build_tags_directed_graph(db, fw_rules):
    for rule in fw_rules:
        db.tags_directed_graph.add_edge(rule.get("source_tag"), rule.get("dest_tag"))


def build_vms_to_potentially_attackers(db, vms):
    tag_to_allowed_to_access_tags = {}
    
    tag_to_potentially_attackers = initialize_tags_tp_potentially_attackers(vms)
    
    for tag in db.tags_directed_graph.nodes():
        tag_to_allowed_to_access_tags[tag] = list(db.tags_directed_graph.predecessors(tag))
    
    for tag in db.tags_directed_graph.nodes():
        tag_to_potentially_attackers[tag] = [vm for vm in vms if any(
            vm_tag in tag_to_allowed_to_access_tags[tag] for vm_tag in vm.get("tags"))]
    
    vms_to_potentially_attackers = {}
    for vm in vms:
        vms_to_potentially_attackers[vm.get("vm_id")] = flatten(
            [tag_to_potentially_attackers[tag] for tag in vm.get("tags")])
    
    db.tag_to_potentially_attackers = tag_to_potentially_attackers
    db.vm_to_potentially_attackers = vms_to_potentially_attackers


def initialize_tags_tp_potentially_attackers(vms):
    tag_to_potentially_attackers = {}
    all_vms_tags = flatten([vm.get("tags") for vm in vms if vm.get("tags")])
    set_all_vms_tags = remove_duplication(all_vms_tags)
    for tag in set_all_vms_tags:
        tag_to_potentially_attackers[tag] = []
    return tag_to_potentially_attackers
