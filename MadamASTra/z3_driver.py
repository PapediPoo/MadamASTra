'''
This module is responsible for abstracting the interaction between Z3 and MadamASTra.
It provides the Z3Driver class, which when given a SMT string runs Z3 and returns the result.
It does not have any knowledge of the SMT language, and does not know how to generate SMT formulas.
It just handles the process of running Z3.
'''

import subprocess
from c_printer import print_content, print_warning

class Z3Driver():
    '''
    summary: handles interactions between Z3 and MadamASTra.
    Spawns a process for every requested Z3 formula,
    waits for the process to complete and returns its result.
    '''

    def __init__(self, verbose=False, timeout=5) -> None:
        self.set_verbose(verbose)
        self.set_timeout(timeout)

    def set_verbose(self, value: bool) -> None:
        '''
        summary: defines the logging behaviour of the driver
        '''
        self.verbose = value

    def set_timeout(self, value: int) -> None:
        '''
        summary: defines the max amount of time that Z3 is allowed to take for finish
        '''
        self.timeout = value

    def run(self, smt_expr: str) -> str:
        '''
        summary: given an SMT expression runs Z3 and returns its findings
        '''
        command = 'echo \'' + smt_expr.replace("'", "\"") + f"\' | z3 -in -smt2 -T:{self.timeout}"
        print(command)
        result = subprocess.run(command, capture_output=True, shell=True, check=False)
        err_decoded = result.stderr.decode()
        if len(err_decoded) > 0:
            print_warning("z3 raised an error")
            if self.verbose:
                print_content(err_decoded)

        result_readable = result.stdout.decode('utf-8')
        return result_readable
