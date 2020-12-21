from collections import namedtuple
import inputs
import classes
import plants_array

tray_edges = None
transfer_edges = None
source_edges = None
sink_edges = None
meta_nodes = None
n_plants = None

'''
bounds : (plants, value)  value = [0,1]
size : int, size of the active plant
'''
Edge = namedtuple('Edge', ['node_from', 'node_to', 'bounds', 'size'])

def make_meta_nodes():
	global n_plants
	n_plants = len(inputs.plant_data)
	size = inputs.HORIZON / (n_plants-1)
	
	global meta_nodes
	meta_nodes = []
	for i in range(n_plants):
		meta_nodes.append((inputs.plant_data[i].source(size * i),
						   inputs.plant_data[i].sink(size * i)))

def make_tray_edges():
	global tray_edges
	tray_edges = []
	for tray in range(inputs.TRAYS):
		for hole in range(inputs.HOLES):
			for t in range(inputs.HORIZON):
				node_from = classes.Node('hole', tray, hole, t)

				# for hole_to in range(inputs.HOLES):
				#node_to = classes.Node('hole',tray, hole_to, t + 1)
				node_to = classes.Node('hole', tray, hole, t + 1)
				edge = Edge(node_from, node_to, get_bounds_per_edge(
					tray, t, plants_array.plants), get_sizes_per_edge(tray, t, plants_array.plants))
				tray_edges.append(edge)
   
def make_transfer_edges():    
	global transfer_edges     
	transfer_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]

		for i in range(len(plant_type.transfers) - 1):

			from_ = plant_type.transfers[i]
			to_ = plant_type.transfers[i + 1]

			t = plant_type.transfer_days[i][1] + plant[1]
			for hole in range(inputs.HOLES):
				node_from = classes.Node('hole', from_, hole, t)

				for hole_to in range(inputs.HOLES):
					node_to = classes.Node('hole', to_, hole_to, t+1)
					edge = Edge(node_from, node_to, get_bounds_per_edge(
						to_, t, plants_array.plants), get_sizes_per_edge(to_, t, plants_array.plants))
					transfer_edges.append(edge)

def make_source_edges():    
	global source_edges            
	source_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]
		tray = plant_type.transfers[0]
		bounds = {p: 1*(p == plant) for p in plants_array.plants}

		source = meta_nodes[get_plant_type(plant_type)][0]

		for hole in range(inputs.HOLES):
			node_to = classes.Node('hole', tray, hole, plant[1])
			edge = Edge(source, node_to, bounds, 0)
			source_edges.append(edge)

def make_sink_edges():    
	global sink_edges  
	sink_edges = []
	for plant in plants_array.plants:
		plant_type = plant[0]
		size_tray = len(plant_type.transfers)
		tray = plant_type.transfers[size_tray - 1]
		bounds = {p: 1*(p == plant) for p in plants_array.plants}

		sink = meta_nodes[get_plant_type(plant_type)][1]

		for hole in range(inputs.HOLES):
			node_from = classes.Node('hole', tray, hole,
							 plant[1] + plant_type.total_days)
			edge = Edge(node_from, sink, bounds, 0)
			sink_edges.append(edge)


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

def get_plant_type(plant):
	for i in range(n_plants):
		if(inputs.plant_data[i].name == plant.name):
			return i 
	return -1
 
