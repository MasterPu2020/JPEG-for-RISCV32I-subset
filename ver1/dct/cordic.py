# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/21
# Python Coordinate rotation digital algorithm
# Clark Pu
# -------------------------------------

import numpy
import random
import math

# number = random.random() * 8 * math.pi
number = 60 * math.pi / 180 # Debug

# 约至规定区间: -pi/2 ~ pi/2
inverse = False
target = number
while target > math.pi:
    target -= math.pi * 2
if target > math.pi / 2:
    inverse = True
    target -= math.pi
elif target < - math.pi / 2:
    inverse = True
    target += math.pi

# 计算系数K
k = 1
for i in range(0,7):
    k = k * (1 / math.sqrt(1 + pow(2, -2 * i)))
print("\nK6 is: ", k)

sigma = [0.7853982, 0.4636476, 0.2449787, 0.1243550, 0.0624188, 0.0312398, 0.0156237] # 角变化量
theta = 0 # 初始角度：0度
direction = 1 # 方向：顺时针为1，逆时针为-1
rotation_matrix = numpy.identity(2) # 单位矩阵
# vi = numpy.matrix([[1],[0]]) # [[x],[y]] # Debug
# 判断旋转方向，迭代旋转角度
for i in range(0,7):
    if theta > target:
        theta -= sigma[i] # 顺时针旋转
        direction = 1
    else:
        theta += sigma[i] # 逆时针旋转
        direction = - 1
    print(direction)
    # 向量旋转迭代，2次方运算仅需使用2进制位移来完成
    rotation_matrix = rotation_matrix.dot(numpy.matrix([[1, - direction * pow(2, - i)], [direction * pow(2, - i), 1]]))
    # <Debug
    # kj = 1
    # for j in range(0,i+1):
    #     kj = kj * (1 / math.sqrt(1 + pow(2, -2 * j)))
    # vi = (kj * rotation_matrix).dot(vi)
    
    # if i % 2 == 0:
    #     x_vi = vi[0,0]
    #     y_vi = vi[1,0]
    # else:
    #     x_vi = vi[1,0]
    #     y_vi = vi[0,0]
    # matrix_angle = math.atan(- y_vi / x_vi)
    # print("\n Rotation matrix ", i, " is:\n", rotation_matrix)
    # print('Matrix Angle is: ', matrix_angle / math.pi * 180, " degree. Theta is ", theta / math.pi * 180, 'degree')
    # print(matrix_angle, theta)
    # Debug>
result_matrix = rotation_matrix.dot(numpy.matrix([[k], [0]])) # [[cos], [sin]]
if inverse:
    result_cos = - result_matrix[0,0]
else:
    result_cos = result_matrix[0,0]

print("Input angle is: ", number / math.pi * 180, 'degree')
print('Target is ', target / math.pi * 180, 'degree')
print("Result angle is: ", theta / math.pi * 180, 'degree')
print("COS(Theta) should be ", math.cos(number), "\nCORDIC result is ", result_cos)
print("Error rate: ", abs((math.cos(number) - result_cos) / math.cos(number)) * 100, "%\n")
# print("\nAnswer to Input is:\n", numpy.matrix([[math.cos(target)], [math.sin(target)]]))
# print("\nAnswer to Theta is:\n", numpy.matrix([[math.cos(theta)], [math.sin(theta)]]))
# print("\nResult is:\n", result_matrix)
