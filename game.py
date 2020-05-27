#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# game.py


from ANN import ANN
from Board import Board, state_from_play
from random import randint
from trainer import pick_move
import pickle


def get_roll():
    return (randint(1, 6), randint(1, 6))


def get_first_roll():
    roll = get_roll()
    while len(set(roll)) == 1:
        roll = get_roll()
    if max(roll) == roll[0]:
        return 'white', 'black', roll
    else:
        return 'black', 'white', roll


def print_on_roll(color, roll):
    print(f'{color} to play {roll}')


def play_from_input(board):
    try:
        u_input = input('Make your move: ')
        if u_input == 'quit':
            raise AssertionError('quit')
        elif u_input == 'print':
            print(board.getBoard())
        moves = u_input.split(',')
        pt_num_strs = [move.split('-') for move in moves]
        pt_num = [(int(pt_num_str[0]), int(pt_num_str[1]))
                  for pt_num_str in pt_num_strs]
        return False, pt_num
    except (ValueError, IndexError):
        return 'Move must be in form point-num, point-num', 0


def user_move(board, roll):
    moves = board.getMoves(roll, 'white')
    if moves == []:
        return

    while True:
        err, play = play_from_input(board)
        if err:
            print(err)
            continue
        else:
            try:
                afterstate = state_from_play(board.getBoard(), play, 'white')
                if afterstate in moves:
                    return afterstate
            except KeyError:
                pass
            print('Invalid move. Try again.')


def run_game(weights):
    print('You are playing white.')
    ann = ANN(weights=weights)
    board = Board()
    color, opp_color, roll = get_first_roll()

    while board.end() is None:
        print(board)
        print_on_roll(color, roll)
        if color == 'white':
            afterstate = user_move(board, roll)
        else:
            afterstate = pick_move(board, ann, roll, 'black')

        if afterstate is None:
            print('No valid moves')
        else:
            board.setBoard(afterstate)

        roll = get_roll()
        color, opp_color = opp_color, color
    print(board)
    print(board.end())


if __name__ == '__main__':
    with open('weights/100k', 'rb') as weight_file:
        weights = pickle.load(weight_file)
    run_game(weights=weights)


# done.
