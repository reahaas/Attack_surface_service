import pytest

from db_service.db_python import build_vms_to_potentially_attackers, DbPython
from db_service.db_python import build_tags_directed_graph

fw_rules_json_0 = [{"fw_id": "fw-82af742", "source_tag": "ssh", "dest_tag": "dev"}]
vms_json_0 = [{"vm_id": "vm-a211de", "name": "jira_server", "tags": ["ci", "dev"]},
              {"vm_id": "vm-c7bac01a07", "name": "bastion", "tags": ["ssh", "dev"]}]

fw_rules_json_1 = [{"fw_id": "fw-c4a11ac", "source_tag": "k8s", "dest_tag": "loadbalancer"},
                   {"fw_id": "fw-1cb4c1", "source_tag": "django", "dest_tag": "django"},
                   {"fw_id": "fw-0d91970ee", "source_tag": "corp", "dest_tag": "django"},
                   {"fw_id": "fw-778beb64", "source_tag": "django", "dest_tag": "nat"},
                   {"fw_id": "fw-1008d7", "source_tag": "ssh", "dest_tag": "ssh"},
                   {"fw_id": "fw-1c8ebac1f", "source_tag": "loadbalancer", "dest_tag": "corp"},
                   {"fw_id": "fw-06bf6a628", "source_tag": "nat", "dest_tag": "nat"},
                   {"fw_id": "fw-9d030bb4bb", "source_tag": "corp", "dest_tag": "nat"},
                   {"fw_id": "fw-fbcfcc16e1", "source_tag": "antivirus", "dest_tag": "nat"},
                   {"fw_id": "fw-c74204", "source_tag": "antivirus", "dest_tag": "antivirus"}]

vms_json_1 = [{"vm_id": "vm-b8e6c350", "name": "rabbitmq", "tags": ["windows-dc"]},
              {"vm_id": "vm-c1e6285f", "name": "k8s node", "tags": ["http", "ci"]},
              {"vm_id": "vm-cf1f8621", "name": "k8s node", "tags": ["windows-dc"]},
              {"vm_id": "vm-b462c04", "name": "jira server", "tags": ["windows-dc", "storage"]},
              {"vm_id": "vm-8d2d12765", "name": "kafka", "tags": []},
              {"vm_id": "vm-9cbedf7c66", "name": "etcd node", "tags": []},
              {"vm_id": "vm-ae24e37f8a", "name": "frontend server", "tags": ["api", "dev"]},
              {"vm_id": "vm-e30d5fa49a", "name": "etcd node", "tags": ["dev", "api"]},
              {"vm_id": "vm-1b1cc9cd", "name": "billing service", "tags": []},
              {"vm_id": "vm-f270036588", "name": "kafka", "tags": []}]


class TestAttackLogic:
    
    def setup_method(self, test_method):
        self.db = DbPython()
        
        build_tags_directed_graph(self.db, fw_rules_json_1)
    
    def test_tags_directed_graph_tags(self):
        build_tags_directed_graph(self.db, fw_rules_json_1)
        
        all_tags = self.db.tags_directed_graph.nodes()
        
        expected_tags = ['k8s', 'loadbalancer', 'django', 'corp', 'nat', 'ssh', 'antivirus']
        assert set(all_tags) == set(expected_tags)
    
    def test_predesessors_of_tag(self):
        build_tags_directed_graph(self.db, fw_rules_json_1)
        
        tag = "django"
        
        allowed_to_connect_to_tag = list(self.db.tags_directed_graph.predecessors(tag))
        
        expected_allowed_to_connect_to_tag = ['django', 'corp']
        assert set(allowed_to_connect_to_tag) == set(expected_allowed_to_connect_to_tag)
    
    def test_build_vms_to_potentially_attackers(self):
        build_tags_directed_graph(self.db, fw_rules_json_0)
        build_vms_to_potentially_attackers(self.db, vms_json_0)
        
        json_1_attacked_vm_id = "vm-a211de"
        potentially_attackers_ids = self.db.get_potentially_attackers(json_1_attacked_vm_id)
        
        json_1_attacker_vm_id = "vm-c7bac01a07"
        expected_potentially_attackers = [json_1_attacker_vm_id]
        assert set(potentially_attackers_ids) == set(expected_potentially_attackers)
    
    def test_build_vms_to_potentially_attackers_can_attack_itself(self):
        build_tags_directed_graph(self.db, fw_rules_json_0)
        build_vms_to_potentially_attackers(self.db, vms_json_0)
        
        json_1_attacked_vm_id = "vm-c7bac01a07"
        potentially_attackers_ids = self.db.get_potentially_attackers(json_1_attacked_vm_id)
        
        # The vm can attack itself since it have two tags, and a rule connecting them
        json_1_attacker_vm_id = json_1_attacked_vm_id
        expected_potentially_attackers = [json_1_attacker_vm_id]
        assert set(potentially_attackers_ids) == set(expected_potentially_attackers)
    
    def test_build_vms_to_potentially_attackers_no_attackers(self):
        build_tags_directed_graph(self.db, fw_rules_json_1)
        build_vms_to_potentially_attackers(self.db, vms_json_1)
        
        # That the "kafka" vm.
        json_1_attacked_vm_id_with_no_tags = "vm-8d2d12765"
        potentially_attackers_ids = self.db.get_potentially_attackers(json_1_attacked_vm_id_with_no_tags)
        
        # There are no vms that can attack this vm, since it have no tags.
        expected_potentially_attackers = []
        assert set(potentially_attackers_ids) == set(expected_potentially_attackers)
    
    def test_build_vms_to_potentially_attackers_vm_id_not_exists(self):
        build_tags_directed_graph(self.db, fw_rules_json_0)
        build_vms_to_potentially_attackers(self.db, vms_json_1)
        
        json_1_attacked_vm_id_not_exists = "vm-not-exists"
        ####
        with pytest.raises(KeyError):
            potentially_attackers_ids = self.db.get_potentially_attackers(json_1_attacked_vm_id_not_exists)
