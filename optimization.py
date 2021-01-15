import pulp as plp
from pulp.constants import LpMaximize

import graph_construction_and_draw as gc
import inputs
import plants_array as plants
import edges

###  OPTIMIZATION  ###

# Creates the Pulp model and ask to maximize it
model = plp.LpProblem(name="Scheduling", sense=plp.LpMaximize)

# The flow variables of the model
flow_vars = None

## FLOW VARIABLES ##

# Creates the flow variables using the graph edges computed before


def make_flow_vars():
    # Set those two variables as global
    global flow_vars
    global model

    flow_vars = dict()
    for u, v, d in gc.g.edges(data=True):
        for key, val in d['bounds'].items():
            if(val > 0):
                flow_vars[u, v, key] = plp.LpVariable(name='{}_{}_{}'.format(
                    *(u, v, key)), lowBound=0, upBound=1, cat='Integer')
                # Per-commodity capacity constraints
                model += flow_vars[u, v, key] <= val

        # Bundle constraints
        bundle = []
        bundle += [flow_vars[u, v, key]
                   for key in d['bounds'].keys() if (u, v, key) in flow_vars]
        model += plp.lpSum(bundle) <= 1

## SIZE CONSTRAINT ##

# Adds the size constraint to the model :
# The sum of the sizes of two neighbor plants should not exceed MAX_SIZE (defined in inputs.py)


def size_constraint():
    global model
    for max_size in inputs.MAX_SIZE.keys():
        for pair in (pair for pair in pair_of_neighbors(gc.g) if (pair[0].hole, pair[1].hole) in inputs.MAX_SIZE[max_size]):
            bundle = []
            for e in (e for e in gc.g.in_edges(pair[0], data=True) if e[0].type == 'hole'):
                for c in e[2]['size'].keys():
                    if (e[0], pair[0], c) in flow_vars:
                        bundle += [flow_vars[e[0], pair[0], c]
                                   * e[2]['size'].get(c)]
            for e in (e for e in gc.g.in_edges(pair[1], data=True) if e[0].type == 'hole'):
                for c in e[2]['size'].keys():
                    if (e[0], pair[1], c) in flow_vars:
                        bundle += [flow_vars[e[0], pair[1], c]
                                   * e[2]['size'].get(c)]
            model += plp.lpSum(bundle) <= max_size


## MAXIMUM INFLOW CONSTRAINT ##

# Adds the maximum inflow constraint to the model :
# The inflow for all nodes in the graph (except sources ans sinks) should not exceed 1
# (Maximum one plant per hole)
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

## FLOW CONSERVATION CONSTRAINT ##

# Adds the flow conservation constraint to the model :
# Inflow and outflow of a node (except sources and sinks) should be equal


def flow_conservation_constraint():
    global model
    for n in (n for n in gc.g.nodes if n.type == 'hole'):
        for c in plants.plants:
            inflow, outflow = get_inflow_outflow(gc.g, flow_vars, n, c)
            model += inflow - outflow == 0

## BALANCE CONSTRAINT ##

# Adds the balance constraint to the model :
# The number of plants of a certain type produced should be larger or equal to the limit minus a loose up constraint alpha
# limit : The number of plant produced divided by the number of types of plant
# alpha : Set to 4 manually here (but can be changed). This constant allows the constraint to be less strict


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

## OPTIMIZE ##

# Asks the solver to maximize the number of plant produced in this model
# Can choose to authorize or not to put a timeout to the optimization


def optimize():
    global model
    model += plp.lpSum(get_sink_inflow())

    # Solves without timeout
    # model.solve()

    # Solves With a timeout of MAX_TIME minutes
    model.solve(plp.PULP_CBC_CMD(maxSeconds=inputs.MAX_TIME * 60))

# Sub-function that creates all the pairs of neighbor nodes in the graph


def pair_of_neighbors(g):
    pairs = set()
    for n1 in (n1 for n1 in gc.g.nodes if n1.type == 'hole' and n1.where % 2 == 0):
        for n2 in (n2 for n2 in gc.g.nodes if n1.neighbors(n2)):
            pairs.add((n1, n2))
    return pairs

# Sub-function that calculates the inflow and outflow for each node in the graph (except sources and sinks)


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

# Sub-function that calculates the inflow of all sinks in the graph


def get_sink_inflow():
    sink_inflow = []
    for n in [n for n in gc.g.nodes if n.sink]:

        for e in gc.g.in_edges(n):
            for c in plants.plants:
                if (e[0], e[1], c) in flow_vars:
                    sink_inflow += [flow_vars[e[0], e[1], c]]
    return sink_inflow
