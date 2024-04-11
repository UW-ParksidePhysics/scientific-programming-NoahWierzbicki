import numpy as np
matrix = np.array([[0, 1], [1, 0]])
print(f'A = {matrix}')

determinant = np.linalg.det(matrix)
print(f'det(A) = {determinant}')
