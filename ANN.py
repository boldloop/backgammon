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
        return np.concatenate(self.weights, axis=None)

    def set_weights(self, weight_vector):
        for i in range(len(self.weights)):
            shape = self.weights[i].shape
            n = np.prod(shape)
            self.weights[i] = weight_vector[:n].reshape(shape)
            weight_vector = np.delete(weight_vector, range(n))

    def gradient(self, inputs):
        activations = [inputs]
        weighted_sums = []
        for weight_array in self.weights:
            z_layer = np.matmul(activations[-1], weight_array)
            weighted_sums.append(z_layer)
            a_layer = sigmoid(z_layer)
            activations.append(a_layer)

        # partial a / partial z
        pa_pz = [d_sigmoid(zs) for zs in weighted_sums]

        # partial z / partial w
        # this is a three-dimensional array
        # roughly: (previous a layer, next a layer, next z layer)
        # this means that the 2d-matrix given from a z-coordinate
        # corresponds with the weights
        pz_pw = []
        for a_layer, weights in zip(activations[:-1], self.weights):
            prev_len, next_len = weights.shape
            layer = np.zeros((prev_len, next_len, next_len))
            for i in range(next_len):
                layer[:, i, i] = a_layer
            pz_pw.append(layer)

        # partial z / partial a (on prev layer)
        pz_pa = self.weights

        # single layer pa_pw
        # derivatives of an activation wrt to the weights directly before it
        # 3-d shape
        single_pa_pw = []
        for pa_pz_layer, pz_pw_layer in zip(pa_pz, pz_pw):
            pa_pz_layer = list(pa_pz_layer)
            layer = np.ndarray(pz_pw_layer.shape)
            for i in range(len(pa_pz_layer)):
                layer[:, :, i] = pa_pz_layer[i] * pz_pw_layer[:, :, i]
            single_pa_pw.append(layer)

        # derivative of an activation wrt to a previous layer's activation
        # same shape as weights (prev layer x cur layer)
        pa_pam1 = []
        for pz_pa_layer, pa_pz_layer in zip(pz_pa, pa_pz):
            # pa_pz is 1-d. (num in current layer)
            # pz_pa is 2-d. (prev layer x cur layer) -- same as weights.
            pa_pz_layer = list(pa_pz_layer)
            layer = np.matmul(pz_pa_layer, np.diag(pa_pz_layer))
            pa_pam1.append(layer)

        # derivative of final activation layer wrt to all layers' activations
        # shape is (prev layer x final layer)
        rev_paL_pa = []
        for i in range(len(pa_pam1) - 1, -1, -1):
            if rev_paL_pa == []:
                rev_paL_pa.append(pa_pam1[i])
            else:
                # pa_pam1[i] is shape (layer i x layer i+1)
                # rev_paL[-1] is shape (layer i+1 x final layer)
                # result is (layer i x final layer)
                layer = np.matmul(pa_pam1[i], rev_paL_pa[-1])
                rev_paL_pa.append(layer)
        paL_pa = list(reversed(rev_paL_pa))

        # now doing full pa_pw
        pa_pw = []
        # the indexing here is because, moving backwards, you want
        # the chain rule to work out.
        # so the pa_pw needs to match with the previous paL_pa.
        # the first item in paL_pa is wrt to the inputs, which is never used.
        # the last item in single_pa_pw is already done,
        # so I append at the end.
        num_aL = len(activations[-1])
        for paL_pa_layer, pa_pw_layer in zip(paL_pa[1:], single_pa_pw[:-1]):
            pa_pw_layer = np.sum(pa_pw_layer, axis=2)
            layer = np.ndarray(pa_pw_layer.shape + (num_aL,))
            for i in range(num_aL):
                aL_diag = np.diag(list(paL_pa_layer[:, i]))
                layer[:, :, i] = np.matmul(pa_pw_layer, aL_diag)
            pa_pw.append(layer)
        pa_pw.append(single_pa_pw[-1])
        pa_pw = [a.reshape(-1, num_aL) for a in pa_pw]
        pa_pw = np.concatenate(pa_pw, axis=0)
        return pa_pw

    def eval(self, inputs):
        a_layer = inputs
        for weight_array in self.weights:
            a_layer = sigmoid(np.matmul(a_layer, weight_array))
        return a_layer

    def __call__(self, inputs):
        return self.eval(inputs)


# done.
