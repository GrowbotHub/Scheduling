import classes

plant_data = None
TRAYS = None
HOLES = None
HORIZON = None
MAX_SIZE = None
MAX_TIME = None

def read_inputs():

	global plant_data
	global TRAYS
	global HOLES
	global HORIZON
	global MAX_SIZE
	global MAX_TIME
	
	f = open("data.txt", "r")

	plant_data = []

	for x in f:
		data = x.replace(" ", "")
		data = data.split("|")
		if data[0] == "TRAYS":
			TRAYS = int(data[1])
		elif data[0] == "HOLES":
			HOLES = int(data[1])
		elif data[0] == "HORIZON":
			HORIZON = int(data[1])
		elif data[0] == "MAX_SIZE":
			MAX_SIZE = int(data[1])
		elif data[0] == "MAX_TIME":
			MAX_TIME = int(data[1])

		elif data[0] == "PLANT":
			name = data[1]
			total_days = int(data[2])
			color = data[3]
			sizes = list(map(int, data[4].split(",")))
			transfers = list(map(int, data[5].split(",")))
			transfer_days = []
			days = data[6].split(";")
			for d in days:
				transfer_days.append(list(map(int, d.split(","))))

			plant_data.append(
				classes.Plant(name, total_days, color, sizes, transfers, transfer_days))

	f.close()
