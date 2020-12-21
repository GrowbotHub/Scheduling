import pulp as plp
from pulp.constants import LpMaximize

import graph_construction_and_draw as gc
import inputs
import plants_array as plants
import edges

model = plp.LpProblem(name="Scheduling", sense=plp.LpMaximize)
flow_vars = None

def make_flow_vars():
	global flow_vars
	global model
	flow_vars = dict()
	for u, v, d in gc.g.edges(data=True):
		for key, val in d['bounds'].items():
			if(val > 0):
				flow_vars[u, v, key] = plp.LpVariable(name='{}_{}_{}'.format(
					*(u, v, key)), lowBound=0, upBound=1, cat='Integer')
				# per-commodity capacity constraints
				model += flow_vars[u, v, key] <= val

		# bundle constraints
		bundle = []
		bundle += [flow_vars[u, v, key]
				   for key in d['bounds'].keys() if (u, v, key) in flow_vars]
		model += plp.lpSum(bundle) <= 1


'''
give all possible pairs of neighbor holes
'''
def pair_of_neighbors(g):
    pairs = set()
    for n1 in (n1 for n1 in gc.g.nodes if n1.type == 'hole' and n1.where % 2 == 0):
        for n2 in (n2 for n2 in gc.g.nodes if n1.neighbors(n2)):
            pairs.add((n1, n2))
    return pairs


'''
Size constraints
'''
def size_constraint():
	global model
	for pair in pair_of_neighbors(gc.g):
		bundle = []
		for e in (e for e in gc.g.in_edges(pair[0], data=True) if e[0].type == 'hole'):
			for c in e[2]['size'].keys():
				if (e[0], pair[0], c) in flow_vars:
					bundle += [flow_vars[e[0], pair[0], c] * e[2]['size'].get(c)]
		for e in (e for e in gc.g.in_edges(pair[1], data=True) if e[0].type == 'hole'):
			for c in e[2]['size'].keys():
				if (e[0], pair[1], c) in flow_vars:
					bundle += [flow_vars[e[0], pair[1], c] * e[2]['size'].get(c)]
		model += plp.lpSum(bundle) <= inputs.MAX_SIZE

'''
maximum 1 plant coming from another hole, no transfer + tray allowed
'''
def max_inflow_constraint():
	global model
	inflow_from_holes = []
	for n in (n for n in gc.g.nodes if n.type == 'hole'):
		for e in (e for e in gc.g.in_edges(n) if e[0].type == 'hole'):
			for c in plants.plants:
				if (e[0], e[1], c) in flow_vars:
					inflow_from_holes += [flow_vars[e[0], e[1], c]]
		model += plp.lpSum(inflow_from_holes) <= 1
		inflow_from_holes = []

'''
calculate inflow and outflow for each node except sink/sources

inflow == outflow

respect of graph formula
'''
def get_inflow_outflow(g, flow_v, n, c):
    inflow = 0
    outflow = 0
    for e in g.in_edges(n):
        if (e[0], e[1], c) in flow_vars:
            inflow += plp.lpSum([flow_v[e[0], e[1], c]])
    for e in g.out_edges(n):
        if (e[0], e[1], c) in flow_vars:
            outflow += plp.lpSum([flow_v[e[0], e[1], c]])
    return inflow, outflow

def inflow_equal_outflow_constraint():
	global model
	for n in (n for n in gc.g.nodes if n.type == 'hole'):
		for c in plants.plants:
			inflow, outflow = get_inflow_outflow(gc.g, flow_vars, n, c)
			model += inflow - outflow == 0

def get_sink_inflow():
	sink_inflow = []
	for n in [n for n in gc.g.nodes if n.sink]:

		for e in gc.g.in_edges(n):
			for c in plants.plants:
				if (e[0], e[1], c) in flow_vars:
					sink_inflow += [flow_vars[e[0], e[1], c]]
	return sink_inflow

def balance_constraint():
	global model
	alpha = 4
	sink_inflow = get_sink_inflow()
	limit = (plp.lpSum(sink_inflow) / edges.n_plants) - alpha
	for n in [n for n in gc.g.nodes if n.sink]:
		sink = []
		for e in gc.g.in_edges(n):
			for c in plants.plants:
				if (e[0], e[1], c) in flow_vars:
					sink += [flow_vars[e[0], e[1], c]]
		model += plp.lpSum(sink) >= limit

def optimize():
	global model
	model += plp.lpSum(get_sink_inflow())
	# model.solve()
	model.solve(plp.PULP_CBC_CMD(maxSeconds=inputs.MAX_TIME * 60))
