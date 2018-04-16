# encoding: utf-8
import sys


vrp = {}


def readinput():
	try:
		line = raw_input().strip()
		while line == '' or line.startswith('#'):
			line = raw_input().strip()
		return line
	except EOFError:
		return None


line = readinput()
if line == None:
	print >> sys.stderr, 'Empty input!'
	exit(1)

if line.lower() != 'params:':
	print >> sys.stderr, 'Invalid input format: it must be the VRP initial params at first!'
	exit(1)

line = readinput()
if line == None:
	print >> sys.stderr, 'Invalid input: missing VRP inital params and nodes!'
	exit(1)
while line.lower != 'nodes:':
	inputs = line.split()
	if len(inputs) < 2:
		print >> sys.stderr, 'Invalid input: too few arguments for a param!'
		exit(1)
	if inputs[0].lower() == 'capacity':
		vrp['capacity'] = float(inputs[1])
	else:
		print >> sys.stderr, 'Invalid input: invalid VRP initial param!'
		exit(1)
	line = readinput()
	if line == None:
		print >> sys.stderr, 'Invalid input: missing nodes!'
		exit(1)

if not set(vrp).issuperset({'capacity'}):
	print >> sys.stderr, 'Invalid input: missing some required VRP initial params!'

line = readinput()
vrp['nodes'] = []
while line != None:
	inputs = line.split()
	if len(vrp['nodes']) == 0 and inputs[0] != 'depot':
		print >> sys.stderr, 'Invalid input: first node must be the depot!'
		exit(1)
	if len(inputs) < 4:
		print >> sys.stderr, 'Invalid input: too few arguments for a node!'
	vrp['nodes'].append({'label' : inputs[0], 'demand' : float(inputs[1]), 'posX' : float(inputs[2]), 'posY' : float(inputs[3])})
	line = readinput()