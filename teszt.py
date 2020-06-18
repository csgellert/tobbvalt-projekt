import numpy as np

matrix = np.zeros((2,3))
print(matrix)

m = np.ones((6,))
print(type(m), m.shape)

matrix = np.matrix.flatten(matrix)
print(type(matrix), matrix.shape)

m[3:] = matrix[3:]
print(m)
