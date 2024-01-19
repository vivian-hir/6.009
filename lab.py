"""
6.1010 Spring '23 Lab 12: LISP Interpreter Part 2
"""
#!/usr/bin/env python3
import sys

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


class Nil:
    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, Nil):
            return True

        return False


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

    def lookup(self, var, val):
        if var in self.frame_dict:  # base case
            self.dictionary_setup(var, val)
            return val
        else:
            if self.parent is None:  # recursive case
                raise SchemeNameError  # raise if there's no parent
            return self.parent.lookup(var, val)  # keep looking inside

    # do I need to write an additional thing to check if variable is sequence of characters?


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


def equal(args):
    if args is None:
        raise SchemeEvaluationError  # not sure if this is the correct way
    elif len(args) == 1:
        return True  # I don't know if the above base cases are necessary?
    else:
        result = args[0]
        if all(item == result for item in args):
            return True
        return False


def decrease(args):
    if args is None:
        raise SchemeEvaluationError  # not sure if this is the correct way
    elif len(args) == 1:
        return True  # I don't know if the above base cases are necessary?
    else:
        if all(args[i + 1] < args[i] for i in range(len(args) - 1)):
            return True
        return False


def increase(args):
    if args is None:
        raise SchemeEvaluationError  # not sure if this is the correct way
    elif len(args) == 1:
        return True  # I don't know if the above base cases are necessary?
    else:
        if all(args[i + 1] > args[i] for i in range(len(args) - 1)):
            return True
        return False


def nonincreasing(args):
    if args is None:
        raise SchemeEvaluationError  # not sure if this is the correct way
    elif len(args) == 1:
        return True  # I don't know if the above base cases are necessary?
    else:
        if all(args[i] >= args[i + 1] for i in range(len(args) - 1)):
            return True
        return False


def nondecreasing(args):
    if args is None:
        raise SchemeEvaluationError  # not sure if this is the correct way
    elif len(args) == 1:
        return True  # I don't know if the above base cases are necessary?
    else:
        if all(args[i] <= args[i + 1] for i in range(len(args) - 1)):
            return True
        return False


def not_method(args):
    if len(args) == 1:
        return not args[0]
    else:
        raise SchemeEvaluationError


def car(args):
    if len(args) != 1:
        raise SchemeEvaluationError
    obj = args[0]
    if not isinstance(obj, Pair):
        raise SchemeEvaluationError
    return obj.car


def cdr(args):
    if len(args) != 1:
        raise SchemeEvaluationError
    obj = args[0]
    if not isinstance(obj, Pair):
        raise SchemeEvaluationError
    return obj.cdr


def list_boolean(args):
    """ 
    Takes in an arbitrary object and checks if it is a type scheme list 
    """
    # check args length
    # then retrieve parameters from args
    # never use args again and use object
    if len(args) != 1:
        raise SchemeEvaluationError
    obj = args[0]
    if isinstance(obj, Nil) or obj == []:
        return True  # this case is not passing
    elif isinstance(obj, Pair) and list_boolean([obj.cdr]):
        return True
    else:
        return False


def length(args):  # args takes in a list though not an object ...?
    """
    Takes in a list and finds the length of the linked list 
    """
    counter = 0
    if len(args) != 1:
        raise SchemeEvaluationError
    obj = args[0]
    boolean_value = list_boolean(args)
    if not boolean_value:
        raise SchemeEvaluationError  # if object is not a linked list
    while not isinstance(obj, Nil):
        counter += 1
        obj = obj.cdr
    return counter


def list_ref(args):
    """
    Returns the value based on the provided index for the scheme list 
    """
    if len(args) != 2:
        raise SchemeEvaluationError  # I am not sure if this is correct
    obj = args[0]
    index = args[1]
    boolean_value = list_boolean([args[0]])
    if isinstance(obj, Pair) and not boolean_value:
        if index == 0:
            return obj.car
        raise SchemeEvaluationError
    elif isinstance(obj, Pair) and boolean_value:
        if index == 0:
            return obj.car
        else:
            return list_ref((obj.cdr, index - 1))
    else:
        raise SchemeEvaluationError


def append(args):  # [ scheme lists ]
    """
    Appends values to a scheme list 
    """
    args = [arg for arg in args if not isinstance(arg, Nil)]  # don't want Nil
    for i in range(len(args)):
        if list_boolean([args[i]]) is False:
            raise SchemeEvaluationError
    if len(args) == 0:
        return Nil()
    elif len(args) == 1:  # you need to use the helper function length
        return copy(
            args[0]
        )  # do I need to call helper functions like cons and list_func?
        # it returns the pair object, not sure if correct
    else:
        first_list = copy(args[0])
        other_list = append(args[1:])
        ptr = first_list  # need a pointer variable
        while not isinstance(ptr.cdr, Nil):  # keep doing until the cdr is Nil
            # if isinstance(ptr, Nil):
            ptr = ptr.cdr  # reassign the pointer
        ptr.cdr = other_list  # once we break we reassign the Nil cdr to the other_list
        return first_list
    # you can't be doing recursion if you aren't doing base case and a recursive case


def copy(lst):
    """
    Makes a copy of the scheme list using the car cdr format 
    """
    if isinstance(lst, Nil):
        return Nil()
    elif isinstance(lst.cdr, Nil):
        return Pair(lst.car, Nil())
    else:
        return Pair(lst.car, copy(lst.cdr))
    # use while loop for accessing nil


