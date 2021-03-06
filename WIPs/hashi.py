#!/usr/bin/env python3
from enum import Enum

# noinspection PyArgumentList
DIRECTION = Enum('directions', 'N W E S')

V_BAR = '|'
V_BAR_2 = u'\u2016'
H_BRIDGE = '-'
H_BRIDGE_2 = u'\u1234'
BLANK = '.'


class Bridge:
    def __init__(self, direction, island_1, island_2):
        self.direction = direction
        self.island_1 = island_1
        self.island_2 = island_2
        self.weight = 0

    def __add__(self, other):
        self.weight += other

    def __str__(self):
        if self.weight == 0:
            return BLANK
        if self.weight == 1:
            return V_BAR if self.direction in (DIRECTION.N, DIRECTION.S) else H_BRIDGE
        if self.weight == 2:
            return V_BAR_2 if self.direction in (DIRECTION.N, DIRECTION.S) else H_BRIDGE_2
        raise RuntimeError("Count and direction `!r}`, `{!r}` invalid".format(self.weight, self.direction))


def main(puzzle, show_work=True):
    while not puzzle.solved():
        if show_work:
            print(puzzle.ascii_display())
        puzzle.iterate_solution()


class Hashi:
    def __init__(self, dims=(None, None), *islands):
        self.islands = {}
        self.iterations = 0
        self.dims = (None, None)
        for island in islands:
            self._add_island(island)

    def __repr__(self):
        return '<Hashi puzzle>'

    def _add_island(self, island, overwrite=False):
        if island.position in self.islands and not overwrite:
            raise RuntimeError('Island in position {} already present'.format(island.position))
        self.islands[island.position] = island

    @classmethod
    def from_string(cls, s):
        hashi = Hashi()
        width, height = 0, 0
        for j, row in enumerate(s.split('\n')):
            for i, entry in enumerate(row):
                if entry.isnumeric():
                    island = HashiIsland(int(entry), (i, j))
                    hashi._add_island(island)
                    width = width if width > i else i
                    height = height if height > j else j
        hashi.dims = (width, height)
        return hashi

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            s = f.readlines()
            return cls.from_string('\n'.join(s))

    def solved(self):
        pass

    def ascii_display(self):
        pass

    def iterate_solution(self):
        self.iterations += 1


class HashiIsland:
    def __init__(self, capacity, position):
        self.capacity = capacity
        self.remaining_stubs = capacity
        self.position = position
        self.edges = {k: 0 for k in DIRECTION}
        self.neighbor = {}

    def __repr__(self):
        return '<HashiIsland {}>'.format(self.position)


if __name__ == '__main__':
    tst = ('2...3\n'
           '....1\n'
           '1....')
    hashi = Hashi.from_string(tst)
    print(hashi)
