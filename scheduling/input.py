from classes import Node, Plant

n_trays = 0
n_holes_per_tray = 0
horizon = 0
max_size = 0
max_time = 2
plant_data = []


def getInput():

    f = open("data.txt", "r")

    for x in f:
        data = x.replace(" ", "")
        data = data.split("|")
        if data[0] == "TRAYS":
            n_trays = int(data[1])
        elif data[0] == "HOLES":
            n_holes_per_tray = int(data[1])
        elif data[0] == "HORIZON":
            horizon = int(data[1])
        elif data[0] == "MAX_SIZE":
            max_size = int(data[1])
        elif data[0] == "MAX_TIME":
            max_time = int(data[1])

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
                Plant(name, total_days, color, sizes, transfers, transfer_days))

    f.close()
    return plant_data
