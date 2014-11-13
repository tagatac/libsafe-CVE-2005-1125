#!/usr/bin/env python

import re

functions = set()
count = 0
f=open('ltrace.log', 'r')
for line in f:
	parsedline = line.split('(')
	if len(parsedline) > 1: functions.add(parsedline[0])
f.close()

count = 0
for f in functions:
	count += 1
	print count, f

count = 0
f = open('func_names.txt', 'r')
for line in f:
	if line[0] is not '#':
		splitline = re.split('[* (]', line)[1]
		if splitline not in functions:
			count += 1
			print count, line.split('\n')[0]
