import argparse
import logging

from tornado_server import main

logging.basicConfig(level=logging.INFO)


def get_command_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-f", "--input_file",
                        help="input file: json: {'vms': [ virtual machines ], 'fw_rules': [ firewall rules ]}")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_command_args()
    main(args.input_file)
