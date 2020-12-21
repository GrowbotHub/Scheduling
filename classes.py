import inputs

class Node(object):
    def __init__(self, *args):

        #('hole', tray, hole, when)
        if args[0] == 'hole':
            self.where = args[1] * (inputs.HOLES + 2) + args[2]
            self.when = args[3]
            self.sink = False
            self.type = 'hole'
            self.tray = args[1]
            self.hole = args[2]

        #('source', where, when)
        elif args[0] == 'source':
            self.where = args[1]
            self.when = args[2]
            self.sink = False
            self.type = 'source'

        #('sink', where, when)
        elif args[0] == 'sink':
            self.where = args[1]
            self.when = args[2]
            self.sink = True
            self.type = 'sink'

    def neighbors(self, other):
        return self.type == 'hole' and other.type == 'hole' and self.when == other.when and abs(self.where - other.where) == 1

    def __eq__(self, other):
        return self.where == other.where and self.when == other.when and self.type == other.type

    def __hash__(self):
        return hash((self.where, self.when, self.type))
        
class Plant():
    def __init__(self, name, total_days, color, size, transfers, transfer_days):
        self.name = name
        self.total_days = total_days
        self.color = color
        self.size = size
        self.transfers = transfers
        self.transfer_days = transfer_days

    def source(self, size):
        return Node('source', -3, size)

    def sink(self, size):
        return Node('sink', inputs.TRAYS * (inputs.HOLES + 2) + 1, size)
        
class Instruction():
    def __init__(self, name, *args):
        self.name = name
        if args[0] == 'hole_transfer':
            self.hole_from = args[1]
            self.tray_from = args[2]
            self.hole_to = args[3]
            self.tray_to = args[4]
            self.type = 'hole'

        elif args[0] == 'source_transfer':
            self.hole_to = args[1]
            self.tray_to = args[2]
            self.type = 'source'

        elif args[0] == 'sink_transfer':
            self.hole_from = args[1]
            self.tray_from = args[2]
            self.type = 'sink'

    def toString(self):
        if(self.type == 'hole'):
            return "Move the " + self.name + " from hole " + str(self.hole_from) + \
                " and tray " + str(self.tray_from) + " to hole " + str(self.hole_to) + \
                " and tray " + str(self.tray_to)
        elif(self.type == 'source'):
            return "Plant a seed of " + self.name + " to hole " + str(self.hole_to) + " and tray " + str(self.tray_to)
        else:
            return "Harvest plant " + self.name + " from hole " + str(self.hole_from) + " and tray " + str(self.tray_from)
