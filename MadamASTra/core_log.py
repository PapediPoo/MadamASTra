"""
This module is responsible for generating SMT files that trigger
errors in Z3. Its not going to run Z3, but it will generate the
SMT files that will be run by the Z3Tester. The purpose of this
module is to debug both MadamASTra and Z3.
"""

import argparse
from formula_generator import get_sat_z3_formulas, get_unsat_z3_formula, wrap_formula
from c_printer import print_title, print_content, print_warning, print_success

def add_parser(parser: argparse.ArgumentParser) -> None:
    '''
    add the parser for the log command
    '''
    parser.set_defaults(run_mode="log")
    parser.set_defaults(run_method=run)
    parser.add_argument("word1", type=str, help="the first word")
    parser.add_argument("word2", type=str, help="the second word")
    parser.add_argument("-s", "-solver",
                        type=str,
                        default="z3str3",
                        help="the solver to use. default: z3str3")
    parser.add_argument("-m", "--mode",
                        type=str,
                        default="sat",
                        help="the mode to use. default: sat")
    parser.add_argument("-f", "--file", type=str, help="the file to write the SMT formula to")
    parser.add_argument("--seed", type=int, help="the seed to use for the unsat mode")


def run(args: argparse.Namespace) -> None:
    '''
    generates SMT files that contain the formulas induced by word1 and word2.
    These files can be used to debug Z3.
    '''
    print_title("generating SMT files")

    # generate formulas depending on the mode
    if args.mode == "sat":
        formulas, _ = get_sat_z3_formulas(args.word1, args.word2)
    elif args.mode == "unsat":
        formulas, _ = get_unsat_z3_formula(args.word1, args.word2, seed=args.seed)
    else:
        print_warning(f"unknown mode {args.mode}")
        return

    # add the solver and wrap the formulas in a string that can be written to a file
    full_formula = wrap_formula(formulas, args.s)

    print_content(full_formula)

    # write to file
    if args.file:
        file_name = args.file
        file_name = "".join(x for x in file_name if x.isalnum() or x in ["_", "."])
        if not file_name.endswith(".smt2"):
            file_name += ".smt2"
    else:
        file_name = f"{args.word1}_{args.word2}_{args.mode}_{args.s}.smt2"
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(full_formula)

    print_success(f"written to {file_name}")

    print_title("done")
