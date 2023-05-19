'''
Responsible for printing consistently over the whole program
'''
import textwrap
from colorama import Fore, Style

BOXWIDTH = 20
INDENT = 3
BOXGUARDS = ("[ ", " ]")
BOXFILL = " "
INDENTGUARD = "|"

# colors
HEADER = Fore.MAGENTA
OKBLUE = Fore.BLUE
OKCCYAN = Fore.CYAN
OKGREEN = Fore.GREEN
OKYELLOW = Fore.YELLOW
WARNING = Fore.YELLOW
FAIL = Fore.RED
ENDC = Fore.RESET
BOLD = Style.BRIGHT
UNDERLINE = Style.DIM


def print_title(content: str) -> None:
    '''prints the title in a big centered block'''
    print(
        HEADER
        + BOXGUARDS[0]
        + content.upper().center(BOXWIDTH, BOXFILL)
        + BOXGUARDS[1] + ENDC)

def print_warning(content: str) -> None:
    '''prints a warning in a big centered block'''
    print(
        WARNING
        + BOXGUARDS[0]
        + ("WARNING! " + content).upper().center(BOXWIDTH, BOXFILL)
        + BOXGUARDS[1] + ENDC)

def print_success(content: str) -> None:
    '''prints a success message in a big centered block'''
    print(
        OKGREEN
        + BOXGUARDS[0]
        + ("SUCCESS! " + content).upper().center(BOXWIDTH, BOXFILL)
        + BOXGUARDS[1] + ENDC)

def print_content(content: str) -> None:
    '''prints content with an indent'''
    print(
        INDENTGUARD
        + textwrap.indent(content, " " * INDENT))
