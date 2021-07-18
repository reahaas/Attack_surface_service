from db_service.db_python import setup_db
from loader_service.load_attack_surface_data import load_attack_surface_data


def test_load_attack_surface_data():
    input_file = "data/input-0.json"
    
    db = setup_db()
    load_attack_surface_data(input_file, db)
    
    expected_vms_to_potentially_attackers = {'vm-a211de': [], 'vm-c7bac01a07': []}
    assert db.vms_to_potentially_attackers == expected_vms_to_potentially_attackers
