import pytest
import random
import math
from functools import partial
from .linalg import inv, dot
from . import lagrange as lan


class CaseEval:
    def __init__(self, expr, correct, name, **kwargs):
        self._name = name
        self.res = expr(**kwargs)
        self.correct = correct

    def __str__(self) -> str:
        return 'test_{}'.format(self._name)


class CaseSolve:
    def __init__(self, a, b, name):
        self._name = name
        a_inv = inv(a)
        self.a = a
        self.b = b
        self.x = dot(a_inv, b)

    def __str__(self) -> str:
        return 'test_{}'.format(self._name)


class CaseNewton:
    def __init__(self, fun, variables, start, name):
        self._name = name
        self.vars = variables
        self.fun = fun
        self.res = lan.newton_raphson(fun, variables, start)

    def __str__(self) -> str:
        return 'test_{}'.format(self._name)


class CaseLagrange:
    def __init__(self, fun, eqs, variables, correct, name):
        fun, lambdas = lan.build_lagrangian(fun, eqs)
        variables.extend(lambdas)
        start = [1] * len(variables)
        grad = fun.grad(variables)
        self.res = lan.newton_raphson(grad, variables, start)
        self.corr = correct


def fun_rosen(x):
    """
    Calculate this: https://en.wikipedia.org/wiki/Rosenbrock_function

    Parameters
    --------
    x : list or numpy.ndarray
        Parameters vector of an arbitrary length. The length of this vector
        defines the degree of the Rosenbrock function.

    Returns
    -------
    Rosenbrock function value at point x.

    """
    return sum(100 * ((a - b ** 2) ** 2) + (1 - b) ** 2
               for a, b in zip(x[1:], x[:-1]))


random.seed(1)

TEST_CASES_NEWTON = list()

x, y, z = lan.variables('x y z')
fun = x ** lan.Const(4) - lan.Const(16)
TEST_CASES_NEWTON.append(CaseNewton(fun, [x], [1], 'fun1'))

TEST_CASES_SOLVE = [CaseSolve([[1, 2], [3, 4]], [0, 3], 'sys1'),
                    CaseSolve([[6, 2, 3.25], [5, 0, 1], [0, 0, 10]], [1, 10, 1],
                              'sys2')]

TEST_CASES_EVAL = [CaseEval(lan.Sum(x, lan.Product(x, x)).d(x), 85,
                            'sum', x=42),
                   CaseEval(lan.Product(x, lan.Sum(x, lan.Const(2))), 1848,
                            'prod', x=42),
                   CaseEval(lan.Fraction(lan.Product(x, y),
                                         lan.Sum(lan.Const(42), x)).d(x),
                            0.14285714285714285, 'sum', x=42, y=24),
                   CaseEval(lan.Power(lan.Fraction(x, lan.Const(4)),
                                      lan.Const(2)).d(x), 5.25, 'power', x=42)]

TEST_CASES_LAGRANGE = []
fun = x ** lan.Const(2) + y ** lan.Const(2) + z ** lan.Const(2)
eqs = [x - lan.Const(6)]
TEST_CASES_LAGRANGE.append(CaseLagrange(fun, eqs, [x, y, z], [6, 0, 0], 'hyp'))


@pytest.mark.parametrize('eval', TEST_CASES_EVAL, ids=str)
def test_eval(eval: CaseEval):
    assert eval.correct == eval.res


@pytest.mark.parametrize('sys', TEST_CASES_SOLVE, ids=str)
def test_linalg(sys: CaseSolve) -> None:
    a, x, b = sys.a, sys.x, sys.b
    assert sum(abs(i - j) for i, j in zip(dot(a, x), b)) / len(x) < 1e-6


@pytest.mark.parametrize('fun', TEST_CASES_NEWTON, ids=str)
def test_newton(fun: CaseNewton) -> None:
    f, res = fun.fun, fun.res
    assert abs(f(**res)) < 1e-6


@pytest.mark.parametrize('lag', TEST_CASES_LAGRANGE, ids=str)
def test_lagrange(lag: CaseLagrange) -> None:
    res, corr = lag.res, lag.corr
    assert sum(abs(r - c) for r, c in zip(res.values(), corr)) / len(res) < 1e-6
