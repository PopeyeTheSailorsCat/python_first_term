from abc import ABC, abstractmethod
from task.linalg import inv, dot


#
# class CallableList(list):
#     """
#     Augmentation of built-in list class to allow convenient lt(x=1, y=3)
#     inference.
#     """
#     raise NotImplementedError


class Expr(ABC):
    """
    Base expression class. Constant and Variable classes are inherited from it.
    """

    @abstractmethod
    def __call__(self, **context):
        """
        Call expresion as a function with certain values passed as arguments.

        Parameters
        ----------
        **context : dict
            Arguments to the function.

        Returns
        -------
        float
            Value of expression at context.

        """
        pass

    @abstractmethod
    def d(self, wrt):
        """
        Calculate symbolic derivative with respect to wrt variable.

        Parameters
        ----------
        wrt : Expr
            Differentiate with respect to the variable wrt..

        Returns
        -------
        Expr
            Derivative dExpr/dwrt.

        """

        pass

    def grad(self, wrts):
        """"
        Calculate symbolic gradient with respect to wrts variables.

        Parameters
        ----------
        wrts : List[Expr]
            Differentiate with respect to the variables in wrt list.

        Returns
        -------
        List[Expr]
            Gradient vectordExpr/dwrts.

        """
        res_grad = []
        for elem in wrts:  # We take the derivative for each variable
            res_grad.append(self.d(elem))
        return res_grad
        # raise NotImplementedError

    def __neg__(self):
        """
        Return negative of expression.

        Returns
        -------
        Expr
            -Expr

        """
        return Const(-1) * self

    def __pos__(self):
        """
        Return absolute value.

        Returns
        -------
        Expr
            Absolute value.

        """
        return Power(Power(self, Const(2)), Const(0.5))  # Returning the square root of the square
        # raise NotImplementedError

    def __add__(self, other):
        """
        Sum expressions.

        Parameters
        ----------
        other : Expr
            Expression to add.

        Returns
        -------
        Expr
            Expression + other.

        """
        return Sum(self, other)
        # raise NotImplementedError

    def __sub__(self, other):
        """
        Subtract from expression.

        Parameters
        ----------
        other : Expr
            Expression to subtract.

        Returns
        -------
        Expr
            Expression - other.

        """
        return Sum(self, -other)
        # raise NotImplementedError

    def __mul__(self, other):
        """
        Multiply by expression.

        Parameters
        ----------
        other : Expr
            Expression to add.

        Returns
        -------
        Expr
            Expression * other.

        """
        return Product(self, other)
        # raise NotImplementedError

    def __truediv__(self, other):
        """
        Divide by expression.

        Parameters
        ----------
        other : Expr
            Expression-divisor.

        Returns
        -------
        Expr
            Expression / other.

        """
        return Fraction(self, other)
        # raise NotImplementedError

    def __pow__(self, power, modulo=None):
        """
        Raise to power.

        Parameters
        ----------
        power : Expr
            Expression-exponent.

        Returns
        -------
        Expr
            Expression^power.

        """
        return Power(self, power)
        # raise NotImplementedError


class Var(Expr):
    """
    Variable class to contain symbolic variables ('x', 'y', for example).
    """

    def __init__(self, var):
        self.name = var
        return
        # raise NotImplementedError

    def __call__(self, **context):
        val = context.get(self.name)
        return val
        # raise NotImplementedError

    def d(self, wrt):
        if str(wrt) == self.name:  # If the derivative of this variable is
            return Const(1)
        else:
            return Const(0)

        # raise NotImplementedError

    def __str__(self):
        return self.name
        # raise NotImplementedError


class Const(Expr):
    """
    Const expression
    """

    def __init__(self, const):
        self.value = const
        return
        # raise NotImplementedError

    def __call__(self, **context):
        return self.value
        # raise NotImplementedError

    def d(self, wrt):
        return Const(0)
        # raise NotImplementedError

    def __str__(self):
        return str(self.value)
        # raise NotImplementedError


class BinOp(Expr):
    """
    Base class for a binary operation (a ? b, where ? is an arbitrary binary
    operator).
    """

    def __init__(self, expr1, expr2):
        """
        Instantiate BinOp with left operand and right operand. expr1 ? expr2

        Parameters
        ----------
        expr1 : Expr
            Left operand.
        expr2 : Expr
            Right operand.

        Returns
        -------
        None.

        """
        self.expr1 = expr1  # Storing the received expr
        self.expr2 = expr2

    def __str__(self, op):
        raise NotImplementedError


class Sum(BinOp):
    """
    Summation operator: a + b.
    """

    def __call__(self, **context):
        a = self.expr1(**context)
        b = self.expr2(**context)
        return a + b

    def d(self, wrt):
        return self.expr1.d(wrt) + self.expr2.d(wrt)
        # raise NotImplementedError

    def __str__(self):
        stroka = "(" + str(self.expr1) + "+" + str(self.expr2) + ")"
        return stroka
        # raise NotImplementedError


