# MACHINE_FREE[k]: the time you can use it again
# JOB_FREE[i]: its last dispatch operation's finish time
# H[i]: number of completed operations of job i
# W[i]: number of operations of job i, enumerated 0, 1, ..., W[i] - 1
# T[i][j][k]: time for machine k complete j-th operation of job i (equal -1 if machine k can not do this operation).

class solution:
    def update(self, TIME, N_MACHINE, N_JOB, MACHINE_FREE, JOB_FREE, H, W, T):
        # your solution goes here
        # return a list of dispatching actions (pair of job-matchine)

        # a naive dispatching rule for an example
        for i in range(N_JOB):
            if JOB_FREE[i] > TIME or H[i] == W[i]:
                continue

            j = H[i]
            for k in range(N_MACHINE):
                if MACHINE_FREE[k] <= TIME and T[i][j][k] != -1:
                    return [ [i, k] ] # return a list of actions (job, machine)

        # if you don't want to do any actions, please:
        return [ [-1, -1] ]
        # do not return an empty array

