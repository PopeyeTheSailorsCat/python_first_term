from task import lagrange as lan

a, b, c, d = lan.variables('a b c d')
C = lan.Const
fun = C(2 / 5) * (a + b) + C(2 / 5) * (c + d)
eqs = [a ** C(2) + b ** C(2) - C(3), c ** C(2) + d ** C(2) - C(1), a * c + b * c + C(2)]
var = [a, b, c, d]
# start = [1,1,1,1]
fun, lambdas = lan.build_lagrangian(fun, eqs)
var.extend(lambdas)
start = [1] * len(var)
grad = fun.grad(var)
res = lan.newton_raphson(grad, var, start)
print(res)