class Product(BinOp):
    """
    Product operator: a *b
    """

    def __call__(self, **context):
        a = self.expr1(**context)
        b = self.expr2(**context)
        return a * b
        # raise NotImplementedError

    def d(self, wrt):
        return self.expr1.d(wrt) * self.expr2 + self.expr1 * self.expr2.d(wrt)
        # raise NotImplementedError

    def __str__(self):
        stroka = "(" + str(self.expr1) + "*" + str(self.expr2) + ")"
        return stroka
        # raise NotImplementedError


class Fraction(BinOp):
    """
    Division operator: a / b.
    """

    def __call__(self, **context):
        a = self.expr1(**context)
        b = self.expr2(**context)
        return a / b
        # raise NotImplementedError

    def d(self, wrt):
        up = self.expr1.d(wrt) * self.expr2
        also_up = self.expr1 * self.expr2.d(wrt)
        down = self.expr2 ** Const(2)
        return Fraction(Sum(up, -also_up), down)
        # raise NotImplementedError

    def __str__(self):
        stroka = "(" + str(self.expr1) + "/" + str(self.expr2) + ")"
        return stroka
        # raise NotImplementedError


class Power(BinOp):
    """
    Exponentiation operator: a^b
    """

    def __call__(self, **context):
        a = self.expr1(**context)
        b = self.expr2(**context)
        return pow(a, b)
        # raise NotImplementedError

    def d(self, wrt):
        a = self.expr1
        b = self.expr2

        return b * a.d(wrt) * a ** (b - Const(1))
        # raise NotImplementedError

    def __str__(self):
        stroka = "(" + str(self.expr1) + ")^" + str(self.expr2)
        return stroka
        # raise NotImplementedError


def variables(s):
    """
    Transform string with variable names to a list of variables.

    Parameters
    ----------
    s : str
        String with variables names separated by space.

    Returns
    -------
    List[Var]
        List of variables.

    """
    var = s.split()
    out = []
    for elem in var:
        out.append(Var(str(elem)))
    return out
    # raise NotImplementedError


def build_lagrangian(fun, eqs):
    """
    Construct Langrangian function from fun to minimize and eq. constraints.

    Parameters
    ----------
    fun : Expr
        Function to minimize.
    eqs : List[Expr]
        List of Expr function that constitute constraints of type equality.

    Returns
    -------
    Expr and List[Var]
        Langrangian Multipliers Function with a set of new lambda_k variables.

    """
    set_new_var = ""
    for i in range(len(eqs)):  # Creating new variables
        set_new_var += ("lamda_" + str(i + 1) + " ")
    new_var = variables(set_new_var)  # Turning our lambdas into variables
    return_fun = fun
    for i in range(len(new_var)):
        return_fun = return_fun + new_var[i] * eqs[i]
    return return_fun, new_var
    # raise NotImplementedError


def build_jac(fun, wrts):
    """
    Build jacobian from vector-values function (or scalar).

    Parameters
    ----------
    fun : List[Expr] or CallableList
        Some vector-valued functional (for example a gradient of a function).
    wrts : List[Var]
        List of variables that will be used for derivative computations.

    Returns
    -------
    List[List[Expr]] or CallableList
        Jacobian of fun. In case of scalar-valued functions, it is just a
        gradient vector of size 1 x len(wrts). 

    """
    if not isinstance(fun, list):  # if you submitted a single function
        fun = list(fun)

    out = []
    for elem in fun:
        out.append(elem.grad(wrts))

    # raise NotImplementedError
    return out


def inf_norm(expr, value):
    maximum = 0
    for elem in expr:
        res = elem(**value)
        if abs(res) > maximum:
            maximum = res
    return maximum


def newton_raphson(expr, variables, start, threshold=1e-5):
    """
    Multivariate Newton-Raphson method for root finding.

    Parameters
    ----------
    expr : Expr or List[Expr]
        Callable symbolic function, possibly vector-valued.
    variables : List[Var]
        List of variables present in the function.
    start : float or List[float]
        Starting values for variables provided in the same order.
    threshold : float, optional
        Stopping criteria for Newton-Raphson.

    Returns
    -------
    cur : dict
        Variable estimates where expr attains zero.

    """
    funct = []
    if not isinstance(expr, list):  # If you submitted one expr
        funct.append(expr)
    else:
        funct = expr

    my_dict = {str(var): value for var, value in zip(variables, start)}  # Building a dictionary-variable name:value
    x = start
    jac = build_jac(funct, variables)  # Building the Jacobian once

    while abs(inf_norm(funct, my_dict)) >= threshold:  # As long as the infinite norm is greater than the required
        # accuracy

        jab_val = []
        expr_val = []
        for i in range(len(funct)):  # считаем значение якобиана и функций
            jab_line = []
            expr_val.append(funct[i](**my_dict))
            for j in range(len(variables)):
                jab_line.append(jac[i][j](**my_dict))

            jab_val.append(jab_line)
        mul_jab_expr = dot(inv(jab_val), expr_val)  # multiplying the inverse Jacobian with the function vector
        for i in range(len(variables)):  # we change the value of the vector coordinate-wise
            x[i] = x[i] - mul_jab_expr[i]
        my_dict = {str(var): value for var, value in zip(variables, x)}  # Building a dictionary-variable name:value
        #print(my_dict)

    return my_dict
    # raise NotImplementedError
