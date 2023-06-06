## MadamASTra

MadamASTra is a metamorphic testing tool for the SMT solver Z3 written in python. It encodes the edit distance between two strings into a SMT formula. Due to the strong guarantees of the edit distance, the SMT formulas are guaranteed to be SAT/UNSAT. This allows us to test the SMT solver with a large number of test cases without the need for a test oracle.

<img src="docs/res/MadamASTra1.png" height="300">
<img src="docs/res/MadamASTra2.png" height="300">

Project for the class "Automated Software Testing FS2023"

by Pascal Strebel and Robin Schmidiger

[Project Proposal](docs/ProjectProposal.pdf)

[Progress Report](docs/ProgressReport.pdf)

[Final Report](docs/FinalReport.pdf)

MadamASTra provides a rich CLI interface. For more information, run `python3 MadamASTra --help`.

## Installation

To run MadamASTra, you need to install the following dependencies:
- python3
- Z3
- the python3 libraries found in `requirements.txt`

## Usage

Run `python3 MadamASTra search` to start a basic search to generate 5 pairs of random strings and test them with MadamASTra. The results are printed to the console. If MadamASTra finds a bug in Z3, it will be logged in the `bugs.txt` file.

Run `python3 MadamASTra search --help` to see all available options.

Run `python3 MadamASTra try word1 word2` to test the two words `word1` and `word2` with MadamASTra using all available configurations of solvers and SAT/UNSAT. The results are printed to the console.

## Examples

`python3 MadamASTra search -r 100` will generate 100 random pairs of strings and test them with MadamASTra.

`python3 MadamASTra search -t 60` will set the Z3 timeout to 60 seconds.

`python3 MadamASTra search -r 1000 -p 64` will generate 1000 random pairs of strings and test them with MadamASTra using 64 parallel processes.

`python3 MadamASTra try word1 word2 -s z3str3 -m unsat` will test the two words `word1` and `word2` with MadamASTra using the solver `z3str3` and the SAT/UNSAT mode `unsat`.
