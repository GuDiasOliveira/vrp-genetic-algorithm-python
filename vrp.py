# encoding: utf-8
import sys
import random
import math


vrp = {}


## First reading the VRP from the input ##


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
	print >> sys.stderr, 'Invalid input: it must be the VRP initial params at first!'
	exit(1)

line = readinput()
if line == None:
	print >> sys.stderr, 'Invalid input: missing VRP inital params and nodes!'
	exit(1)
while line.lower() != 'nodes:':
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
	exit(1)

line = readinput()
vrp['nodes'] = [{'label' : 'depot', 'demand' : 0, 'posX' : 0, 'posY' : 0}]
while line != None:
	inputs = line.split()
	if len(inputs) < 4:
		print >> sys.stderr, 'Invalid input: too few arguments for a node!'
		exit(1)
	vrp['nodes'].append({'label' : inputs[0], 'demand' : float(inputs[1]), 'posX' : float(inputs[2]), 'posY' : float(inputs[3])})
	line = readinput()

if len(vrp['nodes']) == 0:
	print >> sys.stderr, 'Invalid input: no such nodes!'
	exit(1)


## After inputting and validating it, now computing the algorithm ##


def distance(n1, n2):
	dx = n2['posX'] - n1['posX']
	dy = n2['posY'] - n1['posY']
	return math.sqrt(dx * dx + dy * dy)

def fitness(p):
	# The first distance is from depot to the first node of the first route
	s = distance(vrp['nodes'][0], vrp['nodes'][p[0]])
	# Then calculating the distances between the nodes
	for i in range(len(p) - 1):
		prev = vrp['nodes'][p[i]]
		next = vrp['nodes'][p[i + 1]]
		s += distance(prev, next)
	# The last distance is from the last node of the last route to the depot
	s += distance(vrp['nodes'][p[len(p) - 1]], vrp['nodes'][0])
	return s

def adjust(p):
	# Adjust repeated
	repeated = True
	while repeated:
		repeated = False
		for i1 in range(len(p)):
			for i2 in range(i1):
				if p[i1] == p[i2]:
					haveAll = True
					for nodeId in range(len(vrp['nodes'])):
						if nodeId not in p:
							p[i1] = nodeId
							haveAll = False
							break
					if haveAll:
						del p[i1]
					repeated = True
				if repeated: break
			if repeated: break
	# Adjust capacity exceed
	i = 0
	s = 0.0
	cap = vrp['capacity']
	while i < len(p):
		s += vrp['nodes'][p[i]]['demand']
		if s > cap:
			p.insert(i, 0)
			s = 0.0
		i += 1
	i = len(p) - 2
	# Adjust two consective depots
	while i >= 0:
		if p[i] == 0 and p[i + 1] == 0:
			del p[i]
		i -= 1


popsize = int(sys.argv[1])
iterations = int(sys.argv[2])

pop = []

# Generating random initial population
for i in range(popsize):
	p = range(1, len(vrp['nodes']))
	random.shuffle(p)
	pop.append(p)
for p in pop:
	adjust(p)

# Running the genetic algorithm
for i in range(iterations):
	nextPop = []
	# Each one of this iteration will generate two descendants individuals. Therefore, to guarantee same population size, this will iterate half population size times
	for j in range(int(len(pop) / 2)):
		# Selecting randomly 4 individuals to select 2 parents by a binary tournament
		parentIds = set()
		while len(parentIds) < 4:
			parentIds |= {random.randint(0, len(pop) - 1)}
		parentIds = list(parentIds)
		# Selecting 2 parents with the binary tournament
		parent1 = pop[parentIds[0]] if fitness(pop[parentIds[0]]) < fitness(pop[parentIds[1]]) else pop[parentIds[1]]
		parent2 = pop[parentIds[2]] if fitness(pop[parentIds[2]]) < fitness(pop[parentIds[3]]) else pop[parentIds[3]]
		# Selecting two random cutting points for crossover, with the same points (indexes) for both parents, based on the shortest parent
		cutIdx1, cutIdx2 = random.randint(1, min(len(parent1), len(parent2)) - 1), random.randint(1, min(len(parent1), len(parent2)) - 1)
		cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)
		# Doing crossover and generating two children
		child1 = parent1[:cutIdx1] + parent2[cutIdx1:cutIdx2] + parent1[cutIdx2:]
		child2 = parent2[:cutIdx1] + parent1[cutIdx1:cutIdx2] + parent2[cutIdx2:]
		nextPop += [child1, child2]
	# Doing mutation: swapping two positions in one of the individuals, with 1:15 probability
	if random.randint(1, 15) == 1:
		ptomutate = nextPop[random.randint(0, len(nextPop) - 1)]
		i1 = random.randint(0, len(ptomutate) - 1)
		i2 = random.randint(0, len(ptomutate) - 1)
		ptomutate[i1], ptomutate[i2] = ptomutate[i2], ptomutate[i1]
	# Adjusting individuals
	for p in nextPop:
		adjust(p)
	# Updating population generation
	pop = nextPop

# Selecting the best individual, which is the final solution
better = None
bf = float('inf')
for p in pop:
	f = fitness(p)
	if f < bf:
		bf = f
		better = p


## After processing the algorithm, now outputting it ##


# Printing the solution
print ' route:'
print 'depot'
for nodeIdx in better:
	print vrp['nodes'][nodeIdx]['label']
print 'depot'
print ' cost:'
print '%f' % bf