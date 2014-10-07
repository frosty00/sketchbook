"""
Propositional validity checker.
Crunched down from boole.py.
Suggested by reading http://www.ps.uni-sb.de/~duchier/python/validity.py
and https://gist.github.com/2789099
"""

def is_valid(expr):       return not satisfy(expr, 0)
def satisfy(expr, value): return expr(value, {None:None}, lambda env: env)

def Literal(my_value):
    return lambda value, env, succeed: (
        my_value == value and succeed(env))

def Variable(name):
    return lambda value, env, succeed: (
        env[name] == value and succeed(env) if name in env
        else succeed(extend(env, name, value)))

def Choice(test, if0, if1):
    return lambda value, env, succeed: (
           test(0, env, lambda env: if0(value, env, succeed))
        or test(1, env, lambda env: if1(value, env, succeed)))

def extend(env, var, value):
    result = dict(env)
    result[var] = value
    return result

zero, one = Literal(0), Literal(1)

def and_(x, y): return Choice(x, zero, y)
def or_(x, y):  return Choice(x, y, one)
def not_(x):    return Choice(x, one, zero)
def impl(x, y): return Choice(x, one, y)

## x, y = map(Variable, 'x y'.split())
## is_valid(zero), is_valid(one), is_valid(x)
#. (False, True, False)

# This had a bug before we added the ugly {None:None}:
## satisfy(not_(zero), 1)
#. {None: None}

## satisfy(zero, 0)
#. {None: None}
## satisfy(zero, 1)
#. False

## satisfy(x, 1)
#. {'x': 1, None: None}
## satisfy(not_(x), 1)
#. {'x': 0, None: None}
## satisfy(and_(x, x), 1)
#. {'x': 1, None: None}
## satisfy(and_(x, not_(x)), 1)
#. False

## is_valid(impl(impl(impl(x, y), x), x))
#. True
## is_valid(impl(impl(impl(x, y), x), y))
#. False
