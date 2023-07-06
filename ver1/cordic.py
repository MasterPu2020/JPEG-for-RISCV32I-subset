# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/21
# Python Coordinate rotation digital algorithm
# Precision = 0.1
# Clark Pu
# -------------------------------------

def cos(target):

    # 约至规定区间: -pi/2 ~ pi/2
    inverse = False
    pi = 3.1415926535897932384626
    while target > pi:
        target -= pi * 2
    if target > pi / 2:
        inverse = True
        target -= pi
    elif target < - pi / 2:
        inverse = True
        target += pi

    # 系数K
    k = 0.6072529350088812561694
    # 角变化量
    sigma = [0.7853982, 0.4636476, 0.2449787, 0.1243550, 0.0624188, 0.0312398, 0.0156237]
    # 初始角度：0度
    theta = 0
    # 方向：顺时针为1，逆时针为-1
    direction = [0, 0, 0, 0, 0, 0, 0]

    # 判断旋转方向，迭代旋转角度
    i = 0
    while i != 7:
        if theta > target:
            theta -= sigma[i] # 顺时针旋转
            direction[i] = 1
        else:
            theta += sigma[i] # 逆时针旋转
            direction[i] = - 1
        i += 1

    # 向量旋转迭代，2次方运算仅需使用2进制位移来完成
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
    
    # 返回计算结果
    if inverse:
        return - x
    else:
        return x


# # Debug:
# import math
# import random
# number = random.random() * 8 * math.pi
# cos_result = cos(number)
# cos_answer = math.cos(number)
# print("COS should be ", round(cos_answer,3), "\nCORDIC result is ", round(cos_result, 3))
