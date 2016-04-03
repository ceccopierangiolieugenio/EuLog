#!/usr/bin/python2

import sys
import random

if len(sys.argv) != 3 :
	print ("Missing filename")
	print ("use %s <FILENAME> <LINES>" % sys.argv[0])
	exit(1)

filename = sys.argv[1]
lines = int(sys.argv[2])
print ("Lines=%d" % lines)

with open(filename, 'a') as out:
	for i in range(0,lines):
		seconds = 1000 + i
		m, s = divmod(seconds, 60)
		h, m = divmod(m, 60)
		out.write( "TEST;%d:%02d:%02d;COL1\tCOL2     COL3  c:COL4;LIN=%05X\tRND=%f %s\n" % (h, m, s, i, random.random(), " Fill" * random.randint(1,20)) )
