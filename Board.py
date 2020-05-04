#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# Board.py


switch_color = {'white': 'black', 'black': 'white'}


def _poss_move_groups(side_dict, n_rolls):
    side_dict = side_dict.copy()
    try:
        side_dict.pop(0)
    except KeyError:
        pass

    if 25 in side_dict:  # if there are pieces on the bar
        bar = side_dict.pop(25)
        if bar > n_rolls:
            return {(25,) * n_rolls}
        else:
            other_groups = _poss_move_groups(side_dict, n_rolls - bar)
            return set([(25,) * bar + other for other in other_groups])
    else:
        if n_rolls <= 0:
            return [()]  # list of one empty tuple
        elif n_rolls >= sum(side_dict.values()):
            out_tup = tuple()
            for point in side_dict:
                out_tup += (point,) * side_dict[point]
            return out_tup
        else:
            points = side_dict.keys()
            move_groups = list()
            for point in points:
                tmp = side_dict.copy()
                tmp[point] -= 1
                if tmp[point] == 0:
                    tmp.pop(point)
                other_groups = _poss_move_groups(tmp, n_rolls - 1)
                move_groups.extend([(point,) + other
                                    for point in points
                                    for other in other_groups])
            return set(move_groups)


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
