import random
import re
import os

# Bookkeeping over multiple calls of compute_edit_distance:
n_int_consts, n_str_consts, consts_to_vals = 0, 0, {}

insert_in_smt = "(define-fun insert ((to_insert String) (index Int) (source String)) String\
                    (ite\
                        (and (>= index 0) (<= index (str.len source)))\
                        (str.++ (str.substr source 0 index) to_insert (str.substr source index (str.len source)))\
                        source\
                    )\
                )"
# insert a b c -> insert a at position b in c 
# (e.g. insert "h" 0 "allo" -> "hallo")

remove_in_smt = "(define-fun remove ((index Int) (source String)) String\
                    (ite\
                        (and (>= index 0) (< index (str.len source)))\
                        (str.++ (str.substr source 0 index) (str.substr source (+ index 1) (str.len source)))\
                        source\
                    )\
                )"
# remove a b -> remove character at position a in b 
# (e.g. remove 0 "hallo" -> "allo")

replace_in_smt = "(define-fun replace ((to_insert String) (index Int) (source String)) String\
                    (ite\
                        (and (>= index 0) (< index (str.len source)))\
                        (str.++ (str.substr source 0 index) to_insert (str.substr source (+ index 1) (str.len source)))\
                        source\
                    )\
                )"
# replace a b c -> replace character at position b with a in c 
# (e.g. replace "f" 0 "boo" -> "foo")

# You can also debug via (simplify (replace r 2 (replace a 1 (replace b 0 "foo"))))

def get_formula_for_checking_operator_definitions():
     formula = [
            "(assert (= (insert \"a\" 0 \"\") \"a\"))",
            "(assert (= (insert \"a\" 1 \"\") \"\"))",
            "(assert (= (insert \"a\" -1 \"\") \"\"))",
            "(assert (= (insert \"a\" 0 \"b\") \"ab\"))",
            "(assert (= (insert \"a\" 1 \"b\") \"ba\"))",
            "(assert (= (insert \"a\" 2 \"b\") \"b\"))",
            "(assert (= (insert \"a\" -1 \"b\") \"b\"))",
            "(assert (= (insert \"b\" 1 \"a\") \"ab\"))",
            "(assert (= (insert \"b\" -242 \"foo\") \"foo\"))",
            "(assert (= (insert \"b\" 0 \"foo\") \"bfoo\"))",
            "(assert (= (insert \"b\" 1 \"foo\") \"fboo\"))",
            "(assert (= (insert \"b\" 2 \"foo\") \"fobo\"))",
            "(assert (= (insert \"b\" 3 \"foo\") \"foob\"))",

            "(assert (= (remove 0 \"a\") \"\"))",
            "(assert (= (remove 1 \"a\") \"a\"))",
            "(assert (= (remove -1 \"a\") \"a\"))",
            "(assert (= (remove -1 \"ab\") \"ab\"))",
            "(assert (= (remove 0 \"ab\") \"b\"))",
            "(assert (= (remove 1 \"ab\") \"a\"))",
            "(assert (= (remove 2 \"ab\") \"ab\"))",
            "(assert (= (remove -242 \"foo\") \"foo\"))",
            "(assert (= (remove 0 \"foo\") \"oo\"))",
            "(assert (= (remove 1 \"foo\") \"fo\"))",
            "(assert (= (remove 2 \"foo\") \"fo\"))",

            "(assert (= (replace \"b\" 0 \"a\") \"b\"))",
            "(assert (= (replace \"b\" 1 \"a\") \"a\"))",
            "(assert (= (replace \"b\" -1 \"a\") \"a\"))",
            "(assert (= (replace \"a\" 0 \"ab\") \"ab\"))",
            "(assert (= (replace \"a\" 1 \"ab\") \"aa\"))",
            "(assert (= (replace \"b\" 1 \"ab\") \"ab\"))",
            "(assert (= (replace \"b\" -242 \"foo\") \"foo\"))",
            "(assert (= (replace \"b\" 0 \"foo\") \"boo\"))",
            "(assert (= (replace \"b\" 1 \"foo\") \"fbo\"))",
            "(assert (= (replace \"b\" 2 \"foo\") \"fob\"))"
     ]
     full_input = wrap_formula(formula)
     return full_input


# Basic DP algorithm that computes the minimum edit distance to transform s1 into s2
def just_compute_edit_distance(s1 : str, s2 : str) -> int:
    
    dp = [[0 for x in range(len(s1) + 1)] for x in range(len(s2) + 1)]

    # Initialization:
    for i in range(len(s1) + 1):
        dp[0][i] = i
    for j in range(len(s2) + 1):
        dp[j][0] = j

    # Recursion:
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i-1] == s2[j-1]: # do nothing
                dp[j][i] = dp[j-1][i-1]
            else:
                min_dist = min([dp[j][i-1], dp[j-1][i], dp[j-1][i-1]])
                dp[j][i] = min_dist + 1
    
    return dp[len(s2)][len(s1)]

