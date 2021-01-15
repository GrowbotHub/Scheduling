

class Node(object):
    def __init__(self, *args):

        #('hole', tray, hole, when)
        if args[0] == 'hole':
            self.where = args[1] * (n_holes_per_tray + 2) + args[2]
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
        return Node('sink', n_trays * (n_holes_per_tray + 2) + 1, size)
