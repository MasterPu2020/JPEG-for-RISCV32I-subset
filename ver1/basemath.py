# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/24
# Python basic math
# Clark Pu
# -------------------------------------

pi = 3.1415926535897932384626

# define an zero matrix
def matrix_zero(x, y):
    return [[0 for i in range(x)] for j in range(y)]


# 8x8 matrix dot
def matrix_dot(matrix_l, matrix_r):
    x = 0
    y = 0
    matrix = matrix_zero(8, 8)
    while y != 8:
        while x != 8:
            index = 0
            while index != 8:
                matrix[y][x] += matrix_l[y][index] * matrix_r[index][x]
                index += 1
            x += 1
        y += 1
        x = 0
    return matrix


# 8x8 matrix constant operation
def matrix_op(matrix_8x8, integer, option):
    x = 0
    y = 0
    matrix = matrix_zero(8, 8)
    while y != 8:
        while x != 8:
            if option == '-':
                matrix[y][x] = matrix_8x8[y][x] - integer
            elif option == '*':
                matrix[y][x] = matrix_8x8[y][x] * integer
            elif option == 't':
                matrix[y][x] = matrix_8x8[x][y]
            elif option == 'int':
                matrix[y][x] = int(matrix_8x8[y][x])
            x += 1
        y += 1
        x = 0
    return matrix


# 8x8 matrix divide by 8x8 matrix
def matrix_div(matrix_l, matrix_r):
    x = 0
    y = 0
    matrix = matrix_zero(8, 8)
    while y != 8:
        while x != 8:
            matrix[y][x] = int(matrix_l[y][x] / matrix_r[y][x])
            x += 1
        y += 1
        x = 0
    return matrix


# CORDIC cosine
def cos(target):

    # constraint in -pi/2 ~ pi/2
    inverse = False
    while target > pi:
        target -= pi * 2
    if target > pi / 2:
        inverse = True
        target -= pi
    elif target < - pi / 2:
        inverse = True
        target += pi

    # parameter K6
    k = 0.6072529350088812561694
    # variation of the angle
    sigma = [0.7853982, 0.4636476, 0.2449787, 0.1243550, 0.0624188, 0.0312398, 0.0156237]
    # Initial angle: 0 degree
    theta = 0
    # direction: clockwise as 1, anticlockwise as -1
    direction = [0, 0, 0, 0, 0, 0, 0]

    # iteration of the routation direction
    i = 0
    while i != 7:
        if theta > target:
            theta -= sigma[i] # clockwise
            direction[i] = 1
        else:
            theta += sigma[i] # anticlockwise
            direction[i] = - 1
        i += 1

    # vector routation, 2 to the power using shift
    x = k
    y = 0
    i = 6
    while i != -1:
        if direction[i] == 1:
            x = x - (y * 2 ** ( - i))
            y = (x * 2 ** ( - i)) + y
        else:
            x = x + (y * 2 ** ( - i))
            y = (- x * 2 ** ( - i)) + y
        i -= 1
    
    # return cosine result
    if inverse:
        return - x
    else:
        return x

# get the bit length of an integer
def bit_length(integer):
    length = 0
    while integer > 0:
        integer = integer >> 1
        length += 1
    return length



# # Debug

# from PIL import Image
# import numpy

# rgb_img = Image.open('./develop/coffee.jpg')

# matrix_numpy0 = numpy.zeros((8,8))
# matrix_numpy1 = numpy.zeros((8,8))
# result_numpy = numpy.zeros((8,8))
# matrix0 = matrix_zero(8,8)
# matrix1 = matrix_zero(8,8)
# result = matrix_zero(8,8)

# def print_all():
#     print('matrix_numpy0 :\n', matrix_numpy0)
#     print('matrix_numpy1 :\n', matrix_numpy1)
#     print('result_numpy :\n', result_numpy)
#     print('matrix0 :')
#     for line in matrix0:
#         print(line)
#     print('matrix1 :')
#     for line in matrix1:
#         print(line)
#     print('result :')
#     for line in result:
#         print(line)
#     error = False
#     for cal in range(0,8):
#         for row in range(0,8):
#             if matrix_numpy0[cal,row] != matrix0[cal][row] or matrix_numpy1[cal,row] != matrix1[cal][row] or result_numpy[cal][row] != result[cal][row]:
#                 error = True
#     if error:
#         print('\nNot Equal!\n')
#     else:
#         print('\nEqual\n')

# for cal in range(0,8):
#     for row in range(0,8):
#         a = rgb_img.getpixel((cal, row))[0]
#         b = rgb_img.getpixel((cal, row))[1]
#         matrix_numpy0[cal,row] = a
#         matrix_numpy1[cal,row] = b
#         matrix0[cal][row] = a
#         matrix1[cal][row] = b

# result_numpy = matrix_numpy0.dot(matrix_numpy1)
# result = matrix_dot(matrix0,matrix1)

# # result_numpy = matrix_numpy0 * 10
# # result = matrix_mul(10, matrix0)

# # result_numpy = numpy.fix(result_numpy / matrix_numpy1)
# # result = matrix_div(result,matrix1)

# # result_numpy = result_numpy.T
# # result = matrix_t(result)

# print_all()