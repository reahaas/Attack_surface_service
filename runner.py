import argparse
import logging

from db_service.db_python import setup_db
from loader_service.load_attack_surface_data import load_attack_surface_data

logging.basicConfig(level = logging.INFO)

def get_command_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-f", "--input_file",
                        help="input file: json: {'vms': [ virtual machines ], 'fw_rules': [ firewall rules ]}")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_command_args()
    db = setup_db()
    load_attack_surface_data(args.input_file, db)
    # print(db.vms_to_potentially_attackers)
