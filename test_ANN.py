import numpy as np
import ANN

ann = ANN.ANN(shape=[1, 2, 45, 2])

print(ann([1]))
for i in range(20):
    grad = ann.gradient([1])
    grad = np.matmul(grad, np.array([[1], [-1]]))
    to_set = grad + ann.get_weights().reshape(grad.shape)
    ann.set_weights(to_set)
    print(ann([1]))
