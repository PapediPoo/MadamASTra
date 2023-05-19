"""
This module contains the function for trying two words on Z3,
but with different solver configurations.
Z3 is not entirely deterministic, so it is possible that Z3
will give different results for the same input.
This module tries to find such cases.
"""

import argparse
from itertools import product
from c_printer import print_content, print_title
from z3_tester import Z3Tester


def add_parser(parser: argparse.ArgumentParser) -> None:
    '''
    adds the arguments to the parser used for trying given words on Z3
    '''
    parser.set_defaults(run_mode="try")
    parser.set_defaults(run_method=run)
    parser.add_argument("word1", help="first word")
    parser.add_argument("word2", help="second word")
    parser.add_argument("-s", "--solver",
                        choices=["seq", "z3str3", "both"],
                        default="both",
                        help="the solver to use. default: both")
    parser.add_argument("-m", "--mode",
                        choices=["sat", "unsat", "both"],
                        default="both",
                        help="the mode to use. default: both")
    parser.add_argument("-t", "--timeout",
                        type=int,
                        default=30,
                        help="Z3 timeout [seconds]. default: 30")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        default=False,
                        help="makes the command line output more verbose")
    parser.add_argument("-r", "--retry",
                        action="store_true",
                        default=False,
                        help="retry until Z3 makes a mistake")
    parser.add_argument("--seed",
                        type=int,
                        help="the seed to use for the unsat mode")


def run(args: argparse.Namespace) -> None:
    '''tries word1 and word2 on Z3
    args: the parsed arguments from the CLI
    '''

    # setup Z3 tester
    z3_tester = Z3Tester(args.verbose, args.timeout)

    print_content(f"words: {args.word1}, {args.word2}")

    if args.mode == "both":
        modes = ["sat", "unsat"]
    elif args.mode == "sat":
        modes = ["sat"]
    elif args.mode == "unsat":
        modes = ["unsat"]
    else:
        raise Exception("unknown mode. Z3Tester only supports sat and unsat")

    if args.solver == "both":
        solvers = ["seq", "z3str3"]
    elif args.solver == "seq":
        solvers = ["seq"]
    elif args.solver == "z3str3":
        solvers = ["z3str3"]
    else:
        raise Exception(
            "unknown solver. Z3Tester only supports seq and z3str3")

    configs = list(product(modes, solvers))

    if args.retry:
        # retry until Z3 makes a mistake. iteratively try all configurations
        print_content("retrying until Z3 makes a mistake")
        print_title("starting")
        config_index = 0
        while not z3_tester.test(
                args.word1,
                args.word2,
                *configs[config_index], seed=args.seed):
            config_index = (config_index + 1) % len(configs)
            print_title("retrying")
    else:
        # run Z3 once for each configuration
        print_content("running Z3 once for each configuration")
        print_title("starting")
        for mode, solver in configs:
            z3_tester.test(args.word1, args.word2, mode, solver, seed=args.seed)

    print_title("done")
    z3_tester.print_errors()
