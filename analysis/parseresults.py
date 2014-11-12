#!/usr/bin/env python

import collections

results = collections.OrderedDict()
f = open('../test-results/20141112results.csv', 'r')
for line in f:
	splitline = line.split(',')
	maxdelay = splitline[0] #number of inline assembly NOPs
	successrate = 1000 - int(splitline[2]) #exploit success rate
	microbench = float(splitline[3]) * 1000000 #microseconds
	if len(results) > maxdelay:
		results[maxdelay]['count'] += 1
		results[maxdelay]['rate'] += successrate
		results[maxdelay]['bench'] += microbench
	else:
		results[maxdelay] = dict()
		results[maxdelay]['count'] = 1
		results[maxdelay]['rate'] = successrate
		results[maxdelay]['bench'] = microbench
f.close()

for maxdelay in results:
	count = results[maxdelay]['count']
	print maxdelay + ',' + str(results[maxdelay]['rate'] / count) + ',' + str(results[maxdelay]['bench'] / count)