def cons(args):
    """
    Constructs a pair object with car and cdr 
    """
    if len(args) != 2:
        raise SchemeEvaluationError
    new_pair = Pair(args[0], args[1])
    # I think the error is coming from nil being string, can't be concatenated
    # should I therefore take care of that in the class methods?
    return new_pair


def list_func(args):
    """
    Makes a list function using Pair ojbect 
    """
    if len(args) == 0:
        return Nil()
    elif len(args) == 1:
        return Pair(args[0], Nil())
    else:
        return Pair(args[0], list_func(args[1:]))


def map_func(args):
    """
    Performs functions on each value in the scheme list 
    """
    func = args[0]
    lst = args[1]
    new_list = []
    ptr = lst

    if not list_boolean([lst]):
        raise SchemeEvaluationError

    if isinstance(ptr, Nil):
        return Nil()
    while not isinstance(ptr, Nil):
        value = func([ptr.car])  # wouldn't I have to call evaluate or something then?
        new_list.append(value)
        ptr = ptr.cdr
    scheme_list = list_func(
        new_list
    )  # maybe it can't take in these parameters correctly
    return scheme_list
    # could I use a for loop instead of doing recursion?


def filter_func(args):
    """
    Returns a list of values that satisfy the boolean statement 
    """
    func = args[0]
    lst = args[1]
    new_list = []
    ptr = lst
    if not list_boolean([lst]):
        raise SchemeEvaluationError

    if isinstance(ptr, Nil):
        return Nil()
    while not isinstance(ptr, Nil):
        value = func([ptr.car])
        if value is True:  # wouldn't I have to call evaluate or something then?
            new_list.append(ptr.car)
        ptr = ptr.cdr
    scheme_list = list_func(
        new_list
    )  # maybe it can't take in these parameters correctly
    return scheme_list


def reduce_func(args):
    """
    Returns the final value after calling the function on the list 
    """
    func = args[0]
    lst = args[1]
    initial = args[2]
    ptr = lst
    if not list_boolean([lst]):
        raise SchemeEvaluationError

    if isinstance(lst, Nil):
        return initial  # smallest input possible

    else:
        first_arg = lst.car
        other_arg = lst.cdr
        evaluate_first = func([initial, first_arg])  # at least one element is recursive
        evaluate_second = reduce_func(
            [func, other_arg, evaluate_first]
        )  # handle rest of list using recursion
        return evaluate_second
        # if I put it here wouldn't it reset all the time?


def begin(args):
    # every args gets evaluated
    # built in vs special form (special form cannot evaluate x)
    return args[-1]


def evaluate_file(file_name, frame=None):
    file = open(file_name, mode="r")
    read_content = file.read()  # read processes it and converts it to a string
    tokenized = tokenize(read_content)
    parsed = parse(tokenized)
    return evaluate(parsed, frame)


scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mul,
    "/": div,
    "<": increase,
    ">": decrease,
    "<=": nondecreasing,
    ">=": nonincreasing,
    "equal?": equal,
    "not": not_method,  # how can I just do a lambda function without getting the error?
    "#t": True,
    "#f": False,
    "car": car,
    "cdr": cdr,
    "nil": Nil(),  # is this the right way to do the empty list for nil?
    "list?": list_boolean,
    "length": length,
    "list-ref": list_ref,
    "append": append,
    "cons": cons,
    "list": list_func,
    "map": map_func,
    "filter": filter_func,
    "reduce": reduce_func,
    "begin": begin,
}


class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
        # may not need that variable

    def __str__(self):
        return "(" + " " + str(self.car) + " " + str(self.cdr) + " " + ")"


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
        if len(tree) == 0:
            raise SchemeEvaluationError
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
        elif tree[0] == "cons":
            if len(tree[1:]) != 2:
                raise SchemeEvaluationError
            new_list = Pair(evaluate(tree[1], frame), evaluate(tree[2], frame))
            return new_list
        elif tree[0] == "if":
            pred = evaluate(tree[1], frame)
            if pred is True:
                return evaluate(tree[2], frame)
            else:
                return evaluate(tree[3], frame)
        elif tree[0] == "and":
            for val in tree[1:]:
                if evaluate(val, frame) is False:
                    return False
            return True
        elif tree[0] == "or":
            for val in tree[1:]:
                if evaluate(val, frame) is True:
                    return True
            return False
        elif tree[0] == "del":
            variable = tree[1]
            if (
                variable not in frame.frame_dict
            ):  # don't think this is the correct way to do it
                raise SchemeNameError
            value = frame.getter(variable)
            del frame.frame_dict[variable]
            return value
        elif tree[0] == "let":
            variable_list = tree[1]
            function = tree[2]
            new_frame = Frame(
                frame
            )  # would I have to keep changing this under the for loop or just put it here?
            for var, val in variable_list:
                new_val = evaluate(val, frame)
                new_frame.dictionary_setup(var, new_val)
            return evaluate(function, new_frame)
        elif tree[0] == "set!":
            variable = tree[1]
            expression = tree[2]
            value = evaluate(expression, frame)
            # would I do some for loop or while loop?
            frame.lookup(variable, value)
            return value

        else:
            func = evaluate(
                tree[0], frame
            )  # should I also do other if statements for evaluate tree[0] frame???
            if isinstance(func, (int, float, Nil)):
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

    for i in range(1, len(sys.argv)):
        evaluate_file(i)

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
