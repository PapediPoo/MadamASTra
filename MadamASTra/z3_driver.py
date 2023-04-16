'''
This module is responsible for abstracting the interaction between Z3 and MadamASTra.
It provides the Z3Driver class, which when given a SMT string runs Z3 and returns the result.
'''

import subprocess
from .CPrinter import print_content, print_warning

class Z3Driver():
    '''
    summary: handles interactions between Z3 and MadamASTra.
    Spawns a process for every requested Z3 formula, 
    waits for the process to complete and returns its result.
    '''
    Z3INDENT = 3

    def __init__(self, verbose=False) -> None:
        self.set_verbose(verbose)

    def set_verbose(self, value : bool):
        '''
        summary: defines the logging behaviour of the driver
        '''
        self.verbose = value

    def run(self, smt_expr : str) -> str:
        '''
        given an SMT expression runs Z3 and returns its findings
        '''
        command = 'echo "' + smt_expr + '" | z3 -in -smt2'
        result = subprocess.run(command, capture_output=True, shell=True, check=False)
        err_decoded = result.stderr.decode()
        if len(err_decoded) > 0:
            print_warning("z3 raised an error")
            if self.verbose:
                print_content(err_decoded)

        result_readable = smt_expr + " is " + result.stdout.decode('utf-8')
        return result_readable
