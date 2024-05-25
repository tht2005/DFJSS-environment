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

NTEST = 5000

if __name__ == "__main__":
    N_init = np.random.choice([5, 10, 15], size=NTEST)
    N_arrive = np.random.choice([10, 20, 30], size=NTEST)
    M = np.random.randint(low=5, high=11, size=NTEST)
    E = np.random.choice([1, 5, 10], size=NTEST)

    for test in range(NTEST):
        N = N_init[test] + N_arrive[test]
        machine_list = np.arange(start=1, stop=M[test] + 1, dtype=int)

        tau = np.append(np.zeros(shape=N_init[test]), np.random.exponential(scale=E[test], size=N_arrive[test]))
        for i in range(1, N):
            tau[i] += tau[i - 1]
        tau = np.floor(tau)

        A = [ np.random.randint(t, t + 6) for t in tau ]
        W = np.random.randint(low=1, high=11, size=N)

        # write test
        f = open("./tests/{}.inp".format(test + 1), "w")

        f.write('{} {}\n'.format(N, M[test]))
        f.write(''.join((str(int(t)) + ' ') for t in tau) + '\n')
        f.write(''.join((str(int(t)) + ' ') for t in A) + '\n\n')

        for i in range(N):
            f.write(str(int(W[i])) + '\n')
            for j in range(W[i]):
                Mj = np.random.randint(low=1, high=M[test] + 1)
                M_list = random.sample(machine_list.tolist(), Mj)

                f.write(str(int(Mj)) + ' ')
                for machine in M_list:
                    f.write(str(int(machine)) + ' ' + str(np.random.randint(1, 11)) + ' ')
                f.write('\n')

            f.write('\n\n')

