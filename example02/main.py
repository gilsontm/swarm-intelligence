# imports random module
import random

class Graph:
    def __init__(self):
        self.adj = {}
        self.cost = {}
        self.pherom = {}
        self.start = -1
        self.to_update = {}

    def start_position(self):
        return self.start

    def define_start(self, s):
        self.start = s

    def adjacent(self, u, v, w):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)
        self.pherom[(u,v)] = 1
        self.cost[(u,v)] = w

    def moviment_cost(self, u, v):
        return self.cost[(u, v)]

    def pheromone(self, u, v):
        return self.pherom[(u, v)]

    def adjacents(self, u):
        if u not in self.adj:
            return []
        return self.adj[u]

    def inc_pherom(self, u, v):
        if (u, v) not in self.to_update:
            self.to_update[(u, v)] = 1
        else:
            self.to_update[(u, v)] = self.to_update[(u, v)] + 1

    def update(self):
        for pair in self.to_update:
            amount = self.to_update[pair]
            self.pherom[pair] += amount
        self.to_update = {}

class Unit:

    FOWARD = 1
    BACKWARD = 2

    def __init__(self, graph):
        self.graph = graph
        self.pos = graph.start_position()
        self.state = Unit.FOWARD
        self.wait = 0
        self.path = [self.pos]

    def step(self):
        if self.wait > 0:
            self.wait -= 1
        elif self.state == Unit.FOWARD:
            u = self.pos
            adjacents = self.graph.adjacents(u)
            if adjacents:
                total = 0
                for v in adjacents:
                    p = self.graph.pheromone(u, v)
                    total += p * p
                rand = random.randint(1, total)
                for v in adjacents:
                    pherom = self.graph.pheromone(u, v)
                    """
                        Utiliza-se o quadrático dos feromónios para realmente icentivar
                        a ir para o caminho de maior feromónios.
                    """
                    if rand <= pherom * pherom:
                        # mover
                        self.path.append(v)
                        self.pos = v
                        self.wait = self.graph.moviment_cost(u, v)
                        # self.graph.inc_pherom(u, v)
                        break
                    else:
                        rand -= pherom * pherom
            else:
                self.state = Unit.BACKWARD
                self.step()
        elif self.state == Unit.BACKWARD:
            v = self.path.pop()
            if self.path:
                u = self.path[-1]
                w = self.graph.moviment_cost(u, v)
                self.graph.inc_pherom(u, v)
                self.graph.inc_pherom(u, v)
                self.wait = w
                self.pos = u
            else:
                self.state = Unit.FOWARD
                self.path.append(v)
                self.pos = v
                self.step()

"""
        B --2-- E --3-- H
       / \     / \       \
      2   3   5   7       1
     /     \ /     \       \
    A --6-- C --12- F --6-- I
     \     / \     / \     /
      4   2   2   3   4   7
       \ /     \ /     \ /
        D --5-- G --6-- J
"""

def print_graph(g, index, symbol, units):
    for value in index:
        u = index[value]
        adjacents = g.adjacents(u)
        for v in adjacents:
            print('(', symbol[u], ',', symbol[v], ') =', g.pheromone(u, v))

def main():
    index = {'A': 1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10}
    symbol = {}
    for s in index:
        value = index[s]
        symbol[value] = s

    g = Graph()
    g.adjacent(index['A'], index['B'], 2)
    g.adjacent(index['A'], index['C'], 6)
    g.adjacent(index['A'], index['D'], 4)
    g.adjacent(index['B'], index['E'], 2)
    g.adjacent(index['B'], index['C'], 3)
    g.adjacent(index['C'], index['E'], 5)
    g.adjacent(index['C'], index['F'], 12)
    g.adjacent(index['C'], index['G'], 2)
    g.adjacent(index['D'], index['C'], 2)
    g.adjacent(index['D'], index['G'], 5)
    g.adjacent(index['E'], index['H'], 4)
    g.adjacent(index['E'], index['F'], 7)
    g.adjacent(index['F'], index['I'], 6)
    g.adjacent(index['F'], index['J'], 4)
    g.adjacent(index['G'], index['F'], 3)
    g.adjacent(index['G'], index['J'], 6)
    g.adjacent(index['H'], index['I'], 1)
    g.adjacent(index['J'], index['I'], 7)
    g.define_start(index['A'])

    units = []
    for i in range(120):
        units.append(Unit(g))

    iteration = 0
    while iteration < 1000:
        for u in units:
            u.step()
        g.update()
        iteration += 1

    print_graph(g, index, symbol, units)

main()