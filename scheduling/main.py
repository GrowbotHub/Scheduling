from matplotlib.pyplot import savefig
import networkx as nx
import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt
import pulp as plp
from pulp.constants import LpMaximize
import sys

# n_trays = 0
# n_holes_per_tray = 0
# horizon = 0
# max_size = 0
# max_time = 2

getInput()


# class Node(object):
#     def __init__(self, *args):

#         #('hole', tray, hole, when)
#         if args[0] == 'hole':
#             self.where = args[1] * (n_holes_per_tray + 2) + args[2]
#             self.when = args[3]
#             self.sink = False
#             self.type = 'hole'
#             self.tray = args[1]
#             self.hole = args[2]

#         #('source', where, when)
#         elif args[0] == 'source':
#             self.where = args[1]
#             self.when = args[2]
#             self.sink = False
#             self.type = 'source'

#         #('sink', where, when)
#         elif args[0] == 'sink':
#             self.where = args[1]
#             self.when = args[2]
#             self.sink = True
#             self.type = 'sink'

#     def neighbors(self, other):
#         return self.type == 'hole' and other.type == 'hole' and self.when == other.when and abs(self.where - other.where) == 1

#     def __eq__(self, other):
#         return self.where == other.where and self.when == other.when and self.type == other.type

#     def __hash__(self):
#         return hash((self.where, self.when, self.type))


'''
bounds : (plants, value)  value = [0,1]
size : int, size of the active plant
'''

Edge = namedtuple('Edge', ['node_from', 'node_to', 'bounds', 'size'])


# class Plant():
#     def __init__(self, name, total_days, color, size, transfers, transfer_days):
#         self.name = name
#         self.total_days = total_days
#         self.color = color
#         self.size = size
#         self.transfers = transfers
#         self.transfer_days = transfer_days

#     def source(self, size):
#         return Node('source', -3, size)

#     def sink(self, size):
#         return Node('sink', n_trays * (n_holes_per_tray + 2) + 1, size)


###         READ INPUT      ###
# f = open("data.txt", "r")

# plant_data = []

# for x in f:
#     data = x.replace(" ", "")
#     data = data.split("|")
#     if data[0] == "TRAYS":
#         n_trays = int(data[1])
#     elif data[0] == "HOLES":
#         n_holes_per_tray = int(data[1])
#     elif data[0] == "HORIZON":
#         horizon = int(data[1])
#     elif data[0] == "MAX_SIZE":
#         max_size = int(data[1])
#     elif data[0] == "MAX_TIME":
#         max_time = int(data[1])

#     elif data[0] == "PLANT":
#         name = data[1]
#         total_days = int(data[2])
#         color = data[3]
#         sizes = list(map(int, data[4].split(",")))
#         transfers = list(map(int, data[5].split(",")))
#         transfer_days = []
#         days = data[6].split(";")
#         for d in days:
#             transfer_days.append(list(map(int, d.split(","))))

#         plant_data.append(
#             Plant(name, total_days, color, sizes, transfers, transfer_days))

# f.close()

# plant_data.append(Plant('Lettuce', 5, 'b', (1, 2, 3, 4, 5),
#                         (0, 1), ((0, 2), (2, 5))))
# plant_data.append(Plant('Fennel', 5, 'g', (1, 1, 3, 4, 6),
#                         (1, 0), ((0, 3), (3, 5))))
# plant_data.append(Plant('Marijuana', 5, 'r', (1, 2, 3, 4, 4),
#                         (2, 3, 4, 5), ((0, 1), (1, 2), (2, 3), (3, 5))))
# plant_data.append(Plant('Strawberry', 5, 'y', (1, 1, 3, 3, 5),
#                         (6, 4, 1), ((0, 1), (1, 2), (2, 5))))
# plant_data.append(Plant('Endive', 5, 'purple', (1, 2, 4, 6, 9),
#                         (0, 2, 7), ((0, 1), (1, 4), (4, 5))))
# plant_data.append(Plant('Cabbage', 5, 'orange', (1, 2, 4, 6, 8),
#                         (6, 7, 5), ((0, 1), (1, 3), (3, 5))))
# plant_data.append(Plant('Raddish', 5, 'c', (1, 2, 5, 6, 7),
#                         (4, 7), ((0, 4), (4, 5))))


