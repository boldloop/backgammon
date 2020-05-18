#!/bin/env python3
# -*- coding: utf-8 -*-
#
# Authors:     GB
# Maintainers: GB
# License:     2020, Gus Brocchini, GPL v2 or later
# ===========================================
# ANN.py


import numpy as np


def sigmoid(array):
    return 1 / (1 + np.exp(-array))


def d_sigmoid(array):
    return sigmoid(array) * (1 - sigmoid(array))


class ANN:
    def __init__(self, shape=None, weights=None):
        if shape is None and weights is None:
            raise ValueError("either pass shape or weights")
        elif weights is not None:
            self.weights = weights.copy()
        else:
            self.gen_weights(shape)

    def gen_weights(self, shape):
        weights = []
        for i in range(len(shape) - 1):
            weights.append(np.random.rand(shape[i], shape[i+1]) - .5)
        self.weights = weights

    def get_weights(self):
        return np.concatenate([a.reshape(-1) for a in self.weights])

    def set_weights(self, weight_vector):
        for i in len(self.weights):
            shape = self.weights[i].shape
            n = np.prod(shape)
            self.weights[i] = weight_vector[:n].reshape(shape)
            weight_vector = np.delete(weight_vector, range(n))

    def eval(self, inputs):
        self.last_activations = [inputs]
        for weight_array in self.weights:
            next_activations = sigmoid(np.matmul(inputs, weight_array))
            self.last_activations.append(next_activations)
        return self.last_activations[-1]

    def __call__(self, inputs):
        return self.eval(inputs)


# done.
