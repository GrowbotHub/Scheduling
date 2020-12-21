from matplotlib.pyplot import savefig
import networkx as nx
import matplotlib.pyplot as plt

import edges
import plants_array as plants
import optimization as opti

g = None
pos = None

def construction():

	global g
	g = nx.DiGraph()

	for edge in edges.tray_edges:
		add_edge_to_graph(edge)
	for edge in edges.transfer_edges:
		add_edge_to_graph(edge)
	for edge in edges.source_edges:
		add_edge_to_graph(edge)
	for edge in edges.sink_edges:
		add_edge_to_graph(edge)

def add_edge_to_graph(e):
    edge = (e.node_from, e.node_to)
    g.add_edge(*edge, bounds=e.bounds, size=e.size)

###     DRAW GRAPH      ####
def draw_non_opti():
	global pos
	pos = get_node_pos(g)

	fig = plt.figure(figsize=(15, 8))
	nx.draw(g, pos=pos, node_size=60, node_color='red', edgecolors='w', width=.3, linewidths=2, edge_color='grey')
	savefig("graph.png")
	print("Done with graph")
	
def draw_opti():
	fig = plt.figure(figsize=(20, 12))
	limits = plt.axis("off")  # turn off axis

	nx.draw_networkx_nodes(g, pos, node_size=60,
						   node_color='red', edgecolors='w', linewidths=2)

	for e in g.edges:
		# a list of plants that have flow on the edge
		plant_through = []
		for p in plants.plants:
			if((e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue > 0):
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

def get_node_pos(g):
    pos = dict()
    for node in g.nodes:
        pos[node] = (node.when, node.where)
    return pos


