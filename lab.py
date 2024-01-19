"""
6.1010 Spring '23 Lab 10: Symbolic Algebra
"""

import doctest

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


def token_converter(token):
    # turn token into something useful like num, var
    try:
        float_converter = float(token)
        return Num(float_converter)
    except:
        return Var(token)


def parse(tokens):
    """
    Helper function for expression that takes in token
    and writes out expression, num, var 
    """
    operations = {"+": Add, "-": Sub, "*": Mul, "/": Div, "**": Pow}

    def parse_expression(index):
        if tokens[index] == "(":
            # you take in the index+1 at the operand
            # then input to get the right expression
            # operand index
            # enter recursion
            left, operand_index = parse_expression(index + 1)
            right, next_index = parse_expression(operand_index + 1)
            operation_value = tokens[operand_index]
            class_constructor = operations[operation_value]
            return class_constructor(left, right), next_index + 1  # keep recursing
        else:
            return token_converter(tokens[index]), index + 1

        # construct objects
        # base case

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression


def tokenize(sample):
    """
    Helper function that converts a string into a list of characters
    """
    sample_list = []
    i = 0
    # while loop transfer from smaller container to big container
    while i < len(sample):
        small_string = ""
        # perform string concatenation
        while (
            sample[i] != " " and sample[i] != "(" and sample[i] != ")"
        ):  # impossible to fail or statement
            small_string += sample[i]
            # don't need these if statements
            i += 1
            if i == len(sample):
                break
        # check if it stopped on an empty or parentheses
        if small_string == "":
            if sample[i] != " ":
                sample_list.append(sample[i])
            i += 1  # want to increment cause didn't go inside while loop
        else:
            sample_list.append(small_string)
    return sample_list


def expression(sample_string):
    """
    Function that takes in a string to give a parsed object
    using helper functions tokenize and parse 
    """
    token_list = tokenize(sample_string)
    parsed_obj = parse(token_list)
    return parsed_obj


class Symbol:
    """
    Parent class that BinOp inherits from 
    """
    # Do I need exp and par?
    # what is the correct way to store class attributes for precedence?
    # or does it make more sense to initialize right_parens as True for boolean?
    precedence = 3
    # check this value
    right_parens = False
    left_parens = False

    def __add__(self, other):
        return Add(self, other)

    # self is E1
    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        return Div(other, self)

    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return Pow(other, self)

    # these methods are how + operator works (sees the + sign will call __add__)
    # know E1 is a symbol
    # implement __radd__
    def simplify(self):
        """
        Base case that returns itself 
        """
        return self


class BinOp(Symbol):
    """
    Binary Operation class that inherits from Symbol 
    """
   
    def __init__(self, left, right):
        """
        Initializer.  Store an instance variable called `left` and 'right', 
        containing the value passed in to the initializer.
        """

        if isinstance(left, int) or isinstance(left, float):
            self.left = Num(left)
        elif isinstance(left, str):
            self.left = Var(left)
        else:
            self.left = left

        if isinstance(right, int) or isinstance(right, float):
            self.right = Num(right)
        elif isinstance(right, str):
            self.right = Var(right)
        else:
            self.right = right
            # only setting it to a variable if it is a string
        # self.left and self.right will be single values


    def __str__(self):
        if self.left.precedence < self.precedence or (
            self.left.precedence <= self.precedence and self.left_parens
        ):
            left = "(" + str(self.left) + ")"

        else:
            left = str(self.left)

        if self.right.precedence < self.precedence or (
            self.precedence == self.right.precedence and self.right_parens
        ):
            right = "(" + str(self.right) + ")"
        else:
            right = str(self.right)
        return left + " " + self.operation + " " + right
       

   
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"

    # is the parenthesize thing a concern for __repr__ or only for __str__?
    # need to get the class name of the operation and left and right values
    # we need to call Add, Mul, Sub, Div
    def eval(self, mapping):
        left = self.left.eval(mapping)  # class method so default is to self
        right = self.right.eval(mapping)
        return self.func(left, right)

    def helper(self):
        left = self.left
        right = self.right
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(self.func(left.n, right.n))
        else:
            return self.func(left, right)  # unsimplified version

    # taking two symbols, left and right and does simplification of them
    # origin of your error is that you want to create an object rather than mutating
    # you are getting recursion error because of your base cases not going to base case
    def __eq__(self, other):
        """
        Checks if two operations are equal 
        """
        if type(other) is type(self):
            return self.left == other.left and self.right == other.right
        else:
            return False  # is this the correct way to do the input?
        # type isn't just float, string, int, can also return class
        # isinstance works on any parent class, type gives the lowest level class
        # should check for the structure to determine equality


