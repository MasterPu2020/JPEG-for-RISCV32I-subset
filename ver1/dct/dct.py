# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/21
# Python DCT-II algorithm verification
# Clark Pu
# -------------------------------------

import numpy
import math

def cordic_cos(angle):
    k = 0.6072529350088812561694
    target = angle
    inverse = False
    while target > 3.14:
        target -= 3.14 * 2
    if target > 3.14 / 2:
        inverse = True
        target -= 3.14
    elif target < - 3.14 / 2:
        inverse = True
        target += 3.14
    sigma = [0.7853982, 0.4636476, 0.2449787, 0.1243550, 0.0624188, 0.0312398, 0.0156237]
    theta = 0
    direction = 1
    rotation_matrix = numpy.identity(2)
    for i in range(0,7):
        if theta > target:
            theta -= sigma[i]
            direction = 1
        else:
            theta += sigma[i]
            direction = - 1
        rotation_matrix = rotation_matrix.dot(numpy.matrix([[1, - direction * pow(2, - i)], [direction * pow(2, - i), 1]]))
    result_matrix = rotation_matrix.dot(numpy.matrix([[k], [0]])) # [[cos], [-sin]]
    if inverse:
        result = - result_matrix[0,0]
    else:
        result = result_matrix[0,0]
    # < Debug
    error = round(math.cos(angle) - result, 4)
    if error > 0.05:
        print('Input angle is ', target, angle, ' = ', target * 180 / 6.28, angle * 180 / 6.28, 'degree')
        print('Math COS: ', math.cos(angle), 'CORDIC COS: ', result)
        print('Error = ', error)
    # Debug >
    return result


# generate an 8x8 block sample
f = numpy.random.randint(-128,127,(8,8))
print('\nOriginal sample is:\n', f)

a = numpy.zeros((8,8))

for i in range(0,7):
    if i == 0:
        c = math.sqrt(1/8)
    else:
        c = math.sqrt(2/8)
    for j in range(0,7):
        a[i + 1, j + 1] = c * cordic_cos(math.pi * (j + 1/2) * i / 4)

# print('Matrix A is:\n', a)
# print("Matrix A' is:\n", a.T)

dct_f = a.dot(f).dot(a.T) # F = a·f·a' (这里F为变量dct_f)
dct_f = numpy.fix(dct_f)

print('\nDCT Matrix is:\n', dct_f)

from scipy import fftpack
new_dct_f = fftpack.dct(fftpack.dct(f[0:8, 0:8], norm='ortho').T, norm='ortho').T
print('\nDCT Matrix is:\n', numpy.fix(new_dct_f))