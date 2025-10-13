from src.project import *
from src.Task import * 
from CLI.parser import CLI 
from CLI.commands import *
import argparse


"""
I structure the CLI as a ArgParser 
Which we pass what we want and it will call the correct function
for that need.

like a office which some one can redirect you to subsections

It would look like 

poetry run main.py create_task .... 
"""
def main():
    # ___ Parser Part ____
    cli = CLI()
    parser = cli.create_parser()
    args = parser.parse_args()
    # ___ Executive Part ___
    cli.exec_command(args)


if __name__ == "__main__":
    main()