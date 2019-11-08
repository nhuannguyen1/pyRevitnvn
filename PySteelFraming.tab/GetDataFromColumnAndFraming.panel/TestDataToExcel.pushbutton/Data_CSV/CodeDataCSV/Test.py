matr_= [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]
rotated90 = zip(*matr_[::1])
print (list(rotated90))