# Basic DP algorithm that computes the minimum edit distance to transform s1 into s2,
# while building a corresponding SMT-formula on the go.
def compute_edit_distance_and_generate_formula(s1 : str, s2 : str) -> str:
    
    global n_int_consts, n_str_consts, consts_to_vals
    # Replaces constant values (e.g. 0, "a") in the formula with unique variables (e.g. int_const_0, str_const_0),
    # stores this information in consts_to_vals.

    dp = [[0 for x in range(len(s1) + 1)] for x in range(len(s2) + 1)]
    formulas = [["" for x in range(len(s1) + 1)] for x in range(len(s2) + 1)]
    n_removals = [[0 for x in range(len(s1) + 1)] for x in range(len(s2) + 1)] # needed for computing indeces
    n_insertions = [[0 for x in range(len(s1) + 1)] for x in range(len(s2) + 1)] # needed for computing indeces

    # Initialization:
    formulas[0][0] = "\"" + s1 + "\""
    for i in range(len(s1) + 1):
        dp[0][i] = i
        if i > 0:
            formulas[0][i] = "(remove int_const_" + str(n_int_consts) + " " + formulas[0][i-1] + ")"
            consts_to_vals["int_const_" + str(n_int_consts)] = "0"
            n_int_consts += 1
            n_removals[0][i] = n_removals[0][i-1] + 1
    for j in range(len(s2) + 1):
        dp[j][0] = j
        if j > 0:
            formulas[j][0] = "(insert str_const_" + str(n_str_consts)  + " int_const_" + str(n_str_consts) + " " + formulas[j-1][0] + ")"
            consts_to_vals["str_const_" + str(n_str_consts)] = s2[j-1]
            n_str_consts += 1
            consts_to_vals["int_const_" + str(n_int_consts)] = str(j-1)
            n_int_consts += 1
            n_insertions[j][0] = n_insertions[j-1][0] + 1

    # Recursion:
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i-1] == s2[j-1]: # do nothing
                dp[j][i] = dp[j-1][i-1]
                formulas[j][i] = formulas[j-1][i-1]
                n_removals[j][i] = n_removals[j-1][i-1]
                n_insertions[j][i] = n_insertions[j-1][i-1]
            else:
                min_dist = min([dp[j][i-1], dp[j-1][i], dp[j-1][i-1]])
                dp[j][i] = min_dist + 1
                if min_dist == dp[j-1][i]: # insert
                    formulas[j][i] = "(insert str_const_" + str(n_str_consts) + " int_const_" + str(n_int_consts) + " " + formulas[j-1][i] + ")"
                    consts_to_vals["str_const_" + str(n_str_consts)] = s2[j-1]
                    n_str_consts += 1
                    consts_to_vals["int_const_" + str(n_int_consts)] = str(i - n_removals[j-1][i] + n_insertions[j-1][i])
                    n_int_consts += 1
                    n_removals[j][i] = n_removals[j-1][i]
                    n_insertions[j][i] = n_insertions[j-1][i] + 1
                elif min_dist == dp[j][i-1]: # remove
                    formulas[j][i] = "(remove int_const_" + str(n_int_consts) + " " + formulas[j][i-1] + ")"
                    consts_to_vals["int_const_" + str(n_int_consts)] = str(i - n_removals[j][i-1] + n_insertions[j][i-1] - 1)
                    n_int_consts += 1
                    n_removals[j][i] = n_removals[j][i-1] + 1
                    n_insertions[j][i] = n_insertions[j][i-1] 
                else: # replace
                    formulas[j][i] = "(replace str_const_" + str(n_str_consts) + " int_const_" + str(n_int_consts) + " " + formulas[j-1][i-1] + ")"
                    consts_to_vals["str_const_" + str(n_str_consts)] = s2[j-1]
                    n_str_consts += 1
                    consts_to_vals["int_const_" + str(n_int_consts)] = str(i - n_removals[j-1][i] + n_insertions[j-1][i])
                    n_int_consts += 1
                    n_removals[j][i] = n_removals[j-1][i-1]
                    n_insertions[j][i] = n_insertions[j-1][i-1]

    return "(assert (= " + formulas[len(s2)][len(s1)] + " \"" + s2 + "\"))"

