# encoding: utf-8
import sys
import random
import math


nodescount = int(sys.argv[1])
maxcap = float(sys.argv[2])
minX = float(sys.argv[3])
maxX = float(sys.argv[4])
minY = float(sys.argv[5])
maxY = float(sys.argv[6])


print 'params:'
print '  capacity %f' % maxcap
print 'nodes:'
for i in range(nodescount):
	demand = random.uniform(0.0, maxcap)
	x = random.uniform(minX, maxX)
	y = random.uniform(minY, maxY)
	# On node label printing, the number of leading zeros is according to the amount of digits of the number of the nodes count, to adjust equal string length
	print ('  node%0' + str(math.ceil(math.log(nodescount + 1) / math.log(10))) + 'd\t\t%.3f\t\t%.3f\t\t%.3f') % (i+1, demand, x, y)