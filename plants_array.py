import inputs

###  PLANTS ARRAY  ###

# Array of tuple (plant data, first day)
plants = None

# Creates the array that holds all the types of plants (commodities) for each possible day
def all_plants():
	global plants
	plants = []

	for plant in inputs.plant_data:
		# Cannot seed a plant if it has not the time to grow
		for day in range(inputs.HORIZON + 1 - plant.total_days):
			plants.append((plant, day))

