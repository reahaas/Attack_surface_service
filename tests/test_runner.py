from db_service.db_python import DbPython
from loader_service.load_attack_surface_data import load_attack_surface_data


def test_load_attack_surface_data():
    """
    In "input-0.json" scenario there are two vms and one rule.
    vm_id_2 = 'vm-c7bac01a07' can attack both the vms.
    :return:
    """
    input_file = "data/input-0.json"
    
    db = DbPython()
    load_attack_surface_data(input_file, db)
    vm_id_1 = 'vm-a211de'
    vm_id_2 = 'vm-c7bac01a07'
    
    expected_vms_to_potentially_attackers_vm_id_1 = [vm_id_2]
    assert db.get_potentially_attackers(vm_id_1) == expected_vms_to_potentially_attackers_vm_id_1
    
    expected_vms_to_potentially_attackers_vm_id_2 = [vm_id_2]
    assert db.get_potentially_attackers(vm_id_2) == expected_vms_to_potentially_attackers_vm_id_2
