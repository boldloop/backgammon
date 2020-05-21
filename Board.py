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


def test_group(group, side):
    enough = all([side[point] >= group.count(point) for point in set(group)])
    bar = side.get(25, 0) == group.count(25) or set(group) == {25}
    return enough and bar


def execute_move(point_paths, side, opp):
    # point_paths is [(point, nums to move piece)]
    # e.g. a point_path would be (23, (2, 3))
    # to move a piece on the 23-point 2 and then 3 (hitting on the 21- and 18-)
    future_side, future_opp = side.copy(), opp.copy()
    for point, path in point_paths:
        future_side[point] -= 1
        if future_side[point] == 0:
            future_side.pop(point)

        final = point - sum(path)
        if final < 0:
            if max(future_side) <= point <= 6:
                future_side[0] = future_side.get(0, 0) + 1
            else:
                return
        elif final == 0:
            if max(future_side) <= 6:
                future_side[0] = future_side.get(0, 0) + 1
            else:
                return
        else:
            future_side[final] = future_side.get(final, 0) + 1

        pos = point
        for num in path:
            pos -= num
            try:
                future_opp.pop(25 - pos)
                future_opp[25] = future_opp.get(25, 0) + 1
            except KeyError:
                pass
    return future_side, future_opp


def dedup_moves(moves):
    # moves is a list of dicts of dicts of ints. nice.
    # one move is {'white': {1: 3}, 'black': {4: 2}}
    # the list comp below only returns an item if it isn't in the
    # later values of the list.
    # so, it only returns one copy of each unique move.
    # preferred over set-based solutions because a dict of dicts is a pain
    # to make hashable.
    return [move for i, move in enumerate(moves) if move not in moves[i+1:]]


def str_from_board(board):
    # temp str function until I manage to do a fancier one
    out_strs = []
    for i in range(26):
        white = "w" * board['white'].get(i, 0)
        black = "b" * board['black'].get(25 - i, 0)

        if i == 0:
            out_strs.append(f'white borne: {white} | black bar: {black}')
        elif i == 25:
            out_strs.append(f'black borne: {black} | white bar: {white}')
        else:
            out_strs.append(white + black)

        if i % 6 == 0:
            out_strs.append('------')

    return '\n'.join(out_strs)


def end(board):
    win = None
    for color in ['white', 'black']:
        if set(board[color].keys()) == {0}:
            win = color
    if win is None:
        return win
    else:
        opp = board[switch_color[win]]
        gammon = int(opp.get(0, 0) == 0)
        backgammon = int(max(opp) > 25-7) * gammon
        seq = [1, gammon, backgammon]
        if win == 'white':
            return seq + [0]*3
        else:
            return [0]*3 + seq


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
        if roll[0] == roll[1]:
            return self.doubleMoves(roll[0], color)
        else:
            return self.mixedMoves(roll, color)

    def doubleMoves(self, num, color):
        side = self.getBoard()[color]
        opp_side = self.getBoard()[switch_color[color]]
        # n_val is the number of jumps a piece can make
        # so if a piece is on the 23-point, and the 19-, 15- and 11- points
        # are able to be moved to, but the 7- is not (assuming double 4s)
        # point_from_n_val would have {1: [..., 23], 2: [..., 23],
        #                              3: [..., 23], 4: [...]}
        # because a piece on the 23-point could move 1, 2, or 3 4s.
        point_from_n_val = {1: list(), 2: list(), 3: list(), 4: list()}
        for point in side:
            if point != 0:
                for i in range(1, 5):
                    if opp_side.get(25 - (point - i * num), 0) > 1:
                        break
                    else:
                        point_from_n_val[i].append(point)

        moves = list()
        # a move_type is how the move is split between pieces.
        # (4,) means that one piece moves 4 times
        # (3, 1) means one moves 3 times and one moves once
        # (1, 1, 1, 1) means 4 pieces move once, etc.
        for move_type in [(4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)]:
            list_for_product = [point_from_n_val[i] for i in move_type]
            groups = itertools.product(*list_for_product)

            for group in groups:
                if test_group(group, side):
                    point_paths = [(point, (num,) * n_val)
                                   for point, n_val in zip(group, move_type)]
                    futures = execute_move(point_paths, side, opp_side)
                    if futures is not None:
                        moves.append({color: futures[0],
                                      switch_color[color]: futures[1]})

        return dedup_moves(moves)

    def mixedMoves(self, roll, color):
        side = self.getBoard()[color]
        opp_side = self.getBoard()[switch_color[color]]
        points_from_num = dict()
        for num in roll + (sum(roll),):
            points_from_num[num] = [point for point in side
                                    if opp_side.get(25 - (point-num), 0) <= 1]

        groups = itertools.product(points_from_num[roll[0]],
                                   points_from_num[roll[1]])
        moves = list()
        for group in groups:
            if test_group(group, side):
                point_paths = list(zip(group, [(die,) for die in roll]))
                futures = execute_move(point_paths, side, opp_side)
                if futures is not None:
                    moves.append({color: futures[0],
                                  switch_color[color]: futures[1]})

        for point in points_from_num[sum(roll)]:
            if test_group((point,), side):
                for die in roll:
                    if point in points_from_num[die]:
                        point_paths = [(point, (die, sum(roll) - die))]
                        futures = execute_move(point_paths, side, opp_side)
                        if futures is not None:
                            moves.append({color: futures[0],
                                          switch_color[color]: futures[1]})

        return dedup_moves(moves)

    def end(self, board=None):
        board = board if board is not None else self.getBoard()
        return end(board)

    def __str__(self):
        return str_from_board(self.getBoard())


if __name__ == '__main__':
    board = Board()
    print(board)
    moves = board.getMoves((1, 1), 'white')
    # for move in moves:
    #     print(str_from_board(move))

# done.
