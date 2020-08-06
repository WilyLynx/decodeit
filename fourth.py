from sys import stdin


class Node:
    def __init__(self):
        self.rank = 0
        self.parent = self

    def get_leader(self):
        if self.parent == self:
            return self
        else:
            leader = self.parent.get_leader()
            self.parent = leader
            return leader


class UnionFind:

    def __init__(self):
        self.elements = dict()

    def contains(self, value):
        return value in self.elements.keys()

    def add(self, value):
        self.elements[value] = Node()

    def merge(self, valueA, valueB):
        if not (self.contains(valueA)):
            self.add(valueA)
        if not (self.contains(valueB)):
            self.add(valueB)

        leaderA = self.elements[valueA].get_leader()
        leaderB = self.elements[valueB].get_leader()
        if leaderA.rank == leaderB.rank:
            leaderA.rank = leaderA.rank + 1
            leaderB.parent = leaderA
        elif leaderA.rank > leaderB.rank:
            leaderB.parent = leaderA
        else:
            leaderA.parent = leaderB

    def get_leader(self, value):
        return self.elements[value].get_leader()


union_find = UnionFind()


def add_connection(u, v):
    union_find.merge(u, v)


def find_connection(u, v):
    if not(union_find.contains(u)) or not(union_find.contains(v)):
        print('N')
    elif union_find.get_leader(u) == union_find.get_leader(v):
        print('T')
    else:
        print('N')


for line_str in stdin:
    line = line_str.split()
    if len(line) > 0:
        if line[0] == 'B':
            add_connection(line[1], line[2])
        else:
            find_connection(line[1], line[2])
