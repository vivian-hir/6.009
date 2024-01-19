"""
6.1010 Spring '23 Lab 11: LISP Interpreter Part 1
"""
#!/usr/bin/env python3

import sys
import doctest

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def remove_comments(source):
    """
    Helper function for tokenize that takes in a string
    and removes characters after the semicolons (commments)
    """
    new_list = []
    new_string = ""
    remove_n = source.split("\n")
    for line in remove_n:
        input = line.split(";")[0]
        new_list.append(input)
    for item in new_list:
        new_string += item
        new_string += "\n"
    return new_string

    # for char in new_string:
    # if char=='(':
    # new_string.replace('(',' ( ')
    # if char==')':
    # new_string.replace(')', ' ) ')
    # for item in new_list:
    # if item!='':
    # new_string+=item


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """

    sample_list = []
    i = 0
    # while loop transfer from smaller container to big container
    # create helper method to get rid of \n and the semicolons (comments)
    # get rid of the extra white space
    new_string = remove_comments(source)
    while i < len(new_string):
        small_string = ""
        # perform string concatenation
        while (  # but I only can do one character
            new_string[i] != " "
            and new_string[i] != "("
            and new_string[i] != ")"
            and new_string[i] != "\n"
        ):  # impossible to fail or statement
            small_string += new_string[i]
            # don't need these if statements
            i += 1
            if i == len(new_string):
                break
        # check if it stopped on an empty or parentheses
        if small_string == "":
            if new_string[i] != " " and new_string[i] != "\n":
                sample_list.append(new_string[i])
            i += 1  # want to increment cause didn't go inside while loop
        else:
            sample_list.append(small_string)
    return sample_list
    # I think that you need to write something more specific for semicolon
    # It has to not append any character after the semicolon
    # Use the /n, not sure how to though


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    left_parens = tokens.count("(")
    right_parens = tokens.count(")")
    # if parens in tokens:
    if left_parens != right_parens:
        raise SchemeSyntaxError
    if "(" in tokens or ")" in tokens:
        if tokens[0] != "(":
            raise SchemeSyntaxError
        if tokens[-1] != ")":
            raise SchemeSyntaxError
        # [bare-name]

    def parse_helper(index):
        big_list = []

        # not is same as and but the loop only runs once
        if tokens[index] == "(":
            # big_list.append(tokens[index+1])
            index += 1
            while index < len(tokens) and tokens[index] != ")":
                parsed_list, index = parse_helper(index)
                big_list.append(parsed_list)
            return big_list, index + 1  # return outside the parentheses
        else:
            return number_or_symbol(tokens[index]), index + 1

    parsed_expression, next_index = parse_helper(0)
    if next_index != len(tokens):
        raise SchemeSyntaxError
    return parsed_expression


######################
# Built-in Functions #
######################
def mul(args):
    """
    Multiplies two numbers. If none, return 0
    """
    if args is None:
        return 0
    elif len(args) == 1:
        return args[0]
    else:
        return args[0] * mul(args[1:])


def div(args):
    """
    Divides two numbers. If none, raise SchemeEvaluationError.
    If there is only one number, then return 1/x
    """
    if args is None:
        raise SchemeEvaluationError
    elif len(args) == 1:
        return 1 / args[0]  # confused between 1/x and recursive call
    else:
        results = args[0]  # initialize the first value
        for item in args[1:]:
            results /= item
        return results

    # recursive helpers separate the two cases


class Frame:
    """
    A class that contains a dictionary with keys as variables and values as numbers
    Also contains a parent frame that acts as the root in the tree
    """

    def __init__(self, parent=None):
        self.frame_dict = {}
        self.parent = parent

        # need to initalize dictionary

    def dictionary_setup(self, var, val):
        self.frame_dict[var] = val

    def getter(self, var):
        if var not in self.frame_dict:
            if self.parent is None:
                raise SchemeNameError  # if it's not in parent at all (checked all the way up)
            return self.parent.getter(var)  # if not check the parent
        return self.frame_dict[var]  # if it is in current

    # do I need to write an additional thing to check if variable is sequence of characters?


scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mul,
    "/": div,
}


class Functions:
    """
    A class that defines a function as something containing variables,
    expression, and the enclosing frame as the parent.
    Contains the call dunder method to call a function and raises
    SchemeEvaluationError if variable length differs from arg length.
    """

    def __init__(self, vars, exp, frame):
        self.vars = vars  # would vars be a list of variables?
        self.exp = exp
        self.frame = frame

    # defining and calling the function are two separate steps
    # inside of evaluate the lambda definition
    def __call__(self, args):
        if len(args) != len(self.vars):
            raise SchemeEvaluationError
        # check if num of arguments equals number of assigned variables
        # for arg in args: #iterate through the arguments
        #     value=evaluate(arg, self.frame) #evaluate each value
        #     value_list.append(value) #add value to a list
        new_frame = Frame(self.frame)  # parent is self.frame
        for i, val in enumerate(args):  # index and value
            new_frame.dictionary_setup(
                self.vars[i], val
            )  # value list and variable list should be same length
        return evaluate(self.exp, new_frame)


##############
# Evaluation #
##############
parent_frame = Frame()
parent_frame.frame_dict = scheme_builtins


def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    # language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    # print(tree)
    if frame is None:
        frame = Frame(parent_frame)
        # initializing a new built in each time you call evaluate

    # scheme_builtins
    if isinstance(tree, (int, float)):
        return tree  # number case
    elif isinstance(tree, str):
        return frame.getter(tree)  # variable case
    elif isinstance(tree, list):
        if tree[0] == "define":
            variable = tree[1]
            if isinstance(variable, list):
                # final_expression=['lambda']
                final_expression = []
                func_name = variable[0]
                var_name = variable[1:]
                expression = tree[2]
                final_expression.append(var_name)
                final_expression.append(expression)
                new_function = Functions(var_name, expression, frame)
                frame.dictionary_setup(func_name, new_function)
                # new_value=evaluate(final_expression, frame)
                # frame.dictionary_setup(func_name, new_value)
                # return new_value
                return new_function
            value = evaluate(tree[2], frame)
            frame.dictionary_setup(variable, value)
            return value
        elif tree[0] == "lambda":
            function = Functions(tree[1], tree[2], frame)
            return function
        else:
            func = evaluate(
                tree[0], frame
            )  # should I also do other if statements for evaluate tree[0] frame???
            if isinstance(func, (int, float)):
                raise SchemeEvaluationError
            arguments = []
            for item in tree[1:]:
                arguments.append(evaluate(item, frame))
            return func(arguments)  # wouldn't this be the case in which

            # if func in

    # call the methods under the frame class in evaluate


def result_and_frame(tree, frame=None):
    """
    Takes in the same arguments as evaluate but returns a tuple of the
    result of evaluate and frame that it was evaluated in

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
        frame: a type of object containing dictionary assigning vars to vals
    """
    if frame is None:
        frame = Frame(parent_frame)
        # how do I avoid repeating things from evaluate? Shouldn't be too much code right?
    return evaluate(tree, frame), frame


def repl(verbose=False):
    """
    Read in a single line of user input, evaluate the expression, and print
    out the result. Repeat until user inputs "QUIT"

    Arguments:
        verbose: optional argument, if True will display tokens and parsed
            expression in addition to more detailed error output.
    """
    import traceback

    _, frame = result_and_frame(["+"])  # make a global frame
    while True:
        input_str = input("in> ")
        if input_str == "QUIT":
            return
        try:
            token_list = tokenize(input_str)
            if verbose:
                print("tokens>", token_list)
            expression = parse(token_list)
            if verbose:
                print("expression>", expression)
            output, frame = result_and_frame(expression, frame)
            print("  out>", output)
        except SchemeError as e:
            if verbose:
                traceback.print_tb(e.__traceback__)
            print("Error>", repr(e))


if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    repl(True)