# Returns SMT formulas using insert, remove and replace to get from s1 to s2.
# generated_z3_formula is of the form "(assert (= (replace str_const_13 int_const_24 (replace str_const_11 int_const_20 (replace str_const_8 int_const_16 "foo"))) "bar"))"
# -> it is intended to be used to stress-test Z3 
# (note that all the constant definitions are included as well)
# reference_z3_formula is of the form "(assert (= (replace r 2 (replace a 1 (replace b 0 "foo"))) "bar"))"
# -> it is intended to check the correctness of the series of inserts/removes/replacements that we computed
# Both formulas are SAT by construction.
def get_sat_z3_formulas(s1 : str, s2 : str):
    # TODO: Use Z3 to verify that reference_z3_formula evaluates to true (i.e., is SAT)
    # TODO: Maybe replace some occurrences of "int_const_x" and/or "str_const_y" 
    #       in generated_z3_formula with their corresponding values from consts_to_vals,
    #       because otherwise Z3 may take veeeery long and eventually return unknown.
    #       => How much of our rewriting do we have to "expose" for Z3 to succeed?
    z3_expression = compute_edit_distance_and_generate_formula(s1, s2)
    generated_z3_formula = z3_expression
    reference_z3_formula = z3_expression
    for const in re.findall("int_const_\d*", z3_expression):
        generated_z3_formula = "(declare-const " + const + " Int)\n" + generated_z3_formula
        reference_z3_formula = reference_z3_formula.replace(const, consts_to_vals[const])
    for const in re.findall("str_const_\d*", z3_expression):
        generated_z3_formula = "(declare-const " + const + " String)\n" + "(assert (= (str.len " + const + ") 1))\n" + generated_z3_formula # declare string constant and enforce that is has length 1
        reference_z3_formula = reference_z3_formula.replace(const, "\"" + consts_to_vals[const] + "\"") # surround string with " "
    return generated_z3_formula, reference_z3_formula

# Returns an SMT formula using insert, remove and replace that make it IMPOSSIBLE to get from s1 to s2.
# generated_z3_formula is of the form "(assert (= (replace str_const_13 int_const_24 (replace str_const_11 int_const_20 "foo")) "bar"))"
# -> it is intended to be used to stress-test Z3 
# (note that all the constant definitions are included as well)
# The formula is UNSAT by construction, as it uses less insert/remove/replace operations than would be minimally needed to get from s1 to s2.
def get_unsat_z3_formula(s1 : str, s2 : str, seed=None) -> str:
    edit_distance = just_compute_edit_distance(s1, s2)
    formula = "\"" + s1 + "\""
    declarations = ""
    constraints = ""
    for i in range(edit_distance - 1): # by adding edit_distance - 1 insert/remove/replace operations we ensure that the formula will be UNSAT
        if seed:
            random.seed(seed)
        random_number = random.randint(0,2)
        if random_number == 1: # insert
            formula = "(insert str_const_" + str(i) + " int_const_" + str(i) + " " + formula + ")"
            declarations += "(declare-const int_const_" + str(i) + " Int)\n"
            declarations += "(declare-const str_const_" + str(i) + " String)\n"
            constraints += "(assert (= (str.len str_const_" + str(i) + ") 1))\n"
        elif random_number == 0: # remove
            formula = "(remove int_const_" + str(i) + " " + formula + ")"
            declarations += "(declare-const int_const_" + str(i) + " Int)\n"
        else: # replace
            formula = "(replace str_const_" + str(i) + " int_const_" + str(i) + " " + formula + ")"
            declarations += "(declare-const int_const_" + str(i) + " Int)\n"
            declarations += "(declare-const str_const_" + str(i) + " String)\n"
            constraints += "(assert (= (str.len str_const_" + str(i) + ") 1))\n"
    formula = "(assert (= " + formula + " \"" + s2 + "\"))"
    generated_z3_formula = declarations + "\n" + constraints + "\n" + formula
    return generated_z3_formula


def wrap_formula(formula : str, string_solver : str = "seq") -> str:
    '''
    Wraps a formula into the definitions for insert, remove and replace and adds check-sat at the end
    '''
    full_input = ""
    if string_solver == "z3str3":
        full_input += "(set-option :smt.string_solver z3str3) ; set the string solver to be the z3str3 solver\n"
    elif string_solver == "seq":
        full_input += "(set-option :smt.string_solver seq) ; set the string solver to be the seq solver (default)\n"
    else:
        print("ERROR: Invalid string solver.")
        raise ValueError("Invalid string solver. Only z3str3 and seq are supported.")
    # TODO: Add some further options, e.g. max compute time or max memory
    full_input += insert_in_smt + "\n"
    full_input += remove_in_smt + "\n"
    full_input += replace_in_smt + "\n"
    full_input += formula + "\n"
    full_input += "(check-sat)\n"
    return full_input