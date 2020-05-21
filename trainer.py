#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# trainer.py

import numpy as np
from Board import Board
from ANN import ANN
import random
import pickle
import datetime


switch_color = {'white': 'black', 'black': 'white'}


def get_roll():
    return (random.randint(1, 6), random.randint(1, 6))


def inputs_from_side(side):
    side = side.copy()
    try:
        bar = side.pop(25)
    except KeyError:
        bar = 0
    try:
        off = side.pop(0)
    except KeyError:
        off = 0
    inputs = [off / 15]
    for i in range(1, 25):
        num = side.get(i, 0)
        pt_input = [0] * 4
        if num == 1:
            pt_input[0] = 1
        elif num == 2:
            pt_input[1] = 1
        elif num == 3:
            pt_input[2] = 1
        elif num > 3:
            pt_input[3] = (num - 3) / 2
        inputs.extend(pt_input)
    inputs.append(bar / 2)
    return inputs


def inputs_from_board(board, color):
    to_go = {'white': [1, 0], 'black': [0, 1]}
    inputs = (to_go[color]
              + inputs_from_side(board['white'])
              + inputs_from_side(board['black']))
    return inputs


def equity(ann, board, color):
    response = ann(inputs_from_board(board, color))
    white_equity = sum(response[:3]) - sum(response[3:])
    equity = {'white': white_equity, 'black': -white_equity}
    return equity[color]


def pick_move(board, ann, roll, color):
    moves = board.getMoves(roll, color)
    try:
        to_return = max(moves, key=lambda b: equity(ann, b, color))
        return to_return
    except ValueError:
        return


def run_game(ann, lambd, alpha):
    roll = get_roll()
    while len(set(roll)) == 1:
        roll = get_roll()
    if max(roll) == roll[0]:
        color = 'white'
    else:
        color = 'black'
    opp_color = switch_color[color]

    board = Board()

    # make first move
    board.setBoard(pick_move(board, ann, roll, color))
    color, opp_color = opp_color, color
    old_Y, z = ann.gradient(inputs_from_board(board.getBoard(), color))

    steps = 1

    while True:
        steps += 1
        roll = get_roll()
        move = pick_move(board, ann, roll, color)
        color, opp_color = opp_color, color
        if move is not None:
            board.setBoard(move)

        end = board.end()
        if end is not None:
            Y_error = (np.asarray(end).reshape(old_Y.shape)
                       - old_Y).reshape((6, 1))
            d_weights = alpha * np.matmul(z, Y_error)
            ann.set_weights(ann.get_weights() + d_weights)
            break

        new_Y, new_z = ann.gradient(inputs_from_board(board.getBoard(), color))
        Y_error = (new_Y - old_Y).reshape((6, 1))
        d_weights = alpha * np.matmul(z, Y_error)
        ann.set_weights(ann.get_weights() + d_weights)
        z = lambd * z + new_z
        old_Y = new_Y

    return steps


def train(n, weights=None):
    if weights is None:
        ann = ANN(shape=[198, 30, 30, 6])
    else:
        ann = ANN(weights=weights)
    start = datetime.datetime.now()
    print(start)
    for i in range(n):
        steps = run_game(ann, lambd=.7, alpha=.1)
        if i % 25 == 0:
            time_since = (datetime.datetime.now() - start).seconds
            if time_since != 0:
                print(i, time_since, i / time_since)
        with open('logs/games.txt', 'a') as games:
            games.write(f"{steps}\n")
        with open('logs/weights', 'wb') as weight_file:
            pickle.dump(ann.weights, weight_file)


if __name__ == '__main__':
    n = int(input('How many games to run? '))
    try:
        with open('logs/weights', 'rb') as weight_file:
            weights = pickle.load(weight_file)
        train(n, weights)
    except FileNotFoundError:
        train(n)

# done.
