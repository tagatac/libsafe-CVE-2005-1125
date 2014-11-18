#!/usr/bin/env python
"""
Runs test with MAX_DELAY set to starting iteration number to ending iteration number.
"""
import argparse, subprocess, os, sys

parser = argparse.ArgumentParser()
parser.add_argument('-S', '--start', help='Starting iteration number', default=0, type=int)
parser.add_argument('-E', '--end', help='Ending iteration number', default=100000, type=int)
parser.add_argument('-R', '--repeat', help='Number of inner loop iterations', default=50, type=int)
args = parser.parse_args()

start = args.start
end = args.end
repeat = args.repeat
FNULL = open(os.devnull, 'w')

try:
	os.mkdir('test-results')
except OSError:
	print "Error: test-results directory already exists"
	sys.exit()

# x is MAX_DELAY
for x in xrange(start, end, 100):
    total_caught = 0
    try:
        dir = subprocess.Popen(['mkdir', './test-results/{max_delay}'.format(max_delay=x)])
        dir.communicate()
    except:
        print(stderr, "Error(mkdir-x): Cannot make test results directory {m}".format(m=x))
    # Inner loop repeat 'repeat' times
    for i in xrange(repeat):
        is_good = True
        print('Randomizing for MAX_DELAY {max_delay}, iteration {num}'.format(max_delay=x, num=i))
        try:
            p = subprocess.Popen(['make', 'random', 'MAX_DELAY='+str(x)], stdout=FNULL)
            p.communicate()
        except:
            is_good = False
            print(stderr, 'Error(make random): MAX_DELAY {max_delay}, iteration {num}'.format(max_delay=x, num=i))
        try:
            r = subprocess.Popen(['/usr/bin/python2.7', './repeatbug-interpose.py'], stdout=subprocess.PIPE)
            caught, r_errors = r.communicate()
            caught = caught.split()[0]
            total_caught += int(caught)
        except:
            is_good = False
            print(stderr, 'Error(repeatbug-interpose.py): MAX_DELAY {max_delay}, iteration {num}'.format(max_delay=x, num=i))
        try:
            m = subprocess.Popen(['/bin/bash', './timing/test-microbench.sh'], stdout=subprocess.PIPE)
            time, m_errors = m.communicate()
            time = time.split()[-2]
        except:
            is_good = False
            print(stderr, 'Error(test-microbench.sh): MAX_DELAY {max_delay}, iteration {num}'.format(max_delay=x, num=i))
        if is_good:
            try:
                dir2 = subprocess.Popen(['mkdir', './test-results/{max_delay}/{iteration}'.format(max_delay=x, iteration=i)])
                dir2.communicate()
            except:
                print(stderr, "Error(mkdir-i): Cannot make test results directory {i}".format(i=i))
            try:
                with open("./test-results/{m}/{i}/{m}.{i}.csv".format(m=x, i=i), "w") as file:
                    file.write("{c},{t}\n".format(c=caught,t=time))
            except:
                print(stderr, "Error(file): Cannot write to file {m}.{i}.csv".format(m=x, i=i))
            try:
                with open("./test-results/all-results.csv", "a") as file:
                    file.write("{m},{i},{c},{t}\n".format(m=x, i=i, c=caught, t=time))
            except:
                print(stderr, "Error(file): Cannot write to file all-results.csv")
            try:
                interpose = subprocess.Popen(['cp','interpose.c', './test-results/{max_delay}/{iteration}'.format(max_delay=x, iteration=i)])
                interpose.communicate()
                print("Caught: {c} Average time of 1000 strncpy: {t}".format(c=caught, t=time))
            except:
                print(stderr, "Error(interpose): Cannot copy interpose.c to {m}/{i}".format(m=x, i=i))
    avg = total_caught/float(repeat)
    print('Average of 100 repeatbug-interpose: {avg} out of 1000'.format(avg=avg))
