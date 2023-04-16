"""MadamASTra main

This script is responsible for for generating and running the different subsystems of the program

"""

import argparse

# from .Z3Driver import Z3Driver
from .random_word import WordGenerator
from .c_printer import print_content, print_title

def main() -> None:
    '''main function of the program. responsible for 
    1. argparsing
    2. running the wordgenerator, the SMT file generator and the SMT solver #runs times
    3. reporting errors that z3 makes
    '''
    print_title("the clairvoyant will now tell you your fortune")
    # setup arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--supress-warnings")
    parser.add_argument("-r", "--runs", type=int, default=10)

    args = parser.parse_args()

    # setup word generator
    wordgenerator = WordGenerator()

    # setup Z3 driver
    # z3_driver = Z3Driver(args.verbose)

    for run in range(args.runs):
        print_title(f"run {run}")
        word1 = wordgenerator.generate()
        word2 = wordgenerator.generate()
        print_content(f"words: {word1}, {word2}")
    print_title("done")


if __name__ == "__main__":
    main()
