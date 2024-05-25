import matplotlib.pyplot as plt
import numpy as np
import heapq, sys
from solution import solution as sol
from gentest import NTEST

class event:
    # type = 0: job arrival
    # type = 1: machine free
    def __init__(self, TIME, TYPE):
        self.T = TIME
        self.TYPE = TYPE

    def __lt__(self, other):
        return self.T < other.T

plot_data = []

output = open('out.txt', 'w')

if __name__ == "__main__":
    for test in range(NTEST):
        print('At the start of test {}'.format(test + 1))

        f = open('./tests/{}.inp'.format(test + 1, "r"))
        raw_file = f.read()
        f.close()

        raw_file_lines = raw_file.split('\n')

        parsed_input = []

        for raw_line in raw_file_lines:
            if raw_line == '':
                continue
            line = raw_line.split(' ')
            while '' in line:
                line.remove('')
            parsed_input.append(list(map(int, line)))
        
        N = parsed_input[0][0]
        M = parsed_input[0][1]
        tau = parsed_input[1]
        A = parsed_input[2]
        W = np.zeros(shape=N, dtype=int)

        t = np.full(shape=(N, 12, 12), fill_value=-1)

        ptr = 3
        for i in range(N):
            W[i] = parsed_input[ptr][0]
            ptr += 1
            for j in range(W[i]):
                Mj = parsed_input[ptr][0]
                for pos in range(Mj):
                    _machine = parsed_input[ptr][2 * pos + 1] - 1
                    _time = parsed_input[ptr][2 * pos + 2]
                    t[i][j][_machine] = _time
                ptr += 1

        # user solution
        solver = sol()
        cur_njob = 0
        machine_free = np.zeros(shape=M)
        job_free = []
        H = []

        HEAP = []

        # job arrive
        for i in range(N):
            HEAP.append(event(TIME=tau[i], TYPE=0))
        heapq.heapify(HEAP)

        while True:
            events = [ ]
            TIME = -1
            while len(HEAP) > 0 and (TIME == -1 or HEAP[0].T == TIME):
                events.append(heapq.heappop(HEAP))
                TIME = events[0].T

            for e in events:
                if e.TYPE == 0:
                    cur_njob += 1
                    job_free.append(0)
                    H.append(0)
            
            actions = solver.update(TIME, M, cur_njob, machine_free, job_free, H, W[:cur_njob], t[:cur_njob])

            if len(actions) == 0:
                print('Error! Returned action list should not be empty.')
                sys.exit()

            for a in actions:
                job = a[0]
                machine = a[1]
                if job < 0:
                    break

                if job_free[job] > TIME:
                    print('Error! Job {}\'s last operation is still on a machine'.format(job + 1))
                    sys.exit()
                if H[job] == W[job]:
                    print('Error! Job {} is already done (don\'t have any operation left).'.format(job + 1))
                    sys.exit()
                if machine_free[machine] > TIME:
                    print('Error! Machine {} is still busy.'.format(machine + 1))
                    sys.exit()
                if t[job][H[job]][machine] == -1:
                    print('Machine {} can not do {}-th operation of job {}'.format(machine + 1, H[job] + 1, job + 1))
                    sys.exit()

                T = t[job][H[job]][machine]
                H[job] += 1
                job_free[job] = TIME + T
                machine_free[machine] = TIME + T
                
                heapq.heappush(HEAP, event(TIME=TIME + T, TYPE=1))

            # end criteria 
            if cur_njob == N:
                all_job_done = True
                for i in range(N):
                    if H[i] < W[i]:
                        all_job_done = False
                        break
                if all_job_done:
                    break

        print('At the end of test {}'.format(test + 1))
        S = 0
        for i in range(N):
            S += job_free[i] - A[i]
        print('Cost:', S)
        plot_data.append(S)

        output.write(str(int(S)) + ' ')

plt.title('Your result')
plt.violinplot(dataset=plot_data, showmeans=True)
plt.show()