class Add(BinOp):
    """
    Addition class that inherits from BinOp
    """
    operation = "+"
    precedence = 1
    right_parens = False
    # make a lambda function
    func = lambda self, x, y: x + y

    def deriv(self, variable):
        left = self.left.deriv(variable)
        right = self.right.deriv(variable)
        return left + right

    def simplify(self):
        """
        Simplifies for addition
        """
        left = self.left.simplify()
        right = self.right.simplify()
        if left == Num(0):
            return right
        if right == Num(0):
            return left
        else:
            return (left + right).helper()

  
    # is this the correct way to write the lambda function for deriv?
    # class method input should be self

    # should work for any type of symbol, not for specific subclass
    # any two numbers or var


# am I putting it in the right place and is it even correct?
class Sub(BinOp):
    """
    Subtraction class that inherits from BinOp 
    """
    operation = "-"
    precedence = 1
    right_parens = True
    func = lambda self, x, y: x - y

    def deriv(self, variable):
        left = self.left.deriv(variable)
        right = self.right.deriv(variable)
        return left - right

    def simplify(self):
        """
        Simplifies for subtraction
        """
        left = self.left.simplify()
        right = self.right.simplify()
        if right == Num(0):
            return left
        else:
            return (left - right).helper()

   
    # is this the correct way to write lambda for simplify?


class Mul(BinOp):
    """
    Multiplication class that inherits from BinOp 
    """
    operation = "*"
    precedence = 2
    right_parens = False
    func = lambda self, x, y: x * y

    def deriv(self, x):
        return self.left * self.right.deriv(x) + self.left.deriv(x) * self.right
        # will give issue with type checking
        # implement deriv in every sub class

    def simplify(self):
        """
        Simplifies for multiplication 
        """
        left = self.left.simplify()
        right = self.right.simplify()
        if right == Num(1):
            return left
        if left == Num(1):
            return right
        if left == Num(0) or right == Num(0):
            return Num(0)
        else:
            return (left * right).helper()

   
    # how do I handle the two simplify cases under Mul?


class Div(BinOp):
    operation = "/"
    precedence = 2
    right_parens = True
    func = lambda self, x, y: x / y

    def deriv(self, x):
        return (self.right * self.left.deriv(x) - self.left * self.right.deriv(x)) / (
            self.right * self.right
        )

    def simplify(self):
        """
        Simplifies for division case 
        """
        left = self.left.simplify()
        right = self.right.simplify()
        if right == Num(1):
            return left
        if left == Num(0):
            return Num(0)
        else:
            return (left / right).helper()

# maybe you should search up how to write lambda functions yourself


class Pow(BinOp):
    """
    Power class that inherits from BinOp 
    """
    operation = "**"
    precedence = 3
    right_parens = False
    left_parens = True
    func = lambda self, x, y: x**y

    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        if right == Num(0):
            return Num(1)
        if right == Num(1):
            return left
        if left == Num(0) and not isinstance(right, Num):
            return Num(0)
        if left == Num(0) and (isinstance(right, Num) and right.n > 0):
            return Num(0)
        else:
            return left**right


    def deriv(self, x):
        """
        Takes derivative for power case """
        if isinstance(self.right, Num):
            return self.right * (self.left ** (self.right - 1)) * self.left.deriv(x)
        else:
            raise TypeError

    # can we assume that the input will follow the desired order x**y?


class Var(Symbol):
    """
    Variable class that inherits from Symbol 
    """
    precedence = 10

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return str(self.name)

    # is doing str necessary or can you just call self.name?
    def __repr__(self):
        return f"Var('{self.name}')"

    def eval(self, mapping):
        if self.name in mapping.keys():
            return mapping[self.name]
        else:
            raise NameError

    def deriv(self, variable):
        """
        Takes the base case derivative for variables """
        if self.name == variable:
            return Num(1)
        else:
            return Num(0)

    def __eq__(self, other):
        """
        Checks if variables are equal 
        """
        if isinstance(other, Var):
            return bool(self.name==other.name)
            
        else:
            return False


class Num(Symbol):
    """
    Number class that inherits from Symbol 
    """
    precedence = 10

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"

    def eval(self, mapping):
        return self.n

    def deriv(self, variable):
        return Num(0)

    def __eq__(self, other):
        if isinstance(other, Num):
            return bool(self.n == other.n)
        else:
            return False


# implement the eval in num and var and this is the base case

if __name__ == "__main__":
    sample="(cat (dog (tomato)))"
    print(tokenize(sample))

   
