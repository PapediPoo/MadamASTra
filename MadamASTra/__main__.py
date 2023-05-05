"""MadamASTra main

This script is responsible for for generating
and running the different subsystems of the program

"""

import argparse
from core_search import add_parser as add_search_parser
from core_try import add_parser as add_try_parser
from core_log import add_parser as add_log_parser
from c_printer import print_title

def main() -> None:
    '''main function of the program. responsible for
    1. argparsing
    2. running the wordgenerator,
    the SMT file generator and the SMT solver #runs times
    3. reporting errors that z3 makes
    '''
    print_title("the clairvoyant will now tell you your fortune")
    # setup arg parser
    parser = argparse.ArgumentParser(
        prog="MadamASTra", 
        description="MadamASTra is a tool for finding bugs in Z3"
        )
    subparsers = parser.add_subparsers()
    add_search_parser(subparsers.add_parser("search", help="search for bugs in Z3"))
    add_try_parser(subparsers.add_parser("try", help="try the 2 provided words on Z3"))
    add_log_parser(subparsers.add_parser("log", help="print the SMT file that would be generated for the 2 provided words"))

    args = parser.parse_args()
    args.run_method(args)
    

if __name__ == "__main__":
    main()
