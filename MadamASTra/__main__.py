"""MadamASTra main

This script is responsible for for generating and running the different subsystems of the program

"""

import argparse
from random import randint
from formula_generator import get_sat_z3_formulas, get_unsat_z3_formula, wrap_formula

from z3_driver import Z3Driver
from random_word import WordGenerator
from c_printer import print_content, print_title


def main() -> None:
    '''main function of the program. responsible for 
    1. argparsing
    2. running the wordgenerator, the SMT file generator and the SMT solver #runs times
    3. reporting errors that z3 makes
    '''
    print_title("the clairvoyant will now tell you your fortune")
    # setup arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="makes the command line output more verbose")
    parser.add_argument("-s", "--supress-warnings", help="currently does nothing")
    parser.add_argument("-r", "--runs", type=int, default=5, help="number of times Z3 should be tested")
    parser.add_argument("-wl", "--word-length", type=int, default=5, help="length of the generated words. Longer words => Z3 slower")
    parser.add_argument("-wr", "--word-randomness", type=int, default=1, help="randomness of the length of words")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="Z3 timeout [seconds]. default: 30")

    args = parser.parse_args()

    # setup word generator
    wordgenerator = WordGenerator()

    # setup Z3 driver
    z3_driver = Z3Driver(args.verbose, args.timeout)

    for run in range(args.runs):
        print_title(f"run {run}")
        word1 = wordgenerator.generate(args.word_length + randint(-args.word_randomness, args.word_randomness))
        word2 = wordgenerator.generate(args.word_length + randint(-args.word_randomness, args.word_randomness))
        print_content(f"words: {word1}, {word2}")

        if run%2 == 0: # test SAT
            generated_z3_formula, _ = get_sat_z3_formulas(word1, word2)
        else: # test UNSAT
            generated_z3_formula = get_unsat_z3_formula(word1, word2)
        full_input = wrap_formula(generated_z3_formula)
        z3_result = z3_driver.run(full_input)
        print_content("Z3 Response: " + z3_result)
    print_title("done")


if __name__ == "__main__":
    main()
