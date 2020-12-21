import classes
import plants_array
import edges
import graph_construction_and_draw
import optimization
import outputs
from inputs import read_inputs
from plants_array import all_plants
from edges import make_meta_nodes
from edges import make_tray_edges
from edges import make_transfer_edges
from edges import make_source_edges
from edges import make_sink_edges
from graph_construction_and_draw import draw_non_opti
from graph_construction_and_draw import draw_opti
from graph_construction_and_draw import construction
from optimization import make_flow_vars
from optimization import size_constraint
from optimization import max_inflow_constraint
from optimization import inflow_equal_outflow_constraint
from optimization import balance_constraint
from optimization import optimize
from outputs import write_outputs


###         READ INPUT      ###

read_inputs()

###             GRAPH CONSTRUCTION      ###

#creates the array of tuple (plant data, first day) which contains all possible plants (commodities)
all_plants()

make_meta_nodes()
make_tray_edges()
make_transfer_edges()
make_source_edges()
make_sink_edges()

construction()
draw_non_opti()

#####       OPTIMIZATION        #####
print("optimization")

make_flow_vars()
size_constraint()
max_inflow_constraint()
inflow_equal_outflow_constraint()
balance_constraint()
optimize()

#####       DRAW OPTIMIZATION       #####

draw_opti()

###         COMPUTE OUTPUT      ####

print("Output computation")

write_outputs()
