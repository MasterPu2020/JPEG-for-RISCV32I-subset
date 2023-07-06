# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/29
# Python basic math
# Clark Pu
# -------------------------------------

pi = 3.1415926535897932384626

# define an zero matrix : NOT AN INTERGREATE FUNCTION
def zero(x, y):
    return [[0 for i in range(x)] for j in range(y)]


# Shape a vector into 8x8 matrix : NOT AN INTERGREATE FUNCTION
def shape2m(vector):
    if len(vector) == 64:
        x = 0
        y = 0
        matrix = zero(8, 8)
        while y != 8:
            while x != 8:
                matrix[y][x] += vector[y * 8 + x]
                x += 1
            y += 1
            x = 0
        return matrix
    else:
        return False


# Shape a 8x8 matrix into vector : NOT AN INTERGREATE FUNCTION
def shape2v(matrix):
    vector = []
    x = 0
    y = 0
    while y != 8:
        while x != 8:
            vector.append(matrix[y][x])
            x += 1
        y += 1
        x = 0
    return vector


# Format print a verctor in a matrix style : NOT AN INTERGREATE FUNCTION
def display(vector, space, enter):
    i = 0
    line = ''
    for number in vector:
        number = str(number)
        while len(number) < space:
            number = ' ' + number
        line += number
        i += 1
        if i >= enter:
            i = 0
            print(line)
            line = ''
    if line != '':
        print(line)


def dis_block(matrix, space):
    for x in range(0,len(matrix)):
        line = ''
        for y in range(0,len(matrix[x])):
            string = str(matrix[x][y])
            for i in range(0, space - len(string)):
                string = ' ' + string
            line += string
        print(line)
    print()


# 8x8 matrix dot
def dot(matrix_l, matrix_r):
    x = 0
    y = 0
    matrix = zero(8, 8)
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
def op(matrix_8x8, integer, option):
    x = 0
    y = 0
    matrix = zero(8, 8)
    while y != 8:
        while x != 8:
            if option == '-':
                matrix[y][x] = matrix_8x8[y][x] - integer
            elif option == '+':
                matrix[y][x] = matrix_8x8[y][x] + integer
            elif option == '*':
                matrix[y][x] = matrix_8x8[y][x] * integer
            elif option == '/':
                matrix[y][x] = matrix_8x8[y][x] / integer
            elif option == 't':
                matrix[y][x] = matrix_8x8[x][y]
            elif option == 'int':
                matrix[y][x] = int(matrix_8x8[y][x])
            x += 1
        y += 1
        x = 0
    return matrix


# 8x8 matrix divide by 8x8 matrix
def op_block(matrix_l, matrix_r, option):
    x = 0
    y = 0
    matrix = zero(8, 8)
    while y != 8:
        while x != 8:
            if option == '-':
                matrix[y][x] = matrix_l[y][x] - matrix_r[y][x]
            elif option == '+':
                matrix[y][x] = matrix_l[y][x] + matrix_r[y][x]
            elif option == '*':
                matrix[y][x] = matrix_l[y][x] * matrix_r[y][x]
            elif option == '/':
                matrix[y][x] = matrix_l[y][x] / matrix_r[y][x]
            x += 1
        y += 1
        x = 0
    return matrix


# CORDIC cosine
def cos(target):

    # import math
    # return math.cos(target)

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