# plant_data.append(Plant('Lettuce', 40, 'b', (1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7),
#                         (0, 1), ((0, 20), (20, 40))))
# plant_data.append(Plant('Fennel', 30, 'g', (1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 10),
#                         (1, 0), ((0, 10), (10, 30))))
# plant_data.append(Plant('Marijuana', 35, 'r', (1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 8, 7, 7, 7, 10, 10, 10, 10, 10, 10),
#                         (2, 3, 4, 5), ((0, 10), (10, 16), (16, 26), (26, 35))))
# plant_data.append(Plant('Strawberry', 20, 'y', (1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 6, 6, 6, 7, 7, 7, 8),
#                         (6, 4, 1), ((0, 8), (8, 12), (12, 20))))
# plant_data.append(Plant('Endive', 28, 'purple', (1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 9, 9, 10),
#                         (0, 2, 7), ((0, 10), (10, 15), (15, 28))))
# plant_data.append(Plant('Cabbage', 33, 'orange', (1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 10, 10, 11, 11),
#                         (6, 7, 5), ((0, 15), (15, 21), (21, 33))))
# plant_data.append(Plant('Raddish', 58, 'c', (1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 11, 13, 13),
#                         (4, 7), ((0, 32), (32, 58))))


###             GRAPH CONSTRUCTION      ###

n_plants = len(plant_data)
size = horizon / (n_plants-1)

meta_nodes = []
for i in range(n_plants):
    meta_nodes.append((plant_data[i].source(size * i),
                       plant_data[i].sink(size * i)))


'''
array of tuple (plant data, first day)
'''
plants = []

for plant in plant_data:
    for day in range(horizon + 1 - plant.total_days):
        plants.append((plant, day))


def isTrayInPlant(tray, plant):
    return tray in plant.transfers


def get_tray_index(tray, plant):
    return plant.transfers.index(tray)


def get_bounds_per_edge(tray, t, plants):
    bounds_dict = dict()
    for plant in plants:
        day = plant[1]
        this_plant = plant[0]
        if isTrayInPlant(tray, this_plant):
            day_from = day + \
                this_plant.transfer_days[get_tray_index(tray, this_plant)][0]
            day_to = day + \
                this_plant.transfer_days[get_tray_index(
                    tray, this_plant)][1] - 1
            bounds_dict[plant] = (day_from <= t <= day_to)*1
        else:
            bounds_dict[plant] = 0
    return bounds_dict


def get_sizes_per_edge(tray, t, plants):
    sizes_dict = dict()
    for plant in plants:
        day = plant[1]
        plant_type = plant[0]

        sizes_dict[plant] = 0

        if isTrayInPlant(tray, plant_type):
            day_from = day + \
                plant_type.transfer_days[get_tray_index(tray, plant_type)][0]
            day_to = day + \
                plant_type.transfer_days[get_tray_index(
                    tray, plant_type)][1] - 1

            if day_from <= t <= day_to:
                sizes_dict[plant] = plant_type.size[t - day]

    return sizes_dict


tray_edges = []
for tray in range(n_trays):
    for hole in range(n_holes_per_tray):
        for t in range(horizon):
            node_from = Node('hole', tray, hole, t)

            # for hole_to in range(n_holes_per_tray):
            #node_to = Node('hole',tray, hole_to, t + 1)
            node_to = Node('hole', tray, hole, t + 1)
            edge = Edge(node_from, node_to, get_bounds_per_edge(
                tray, t, plants), get_sizes_per_edge(tray, t, plants))
            tray_edges.append(edge)

transfer_edges = []
for plant in plants:
    plant_type = plant[0]

    for i in range(len(plant_type.transfers) - 1):

        from_ = plant_type.transfers[i]
        to_ = plant_type.transfers[i + 1]

        t = plant_type.transfer_days[i][1] + plant[1]
        for hole in range(n_holes_per_tray):
            node_from = Node('hole', from_, hole, t)

            for hole_to in range(n_holes_per_tray):
                node_to = Node('hole', to_, hole_to, t+1)
                edge = Edge(node_from, node_to, get_bounds_per_edge(
                    to_, t, plants), get_sizes_per_edge(to_, t, plants))
                transfer_edges.append(edge)


def get_plant_type(plant):
    for i in range(n_plants):
        if plant_data[i].name == plant.name:
            return i
    return -1


source_edges = []
for plant in plants:
    plant_type = plant[0]
    tray = plant_type.transfers[0]
    bounds = {p: 1*(p == plant) for p in plants}

    source = meta_nodes[get_plant_type(plant_type)][0]

    for hole in range(n_holes_per_tray):
        node_to = Node('hole', tray, hole, plant[1])
        edge = Edge(source, node_to, bounds, 0)
        source_edges.append(edge)


