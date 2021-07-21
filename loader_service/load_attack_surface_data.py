import json

from common_utils import log_runtime_duration, logger
from db_service.db_python import build_tags_directed_graph, build_vms_to_potentially_attackers, DbPython


def read_csv_file(file_path: str) -> dict:
    """

    :param file_path:
    :param class data_type: namedtuple class type, to convert the data to.
    :return list(namedtuple):
    """
    with open(file_path, newline='') as f:
        data = json.load(f)
    return data


def read_data_file(input_file: str) -> tuple:
    data = read_csv_file(input_file)
    vms = data.get("vms", [])
    fw_rules = data.get("fw_rules", [])
    logger.info(f"data loaded: vms: [{len(vms)}], rules: [{len(fw_rules)}]")
    return vms, fw_rules


@log_runtime_duration
def load_attack_surface_data(input_file: str, db: DbPython):
    """
    Load data from file and initial the db with the data structure.
    :param input_file:
    :param db:
    """
    vms, fw_rules = read_data_file(input_file)
    
    build_tags_directed_graph(db, fw_rules)
    
    build_vms_to_potentially_attackers(db, vms)
