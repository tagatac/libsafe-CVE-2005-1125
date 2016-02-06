#!/usr/bin/env python
import csv, sys
import matplotlib as mpl
import matplotlib.pyplot as plt
BASELINE = 99.93333333333333

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

with open(filename, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	for row in csvreader:
		microbench.append((float(row[microbench_column])*1e9)/77.93333333333)
		exploit.append((1000-float(row[exploit_column]))/1000*100)

font = {'size':16}
mpl.rc('font', **font)
xmin = min(microbench)
xmax = max(microbench)
xborder = (xmax-xmin) * 0.05
ymin = min(exploit)
ymax = max(max(exploit), BASELINE)
yborder = (ymax-ymin) * 0.05

plt.scatter(microbench, exploit, marker='.')
plt.axis((xmin-xborder, xmax+xborder, ymin-yborder, ymax+yborder))
bline = plt.axhline(label="baseline", y=BASELINE, color='r')
plt.title('All Libraries NOP Injection\n(Libsafe CVE-2005-1125)')
plt.xlabel('strcpy() Overhead (Runtime Multiplier)')
plt.ylabel('Exploit Success Rate (%)')
plt.legend(handles=[bline], loc=7)
plt.savefig(filename[:-3] + 'png', bbox_inches='tight', format='png')

xmax = 150
xborder = (xmax-xmin) * 0.05

plt.scatter(microbench, exploit, marker='.')
plt.axis((xmin-xborder, xmax+xborder, ymin-yborder, ymax+yborder))
bline = plt.axhline(label="baseline", y=BASELINE, color='r')
plt.title('All Libraries NOP Injection\n(Libsafe CVE-2005-1125)')
plt.xlabel('strcpy() Overhead (Runtime Multiplier)')
plt.ylabel('Exploit Success Rate (%)')
plt.legend(handles=[bline], loc=7)
plt.savefig(filename[:-4] + 'zoom.png', bbox_inches='tight', format='png')