sink_edges = []
for plant in plants:
    plant_type = plant[0]
    size_tray = len(plant_type.transfers)
    tray = plant_type.transfers[size_tray - 1]
    bounds = {p: 1*(p == plant) for p in plants}

    sink = meta_nodes[get_plant_type(plant_type)][1]

    for hole in range(n_holes_per_tray):
        node_from = Node('hole', tray, hole,
                         plant[1] + plant_type.total_days)
        edge = Edge(node_from, sink, bounds, 0)
        sink_edges.append(edge)

g = nx.DiGraph()


def add_edge_to_graph(e):
    edge = (e.node_from, e.node_to)
    g.add_edge(*edge, bounds=e.bounds, size=e.size)


for edge in tray_edges:
    add_edge_to_graph(edge)
for edge in transfer_edges:
    add_edge_to_graph(edge)
for edge in source_edges:
    add_edge_to_graph(edge)
for edge in sink_edges:
    add_edge_to_graph(edge)


###     DRAW GRAPH      ####


def get_node_pos(g):
    pos = dict()
    for node in g.nodes:
        pos[node] = (node.when, node.where)
    return pos


pos = get_node_pos(g)


# fig = plt.figure(figsize=(15, 8))
# nx.draw(g, pos=pos, node_size=60, node_color='red',
#         edgecolors='w', width=.3, linewidths=2, edge_color='grey')
# savefig("graph.png")
# print("Done with graph")


#####       OPTIMIZATION        #####
print("optimization")

model = plp.LpProblem(name="Scheduling", sense=plp.LpMaximize)

flow_vars = dict()
for u, v, d in g.edges(data=True):
    for key, val in d['bounds'].items():
        # DELETE THE IF TO GO BACK TO NORMAL
        if(val > 0):
            flow_vars[u, v, key] = plp.LpVariable(name='{}_{}_{}'.format(
                *(u, v, key)), lowBound=0, upBound=1, cat='Integer')
            # per-commodity capacity constraints
            model.addConstraint(flow_vars[u, v, key] <= val)

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
    for n1 in (n1 for n1 in g.nodes if n1.type == 'hole' and n1.where % 2 == 0):
        for n2 in (n2 for n2 in g.nodes if n1.neighbors(n2)):
            pairs.add((n1, n2))
    return pairs


'''
Size constraints
'''

for pair in pair_of_neighbors(g):
    bundle = []
    for e in (e for e in g.in_edges(pair[0], data=True) if e[0].type == 'hole'):
        for c in e[2]['size'].keys():
            if (e[0], pair[0], c) in flow_vars:
                bundle += [flow_vars[e[0], pair[0], c] * e[2]['size'].get(c)]
        #bundle += [flow_vars[e[0], pair[0], c] * e[2]['size'].get(c) for c in e[2]['size'].keys()]
    for e in (e for e in g.in_edges(pair[1], data=True) if e[0].type == 'hole'):
        for c in e[2]['size'].keys():
            if (e[0], pair[1], c) in flow_vars:
                bundle += [flow_vars[e[0], pair[1], c] * e[2]['size'].get(c)]
        #bundle += [flow_vars[e[0], pair[1], c] * e[2]['size'].get(c) for c in e[2]['size'].keys()]
    model += plp.lpSum(bundle) <= max_size

'''
maximum 1 plant coming from another hole, no transfer + tray allowed

'''
inflow_from_holes = []
for n in (n for n in g.nodes if n.type == 'hole'):
    for e in (e for e in g.in_edges(n) if e[0].type == 'hole'):
        for c in plants:
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


for n in (n for n in g.nodes if n.type == 'hole'):
    for c in plants:
        inflow, outflow = get_inflow_outflow(g, flow_vars, n, c)
        model += inflow - outflow == 0

sink_inflow = []
for n in [n for n in g.nodes if n.sink]:

    for e in g.in_edges(n):
        for c in plants:
            if (e[0], e[1], c) in flow_vars:
                sink_inflow += [flow_vars[e[0], e[1], c]]


alpha = 4
limit = (plp.lpSum(sink_inflow) / n_plants) - alpha
for n in [n for n in g.nodes if n.sink]:
    sink = []
    for e in g.in_edges(n):
        for c in plants:
            if (e[0], e[1], c) in flow_vars:
                sink += [flow_vars[e[0], e[1], c]]
    model += plp.lpSum(sink) >= limit


model += plp.lpSum(sink_inflow)
# model.solve()
model.solve(plp.PULP_CBC_CMD(maxSeconds=max_time * 60))


#####       DRAW OPTIMIZATION       #####


fig = plt.figure(figsize=(20, 12))
limits = plt.axis("off")  # turn off axis

nx.draw_networkx_nodes(g, pos, node_size=60,
                       node_color='red', edgecolors='w', linewidths=2)


