# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/29
# Python 8x8 Image block functions
# Clark Pu
# -------------------------------------


import basemath
import math


# s must be a 8x8 matrix
# Discrete Cosine Transform
def fdct(s):
    S = basemath.zero(8,8)
    for u in range(0,8):
        if u == 0:
            Cu = math.sqrt(1/2)
        else:
            Cu = math.sqrt(2/2)
        for v in range(0,8):
            if v == 0:
                Cv =  math.sqrt(1/2)
            else:
                Cv = math.sqrt(2/2)
            unit = 0
            for x in range(0,8):
                for y in range(0,8):
                    unit += s[y][x] * math.cos(((2*x + 1) * u * math.pi) / 16) * math.cos(((2*y + 1) * v * math.pi) / 16)
            S[v][u] = (1/4) * Cu * Cv * unit
    return S


# Discrete Cosine Transform
def idct(S):
    s = basemath.zero(8,8)
    for x in range(0,8):
        for y in range(0,8):
            unit = 0
            for u in range(0,8):
                for v in range(0,8):
                    if u == 0:
                        Cu = math.sqrt(1/2)
                    else:
                        Cu = math.sqrt(2/2)
                    if v == 0:
                        Cv =  math.sqrt(1/2)
                    else:
                        Cv = math.sqrt(2/2)
                    unit += S[v][u] * Cu * Cv * math.cos(((2*x + 1) * u * math.pi) / 16) * math.cos(((2*y + 1) * v * math.pi) / 16)
            s[y][x] = (1/4) *  unit
    return s


# z must be a 8x8 matrix
def zigzag_scan(z):
    x = 0
    y = 0
    i = 0
    zigzag_list = [0] * 64
    direction = 1
    is_edge = False
    zigzag_list[0] = z[0][0]
    while True:
        if x == 0 or x == 7:
            y += 1
            is_edge = True
        elif y == 0 or y == 7:
            x += 1
            is_edge = True

        if is_edge:
            is_edge = False
            direction = - direction
            i += 1
            zigzag_list[i] = z[x][y]

        if x == 7 and y == 7:
            return zigzag_list
        
        i += 1
        x -= direction
        y += direction
        zigzag_list[i] = z[x][y]


# block_list must be an integer list. EHUFCO EHUFSI tables are list, explained in itu-t81
def huffman_encode(block_list, DC_EHUFCO, DC_EHUFSI, AC_EHUFCO, AC_EHUFSI):
    
    # reverse if it is negtive
    def get_value(value):
        value_bin = ''
        if value != 0: # not empty
            if value < 0:
                for bit in bin(value)[2:]:
                    if bit == '1':
                        value_bin += '0'
                    else:
                        value_bin += '1'
            else:
                value_bin = bin(value)[2:]
        # print(value_bin) #Debug
        return value_bin
    
    # Look for the DC code
    def DC_code(value):
        length = len(value)
        code = bin(DC_EHUFCO[length])[2:]
        size = DC_EHUFSI[length]
        code = '0' * (size - len(code)) + code
        # print(code) #Debug
        return code
    
    # Look for the AC code
    def AC_code(zero_counter, value):
        length = (zero_counter << 4) + len(value) # EHUFCO[ZERO/VALUE]
        code = bin(AC_EHUFCO[length])[2:]
        size = AC_EHUFSI[length]
        code = '0' * (size - len(code)) + code
        # print(code) #Debug
        return code
    
    # DC code
    value = get_value(block_list[0])
    result = DC_code(value) + value
    
    # AC code
    zero_counter = 0
    for index in range(1,len(block_list)):
        if block_list[index] == 0:
            zero_counter += 1
        else:
            while zero_counter > 15: # zeros over than 15
                zero_counter -= 16
                result += AC_code(15,get_value(0)) # AC Luma EHUFCO[F/0]
            value = get_value(block_list[index])
            result += AC_code(zero_counter, value) + value
            zero_counter = 0
    
    # EOB
    result += AC_code(0,get_value(0)) # AC Luma EHUFCO[0/0]
    return result


# input should be integer
def rgb2ycbcr(red, green, blue):
    luminance        =  0.257 * red + 0.564 * green + 0.098 * blue + 16
    blue_chrominance = -0.148 * red - 0.291 * green + 0.439 * blue + 128
    red_chrominance  =  0.439 * red - 0.368 * green - 0.071 * blue + 128
    return [int(luminance), int(blue_chrominance), int(red_chrominance)]
