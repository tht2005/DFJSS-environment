# Test format:
# M N
# tau_1 tau_2 ...
# A_1 A_2 ...
#
# for each job i from 1 to N:
#   O: number of operations
#   for each operation:
#       Mj (M1 t1) (M2 t2) ...

import numpy as np
import random
import os

MMACHINE = [5, 10, 10, 15, 20]
NJOB = [5, 10, 30, 15, 20]
NTEST = 1000

t = np.zeros(shape=(100, 100, 100))

for (M, N) in zip(MMACHINE, NJOB):
    dirname = "./tests/{}_{}".format(M, N)

    E = np.random.choice([1, 5, 10], size=NTEST)

    for test in range(NTEST):
        filename = "{}/{}.inp".format(dirname, test + 1)

        tau = np.random.exponential(scale=E[test], size=N)
        for i in range(1, N):
            tau[i] += tau[i - 1]
        tau = np.floor(tau)
        A = [ np.random.randint(t, t + 6) for t in tau ]

        W = np.random.randint(low=1, high=11, size=N)
        for i in range(N):
            for j in range(W[i]):
                random.sample(