for e in g.edges:
    # a list of plants that have flow on the edge
    plant_through = []
    for p in plants:
        if((e[0], e[1], p) in flow_vars and flow_vars[e[0], e[1], p].varValue > 0):
            plant_through += [p]
    if len(plant_through):
        plant_type = plant_through[0][0]
        g.edges[e[0], e[1]]['color'] = plant_type.color
    else:
        g.edges[e[0], e[1]]['color'] = 'grey'


edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] == 'grey']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='grey', width=.3)

edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] == 'b']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='b', width=1)

edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] == 'g']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='g', width=1)

edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] == 'r']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='r', width=1)

edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] == 'y']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='y', width=1)

edgelist = [(e, e_) for e, e_, d in g.edges(
    data=True) if d['color'] == 'purple']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='purple', width=1)

edgelist = [(e, e_) for e, e_, d in g.edges(
    data=True) if d['color'] == 'orange']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='orange', width=1)

edgelist = [(e, e_) for e, e_, d in g.edges(data=True) if d['color'] == 'c']
nx.draw_networkx_edges(g, pos, edgelist, edge_color='c', width=1)

savefig("optimized.png")
print("Done with optimized graph")


###         COMPUTE OUTPUT      ####

print("Output")


class Instruction():
    def __init__(self, name, *args):
        self.name = name
        if args[0] == 'hole_transfer':
            self.hole_from = args[1]
            self.tray_from = args[2]
            self.hole_to = args[3]
            self.tray_to = args[4]
            self.type = 'hole'

        elif args[0] == 'source_transfer':
            self.hole_to = args[1]
            self.tray_to = args[2]
            self.type = 'source'

        elif args[0] == 'sink_transfer':
            self.hole_from = args[1]
            self.tray_from = args[2]
            self.type = 'sink'

    def toString(self):
        if(self.type == 'hole'):
            return "Move the " + self.name + " from hole " + str(self.hole_from) + \
                " and tray " + str(self.tray_from) + " to hole " + str(self.hole_to) + \
                " and tray " + str(self.tray_to)
        elif(self.type == 'source'):
            return "Plant a seed of " + self.name + " to hole " + str(self.hole_to) + " and tray " + str(self.tray_to)
        else:
            return "Harvest plant " + self.name + " from hole " + str(self.hole_from) + " and tray " + str(self.tray_from)


original_stdout = sys.stdout
f = open("output.txt", "w")
sys.stdout = f

instructions = [[] for i in range(horizon + 2)]

for e in g.edges:
    if e[0].type == 'hole' and e[1].type == 'hole' and e[0].where != e[1].where:
        for p in plants:
            if (e[0], e[1], p) in flow_vars and flow_vars[e[0], e[1], p].varValue == 1:
                instructions[e[1].when].append(Instruction(p[0].name, 'hole_transfer', e[0].hole,
                                                           e[0].tray, e[1].hole, e[1].tray))
    if e[0].type == 'source' and e[1].type == 'hole':
        for p in plants:
            if (e[0], e[1], p) in flow_vars and flow_vars[e[0], e[1], p].varValue == 1:
                instructions[e[1].when].append(Instruction(
                    p[0].name, 'source_transfer', e[1].hole, e[1].tray))

    if e[0].type == 'hole' and e[1].type == 'sink':
        for p in plants:
            if (e[0], e[1], p) in flow_vars and flow_vars[e[0], e[1], p].varValue == 1:
                instructions[e[0].when + 1].append(Instruction(
                    p[0].name, 'sink_transfer', e[0].hole, e[0].tray))


for i in range(len(instructions)):
    print("DAY " + str(i))
    for s in instructions[i]:
        print(s.toString())

sys.stdout = original_stdout
f.close()

f = open("output2.txt", "w")

states = [[[] for i in range(horizon + 1)] for k in range(n_trays)]

for e in g.edges:
    if e[1].type == 'hole':
        for p in plants:
            if (e[0].type != 'source' or e[1].when == 0) and (e[0], e[1], p) in flow_vars and flow_vars[e[0], e[1], p].varValue == 1:
                states[e[1].tray][e[1].when].append(
                    "Hole : " + str(e[1].hole) + " | Plant : " + p[0].name)

sys.stdout = f
for i in range(len(states)):
    print("GROWTH MODULE " + str(i))
    for j in range(len(states[i])):
        if(len(states[i][j]) != 0):
            print("DAY " + str(j))
            for k in range(len(states[i][j])):
                print(states[i][j][k])

sys.stdout = original_stdout
f.close()
