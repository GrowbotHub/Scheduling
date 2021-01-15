from inputs import read_inputs
from plants_array import all_plants
from edges import *
from graph_construction_and_draw import *
from optimization import *
from outputs import write_outputs

###  READ INPUT  ###

print("Reading the inputs")

# Read the inputs from a file and set all the parameters
read_inputs()

###  GRAPH CONSTRUCTION  ###

print("Graph construction")

# Creates the array of tuple (plant data, first day) which contains all possible plants (commodities)
all_plants()

# Creates the source and sink of the graph for each type of plant
make_meta_nodes()

# Creates the edges that stay in the same growth module
make_tray_edges()

# Creates the edges that change of growth module
make_transfer_edges()

# Creates the edges that connect the sources with the growth modules
make_source_edges()

# Creates the edges that connect the growth modules to the sinks
make_sink_edges()

# Constructs the graph with all the edges we created
construction()

# Draw the graph
draw_non_opti()

###  OPTIMIZATION  ###

print("Optimization")

# Creates the flow variables and set the per-commodity capacity constraint and the bundle constraint
make_flow_vars()

# Set the sizes constraint
size_constraint()

# Set the maximum inflow to a hole to one
max_inflow_constraint()

# Set the flow conservation constraint
flow_conservation_constraint()

# Set the balance constraint
balance_constraint()

# Start to optimize to find an optimal solution with Pulp
optimize()

###  DRAW OPTIMIZATION  ###

print("Drawing the optimized graph")

# Draw the optimized graph
draw_opti()

###  COMPUTE OUTPUT  ###

print("Output computation")

# Write the outputs in two different files
write_outputs()
