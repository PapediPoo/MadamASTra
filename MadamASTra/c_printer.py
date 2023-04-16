'''
Responsible for printing consistently over the whole program
'''
import textwrap

BOXWIDTH = 15
INDENT = 3
BOXGUARDS = ("[", "]")
BOXFILL = "_"
INDENTGUARD = "|"

# colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def print_title(content : str) -> None:
    '''prints the title in a big centered block'''
    print(
        HEADER + BOXGUARDS[0]
        + content.upper().center(BOXWIDTH, BOXFILL) +
        BOXGUARDS[1] + ENDC)

def print_warning(content : str) -> None:
    '''prints a warning in a big centered block'''
    print(
        WARNING + BOXGUARDS[0] +
        ("WARNING!" + content).upper().center(BOXWIDTH, BOXFILL) +
        BOXGUARDS[1] + ENDC)

def print_content(content : str) -> None:
    '''prints content with an indent'''
    print(INDENTGUARD + textwrap.indent(content, " " * INDENT))
