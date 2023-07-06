
import numpy
matrix = [0] * 64
for i in range(0,64):
    matrix[i] = numpy.random.randint(50,54)


# Debug
def show(block_list):
    for i in range(0,8):
        k = ''
        for j in range(0,8):
            m = str(int(block_list[i*8 + j]))
            k += ' ' * (4-len(m)) + m + ' '
        print(k)
    print()


# Discrete Cosine Transform (32-bit Integer Only Version: Standered)
def dct1(s:list):
    
    # 2^16 = 65536
    pi_mul_2  = 411775 # pi << 16 * 2
    pi        = 205887 # pi << 16
    pi_div_2  = 102944 # pi << 16 / 2
    pi_div_16 = 12868  # pi << 16 / 16
    k = 39797 # 0.6072529350088812561694 << 16
    # CORDIC variation of the angle: 0.7853982, 0.4636476, 0.2449787, 0.1243550, 0.0624188, 0.0312398, 0.0156237
    sigma = [51471 , 30385 , 16054 , 8149 , 4090 , 2047 , 1023]

    # CORDIC cosine function
    def cos(target:int): # target been << 16

        # constraint in -pi/2 ~ pi/2
        inverse = False
        while target > pi:
            target -= pi_mul_2
        if target > pi_div_2:
            inverse = True
            target -= pi
        elif target < - pi_div_2:
            inverse = True
            target += pi
        
        theta = 0 # Initial angle: 0 degree
        direction = [0, 0, 0, 0, 0, 0, 0] # clockwise is 1, anticlockwise is -1
        i = 0 # iteration of the routation direction
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
                x = x - (y >> i)
                y = (x >> i) + y
            else:
                x = x + (y >> i)
                y = - (x >> i) + y
            i -= 1
        # return cosine result
        if inverse:
            return - x # integer been << 16 bit
        else:
            return   x # integer been << 16 bit
        
    S = [0] * 64
    for u in range(0,8):
        if u == 0:
            Cu = 46341 # 1/root(2) << 16
        else:
            Cu = 65536 # 1 << 16
        for v in range(0,8):
            if v == 0:
                Cv = 46341
            else:
                Cv = 65536
            unit = 0
            for x in range(0,8):
                for y in range(0,8):
                    temp = s[y + x * 8]
                    temp = (temp * cos((2*x + 1) * u * pi_div_16)) >> 8
                    temp = (temp * cos((2*y + 1) * v * pi_div_16)) >> 8
                    unit += temp
            temp = (Cu * Cv) >> 16
            temp = (temp * unit) >> (32 + 2) # divide 4
            if temp < 0:
                temp += 1
            S[v + u * 8] = temp
    return S # integer matrix

# Discrete Cosine Transform 
# Need more effort to perform an 32-bit integer multiplication to replace 32-bit float multiplication
def dct2(s:list):
    from math import cos
    from math import pi
    S = [0] * 64
    for u in range(0,8):
        if u == 0:
            Cu = 0.707106781187
        else:
            Cu = 1
        for v in range(0,8):
            if v == 0:
                Cv = 0.707106781187
            else:
                Cv = 1
            unit = 0
            for x in range(0,8):
                for y in range(0,8):
                    unit += s[y + x * 8] * cos(((2*x + 1) * u * pi) / 16) * cos(((2*y + 1) * v * pi) / 16)
            S[v + u * 8] = (1/4) * Cu * Cv * unit
    return S

show(dct1(matrix))
show(dct2(matrix))
