import sys

import inputs
import optimization as opti
import plants_array as plants
import graph_construction_and_draw as gc
from classes import Instruction

###  OUTPUTS  ###

# Writes the outputs in two different files :
# output.txt which contains all the instructions that the robotic arm will have to perform
# output2.txt which contains the states of all the growth modules for each day
def write_outputs():
	original_stdout = sys.stdout
	
	# Writing the instructions output
	f = open("output.txt", "w")
	sys.stdout = f

	instructions = [[] for i in range(inputs.HORIZON + 2)]

	# Three types of instructions (See the Instruction() class in the classes.py file)
	for e in gc.g.edges:
		if e[0].type == 'hole' and e[1].type == 'hole' and e[0].where != e[1].where:
			for p in plants.plants:
				if (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue == 1:
					instructions[e[1].when].append(Instruction(p[0].name, 'hole_transfer', e[0].hole,
															   e[0].tray, e[1].hole, e[1].tray))
		if e[0].type == 'source' and e[1].type == 'hole':
			for p in plants.plants:
				if (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue == 1:
					instructions[e[1].when].append(Instruction(
						p[0].name, 'source_transfer', e[1].hole, e[1].tray))

		if e[0].type == 'hole' and e[1].type == 'sink':
			for p in plants.plants:
				if (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue == 1:
					instructions[e[0].when + 1].append(Instruction(
						p[0].name, 'sink_transfer', e[0].hole, e[0].tray))


	for i in range(len(instructions)):
		print("DAY " + str(i))
		for s in instructions[i]:
			print(s.toString())	

	sys.stdout = original_stdout
	f.close()
	
	# Writing the growth modules states output
	f = open("output2.txt", "w")

	states = [[[] for i in range(inputs.HORIZON + 1)] for k in range(inputs.TRAYS)]

	for e in gc.g.edges:
		if e[1].type == 'hole':
			for p in plants.plants:
				if (e[0].type != 'source' or e[1].when == 0) and (e[0], e[1], p) in opti.flow_vars and opti.flow_vars[e[0], e[1], p].varValue == 1:
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
