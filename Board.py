#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# Board.py


import itertools


switch_color = {'white': 'black', 'black': 'white'}


def _poss_move_groups(side_dict, n_rolls):
    locs = []
    for loc in side_dict:
        if loc != 0:
            locs.extend([loc] * side_dict[loc])
    if len(locs) <= n_rolls:
        return {tuple(locs)}
    bar = side_dict.get(25, 0)
    bar_req = bar if bar < n_rolls else n_rolls
    return set([group for group in itertools.combinations(locs, n_rolls)
                if group.count(25) == bar_req])


class Board:
    def __init__(self):
        # dict from {point: num of pieces on point}
        # starting position here
        # for the purposes of this, the 0-point is off,
        # and the 25-point is the bar
        self.white = {24: 2, 13: 5, 8: 3, 6: 5}
        self.black = self.white.copy()

    def getBoard(self):
        return {'white': self.white, 'black': self.black}

    def setBoard(self, board):
        self.white = board['white']
        self.black = board['black']

    def getMoves(self, roll, color):
        pass
        # board = self.getBoard()
        # opp_color = switch_color[color]

    def __str__(self):
        # temp str function until I manage to do a fancier one
        out_strs = []
        for i in range(26):
            white = "w" * self.white.get(i, 0)
            black = "b" * self.black.get(25 - i, 0)

            if i == 0:
                out_strs.append(f'white borne: {white} | black bar: {black}')
            elif i == 25:
                out_strs.append(f'black borne: {black} | white bar: {white}')
            else:
                out_strs.append(white + black)

            if i % 6 == 0:
                out_strs.append('------')

        return '\n'.join(out_strs)


if __name__ == '__main__':
    board = Board()
    print(board)
    move_group_tests = [({0: 10, 1: 1, 2: 1}, 2),
                        ({1: 1, 2: 2}, 2),
                        ({1: 1, 2: 2}, 4),
                        ({1: 3, 2: 2}, 4),
                        ({1: 1, 2: 1, 25: 1}, 2),
                        ({1: 1, 25: 3}, 2)]
    for test in move_group_tests:
        print(test)
        print(_poss_move_groups(*test))

# done.
