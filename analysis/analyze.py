#!/usr/bin/env python
import csv, sys
import matplotlib.pyplot as plt
BASELINE = 99.93333333333333
BASELINE_MICRO = 0.00000007625233333
THRESHOLD = 950

if len(sys.argv) < 2:
	print "Usage: gen_fig.py <results filename> [<microbench column>] [<exploit measure column>]"
	sys.exit()
filename = sys.argv[1]
if len(sys.argv) > 2: microbench_column = sys.argv[2]
else: microbench_column = -1
if len(sys.argv) > 3: exploit_column = sys.argv[3]
else: exploit_column = 2

microbench = list()
exploit = list()

for slice in range(0, 2000, 20):
	greatercount = 0
	count = 0
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			if float(row[microbench_column]) >= slice*BASELINE_MICRO and float(row[microbench_column]) < (slice+20)*BASELINE_MICRO:
				if float(row[exploit_column]) > THRESHOLD: greatercount += 1
				count += 1
	print str(slice) + '\n=====\n' + str(greatercount) + ' out of ' + str(count) + ' = ' + str(float(greatercount)/count*100) + '%'
