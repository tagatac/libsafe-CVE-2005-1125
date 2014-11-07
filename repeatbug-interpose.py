#!/usr/bin/env python

import subprocess

libsafecount=0
for i in range(1000):
	try:
		subprocess.check_output('./bug-interpose.sh', stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
		if e.output.split()[0] == 'Libsafe':
			#print e.output
			libsafecount += 1
print str(libsafecount) + ' out of 1000 exploit attempts were caught by libsafe.'
