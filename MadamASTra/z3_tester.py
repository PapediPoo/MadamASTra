"""
This module is an abstraction of the Z3 solver. You give it 2 words, and it tries them on Z3.
It also compares the result of Z3 to the expected result.
"""

from formula_generator import get_sat_z3_formulas, get_unsat_z3_formula, wrap_formula
from z3_driver import Z3Driver
from c_printer import print_content, print_warning, print_summary

class Z3Tester(object):
    '''
    Given two words, this class generates SMT formulas for them and tries them on Z3.
    '''
    def __init__(self, verbose=False, timeout=5) -> None:
        self.z3_driver = Z3Driver(verbose, timeout)
        self.error_log = []

    def test(self, word1, word2, mode_config="sat", solver_config="seq") -> None:
        '''
        1. computes a SMT formula for word1 and word2
        2. tries word1 and word2 on Z3
        3. compares the result of Z3 to the expected result
        4. if Z3 made a mistake, it is logged in error_log
        returns: True if Z3 made a mistake, False otherwise
        '''

        print(f"mode: {mode_config}, solver: {solver_config}")
        if mode_config == "sat":
            generated_z3_formula, _ = get_sat_z3_formulas(word1, word2)
            wrong_response_config = "unsat"
        elif mode_config == "unsat":
            generated_z3_formula = get_unsat_z3_formula(word1, word2)
            wrong_response_config = "sat"
        else:
            raise ValueError("mode_config must be either \"sat\" or \"unsat\"")

        full_input = wrap_formula(generated_z3_formula, solver_config)

        # run Z3
        z3_result = self.z3_driver.run(full_input)

        # check if Z3 made a mistake
        print_content("Z3 Response: " + z3_result)
        if wrong_response_config == z3_result.replace("\n", ""):
            print_warning("Z3 Made a mistake!")
            self.error_log.append((word1, word2, "solver: " + solver_config, "mode: " + mode_config))
            return True
        return False

    def print_errors(self) -> None:
        '''
        saves the error log to "bugs.txt"
        '''
        print_summary(f"Z3 made {len(self.error_log)} mistakes")
        with open("bugs.txt", "a", encoding='utf-8') as f:
            for bug in self.error_log:
                for e in bug:
                    f.write(e + ", ")
                f.write("\n")
        print_content("errors written to \"bugs.txt\"")
