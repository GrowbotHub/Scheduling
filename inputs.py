import classes
from collections import defaultdict

###  INPUTS ###

# All the inputs (given by data.txt) are global variables
# Reads the data.txt file and sets all the plant data (using the Plant class in classes.py)
# and the global variables described above


def read_inputs():

    # All types of plants
    global plant_data
    # Number of growth modules
    global TRAYS
    # Number of holes per growth module
    global HOLES
    # Number of days we have to produce a maximum of plants
    global HORIZON
    # The sum of the sizes of two neighbor plants should not exceed MAX_SIZE
    global MAX_SIZE
    # Optimization timeout is set at MAX_TIME minutes
    global MAX_TIME

    f = open("data.txt", "r")

    plant_data = []
    MAX_SIZE = defaultdict(list)

    for x in f:
        data = x.replace(" ", "")
        data = data.split("|")
        if data[0] == "TRAYS":
            TRAYS = int(data[1])
        elif data[0] == "HOLES":
            HOLES = int(data[1])
        elif data[0] == "HORIZON":
            HORIZON = int(data[1])
        elif data[0] == "MAX_TIME":
            MAX_TIME = int(data[1])

        elif data[0] == "MAX_SIZE":
            constraints = data[1].split(";")

            for c in constraints:
                info_data = c.split(":")
                sizes = info_data[1].split("-")

                for s in sizes:
                    bounds = s.split(",")
                    MAX_SIZE[int(info_data[0])].append(
                        (int(bounds[0]), int(bounds[1])))
                    MAX_SIZE[int(info_data[0])].append(
                        (int(bounds[1]), int(bounds[0])))

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

    print(str(dict(MAX_SIZE)))

    f.close()
