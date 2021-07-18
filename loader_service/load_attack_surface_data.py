import json
from logging import getLogger


from loader_service.fw_rules_matcher import get_potential_attackers

logger = getLogger("load_attack_surface_data")


def read_csv_file(file_path):
    """

    :param file_path:
    :param class data_type: namedtuple class type, to convert the data to.
    :return list(namedtuple):
    """
    with open(file_path, newline='') as f:
        data = json.load(f)
    return data


def read_data_file(input_file):
    data = read_csv_file(input_file)
    vms = data.get("vms", [])
    fw_rules = data.get("fw_rules", [])
    logger.info(f"data loaded: vms: [{len(vms)}], rules: [{len(fw_rules)}]")
    return vms, fw_rules


def load_attack_surface_data(input_file, db):
    logger.info("load_attack_surface_data")
    
    vms, fw_rules = read_data_file(input_file)
    
    for vm in vms:
        potential_attackers = get_potential_attackers(vm, fw_rules)
        db.add_vm(vm.get("vm_id", ""), potential_attackers)
    logger.info("Wooho!! load_attack_surface_data finished.")
    logger.info(db.vms_to_potentially_attackers)
