"""
This module contains the core search functionality of MadamASTra.
It is responsible for running the Z3Tester, such that it finds new
bugs in Z3 by trying random words and configurations on Z3.
"""

import argparse
from random import randint
from random_word import WordGenerator
from c_printer import print_content, print_title
from z3_tester import Z3Tester

def add_parser(parser: argparse.ArgumentParser) -> None:
    '''adds the arguments to the parser used for searching new bugs'''
    parser.set_defaults(run_mode="search")
    parser.set_defaults(run_method=run)
    parser.add_argument("-r", "--runs", type=int, default=5, help="number of times Z3 should be tested")
    parser.add_argument("-wl", "--word-length",
                        type=int,
                        default=5,
                        help="generated word length. Longer words => Z3 slower")
    parser.add_argument("-wr", "--word-randomness", type=int, default=1, help="randomness of the length of words")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="Z3 timeout [seconds]. default: 30")
    parser.add_argument("-v", "--verbose", action="store_true", help="makes the command line output more verbose")

def run(args: argparse.Namespace) -> None:
    '''runs the search for bugs
    1. running the wordgenerator, the SMT file generator and the SMT solver #runs times
    2. reporting errors that z3 makes
    3. reporting the number of errors that z3 made
    4. saving the errors to a file
    args: the parsed arguments from the CLI
    '''
    # setup word generator
    wordgenerator = WordGenerator()

    # setup Z3 tester
    z3_tester = Z3Tester(args.verbose, args.timeout)

    configs = [
        ("sat", "seq"),
        ("unsat", "seq"),
        ("sat", "z3str3"),
        ("unsat", "z3str3")]

    print_content(f"running {args.runs} times")
    for run_no in range(args.runs):
        print_title(f"run {run_no+1}")

        # generate words
        word1 = wordgenerator.generate(args.word_length + randint(-args.word_randomness, args.word_randomness))
        word2 = wordgenerator.generate(args.word_length + randint(-args.word_randomness, args.word_randomness))

        print_content(f"words: {word1}, {word2}")

        # generate SMT file
        mode_config, solver_config = configs[run_no % len(configs)]

        # run Z3
        z3_tester.test(word1, word2, mode_config, solver_config)

    # print errors
    print_title("done")
    z3_tester.print_errors()
