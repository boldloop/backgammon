#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# Board.py


switch_color = {'white': 'black', 'black': 'white'}


def str_ix_from_piece(point, num, color):
    if point == 0:
        base_y = {'white': 3, 'black': 12}[color]
        y = base_y + num // 5
        x = 56 + (num % 5)
        return x, y

    if point == 25:
        x = 26
        if color == 'white':
            y = 15 - num
        else:
            y = 2 + num
        return x, y

    point = 25 - point if color == 'black' else point
    if 1 <= point <= 12:
        y = 2 + num
    elif point <= 24:
        y = 15 - num
        point = 25 - point

    if point <= 6:
        x = 50 - 4*(point - 1)
    else:
        x = 22 - 4*((point - 1) % 6)

    return x, y


def str_from_board(board):
    starting_str = ''' 12  11  10   9   8   7       6   5   4   3   2   1
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                       |   |                       | W's home
|                       |   |                       | |       |
|                       |   |                       | |       |
|                       |   |                       | |       |
|                       |   |                       |
|                       |   |                       |
|                       |   |                       |
|                       |   |                       |
|                       |   |                       |
|                       |   |                       |
|                       |   |                       | |       |
|                       |   |                       | |       |
|                       |   |                       | |       |
|                       |   |                       | B's home
+---+---+---+---+---+---+---+---+---+---+---+---+---+
 13  14  15  16  17  18      19  20  21  22  23  24'''

    out = starting_str.split('\n')
    out = [list(line) for line in out]
    for color in ['white', 'black']:
        char = color[0].upper()
        for point in board[color]:
            for num in range(board[color][point]):
                x, y = str_ix_from_piece(point, num, color)
                out[y][x] = char

    out = [''.join(line) for line in out]
    return '\n'.join(out)


# need to call with every order
# generates superset of valid plays, playing the numbers in the order listed
# doesn't check for maximum part of roll
# to return: list of list of moves (in the berliner sense)
# e.g., [[(25, 5), (20, 3)], [(25, 3), (13, 5)]]
#         25/17               25/22, 13/8
def play_gen(board, nums, color):
    if len(nums) == 0:
        return [[]]

    side, opp = board[color].copy(), board[switch_color[color]].copy()
    num = nums[0]
    nums = nums[1:]

    # if on bar
    if side.get(25, 0) > 0:
        if opp.get(num, 0) > 1:
            return [[]]
        elif opp.get(num, 0) == 1:
            opp[25] = opp.get(25, 0) + opp.pop(num)

        side[25] -= 1
        if side[25] == 0:
            side.pop(25)
        side[25 - num] = side.get(25 - num, 0) + 1
        board = {color: side, switch_color[color]: opp}
        return [[(25, num)] + moves for moves
                in play_gen(board, nums, color)]

    plays = [[]]
    can_bear_off = max(side) <= 6

    # all moves where not bearing off
    for point in side:
        point_bear_off = (num == point or point == max(side)) and can_bear_off
        dest = point - num
        opp_on_dest = opp.get(25 - dest, 0)
        if opp_on_dest <= 1 and (dest > 0 or point_bear_off):
            f_side, f_opp = side.copy(), opp.copy()
            if opp_on_dest == 1:
                f_opp[25] = f_opp.get(25, 0) + f_opp.pop(25 - dest)

            dest = dest if dest >= 0 else 0
            f_side[point] -= 1
            if f_side[point] == 0:
                f_side.pop(point)
            f_side[dest] = f_side.get(dest, 0) + 1
            f_board = {color: f_side, switch_color[color]: f_opp}
            point_plays = [[(point, num)] + moves for moves
                           in play_gen(f_board, nums, color)]
            plays.extend(point_plays)

    return plays


def usage(play):
    return sum([num for point, num in play])


def sort_play(play):
    return tuple(sorted(play, key=lambda x: x[0], reverse=True))


def check_plays(all_plays):
    usage_list = [(play, usage(play)) for play in all_plays]
    max_usage = max([play_usage for play, play_usage in usage_list])
    valid_plays = {sort_play(play) for play, play_usage in usage_list
                   if play_usage == max_usage}
    return list(valid_plays)


def state_from_play(board, play, color):
    if len(play) == 0:
        return board

    point, num = play[0]
    play = play[1:]
    side, opp = board[color].copy(), board[switch_color[color]].copy()

    side[point] -= 1
    if side[point] == 0:
        side.pop(point)

    dest = point - num
    if dest <= 0:
        side[0] = side.get(0, 0) + 1
    else:
        side[dest] = side.get(dest, 0) + 1
        if opp.get(25 - dest, 0) == 1:
            opp[25] = opp.get(25, 0) + opp.pop(25 - dest)

    f_board = {color: side, switch_color[color]: opp}
    return state_from_play(f_board, play, color)


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
            rolls = [roll*2]
        else:
            rolls = [roll, tuple(reversed(roll))]

        plays = []
        board = self.getBoard()
        for roll in rolls:
            plays.extend(play_gen(board, roll, color))
        plays = check_plays(plays)

        after_states = [state_from_play(board, play, color) for play in plays]
        return after_states

    def end(self):
        return end(self.getBoard())

    def __str__(self):
        return str_from_board(self.getBoard())


if __name__ == '__main__':
    board = Board()
    print(board)
    moves = board.getMoves((1, 1), 'white')
    # for move in moves:
    #     print(str_from_board(move))

# done.
