"""
Artifical Intelligence: A Modern Approach (3rd ed.) p. 531
"""

import random

# Let's simplify by assuming there's just one Bayes net, and this will
# list its variables, with parents preceding children:
all_vars = []

class Variable:
    "A binary (True/False) random variable."

    def __init__(self, parents, cpt):
        self.parents = parents  # The variables that I depend on.
        self.cpt = cpt          # The conditional probability that I'm true, for each combo of the parents' values.
        all_vars.append(self)

    def p_true(self, e):
        """Return my conditional probability of being True, given that my
        parents have the values specified by e."""
        return self.cpt[tuple(e[var] for var in self.parents)]

def prior_sample():
    "Return a random sample from the full joint distribution."
    x = {}
    for Xi in all_vars:  # N.B. this depends on the order of variables (parents before children).
        x[Xi] = random.random() < Xi.p_true(x)
    return x


# Burglary example [AIMA figure 14.2]

T, F = True, False

burglary   = Variable((), {(): 0.001})
earthquake = Variable((), {(): 0.002})
alarm      = Variable((burglary, earthquake),
                      {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001})
john_calls = Variable((alarm,), {(T,): 0.90, (F,): 0.05})
mary_calls = Variable((alarm,), {(T,): 0.70, (F,): 0.01})

def simulate(n_trials):
    print 'BEAJM'
    for _ in xrange(n_trials):
        x = prior_sample()
        print ''.join('.*'[x[var]] for var in [burglary, earthquake, alarm, john_calls, mary_calls])

# In 100 random trials, John calls 3 times, Mary calls once -- all false alarms:
## random.seed(1017)
## simulate(100)
#. BEAJM
#. .....
#. ...*.
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. ...*.
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. ...*.
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. ...*.
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. ....*
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
#. .....
