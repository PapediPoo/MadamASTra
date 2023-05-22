"""
This module contains the core search functionality of MadamASTra.
It is responsible for running the Z3Tester, such that it finds new
bugs in Z3 by trying random words and configurations on Z3.
"""

import argparse
import alive_progress
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from random import randint
from random_word import WordGenerator
from c_printer import print_content, print_title
from z3_tester import Z3Tester

def add_parser(parser: argparse.ArgumentParser) -> None:
    '''adds the arguments to the parser used for searching new bugs'''
    parser.set_defaults(run_mode="search")
    parser.set_defaults(run_method=run)
    parser.add_argument("-r", "--runs", type=int, default=5, help="number of times Z3 should be tested")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="Z3 timeout [seconds]. default: 30")
    parser.add_argument("-v", "--verbose", action="store_true", help="makes the command line output more verbose")
    parser.add_argument("--seed", type=int, help="the seed to use for the unsat mode")
    parser.add_argument("-p", "--processes", type=int, default=32, help="number of processes to use. default: 32")

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

    threads = args.processes

    # define work for multiprocessing
    words = wordgenerator.generate(number=args.runs * 2)

    work = []
    for run_no in range(args.runs):
        mode_config, solver_config = configs[run_no % len(configs)]
        word1 = words[run_no * 2]
        word2 = words[run_no * 2 + 1]
        work.append((word1, word2, mode_config, solver_config, args.seed))

    def worker(work_item):
        # define worker function
        word1, word2, mode_config, solver_config, seed = work_item
        z3_tester.test(mode_config, solver_config, seed=seed)
        print_content(f"words: {word1:10}, {word2:10}, mode: {mode_config:5}, solver: {solver_config:7}")

    print_content(f"running {args.runs} times")

    pool = ThreadPool(threads)
    # define progress bar function
    with alive_progress.alive_bar(args.runs) as progress:
        for _ in pool.imap_unordered(worker, work):
            progress()

    pool.close()
    pool.join()

    # print errors
    print_title("done")
    z3_tester.print_errors()
