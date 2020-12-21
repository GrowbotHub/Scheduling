import inputs

'''
	array of tuple (plant data, first day)
'''
plants = None

def all_plants():
	global plants
	plants = []

	for plant in inputs.plant_data:
		for day in range(inputs.HORIZON + 1 - plant.total_days):
			plants.append((plant, day))

