# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/24
# Python 8x8 Image block functions
# Clark Pu
# -------------------------------------


import basemath


# f must be a 8x8 matrix
def dct(f):
    a = basemath.matrix_zero(8,8)
    for i in range(0,8):
        if i == 0:
            c = 0.35355339059327376 # sqrt(1/8)
        else:
            c = 0.5 # sqrt(2/8)
        for j in range(0,8):
            a[i][j] = c * basemath.cos(basemath.pi * (j + 1/2) * i / 8)
    result = basemath.matrix_dot(a,f)
    result = basemath.matrix_dot(result, basemath.matrix_op(a,0,'t'))
    result = basemath.matrix_op(result,0,'int')
    return result # F = a·f·a'


# q is 8x8 DCT matrix, method = 0 for luminance, 1 for chrominance
def quantization(q, method):

    luminance_quantization_table = [
    [16,  11,  10,  16,  24,  40,  51,  61],
    [12,  12,  14,  19,  26,  58,  60,  55],
    [14,  13,  16,  24,  40,  57,  69,  56],
    [14,  17,  22,  29,  51,  87,  80,  62],
    [18,  22,  37,  56,  68, 109, 103,  77],
    [24,  35,  55,  64,  81, 104, 113,  92],
    [49,  64,  78,  87, 103, 121, 120, 101],
    [72,  92,  95,  98, 112, 100, 103,  99]]
    
    chrominance_quantization_table = [
    [17,  18,  24,  47,  99,  99,  99,  99],
    [18,  21,  26,  66,  99,  99,  99,  99],
    [24,  26,  56,  99,  99,  99,  99,  99],
    [47,  66,  99,  99,  99,  99,  99,  99],
    [99,  99,  99,  99,  99,  99,  99,  99],
    [99,  99,  99,  99,  99,  99,  99,  99],
    [99,  99,  99,  99,  99,  99,  99,  99],
    [99,  99,  99,  99,  99,  99,  99,  99]]
    
    if method == 1:
        return basemath.matrix_div(q, luminance_quantization_table)
    else:
        return basemath.matrix_div(q, chrominance_quantization_table)


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


# block_list must be an integer list. EHUFCO table is list, explained in itu-t81
def huffman_encode(block_list, DC_EHUFCO, AC_EHUFCO):
    # DC code
    value = abs(block_list[0])
    length = basemath.bit_length(value)
    result = bin(DC_EHUFCO[length])[2:] + bin(value)[2:]
    # AC code
    zero_counter = 0
    for index in range(1,len(block_list)):
        if block_list[index] == 0:
            zero_counter += 1
        else:
            while zero_counter > 15: # zeros over than 15
                zero_counter -= 16
                result += bin(AC_EHUFCO[240])[2:] # AC Luma EHUFCO[F/0]
            value = abs(block_list[index])
            length = (zero_counter << 4) + basemath.bit_length(value) # EHUFCO[ZERO/VALUE]
            result += bin(AC_EHUFCO[length])[2:] + bin(value)[2:]
            zero_counter = 0
    # EOB
    result += bin(AC_EHUFCO[0])[2:]
    return result


# 2x2 average flatten
def flatten(block):
    for cal in [0, 2, 4, 6]:
        for row in [0, 2, 4, 6]:
            average = (block[cal][row] + block[cal][row + 1] + block[cal + 1][row] + block[cal + 1][row + 1]) / 4
            block[cal][row] = average
            block[cal][row + 1] = average
            block[cal + 1][row] = average
            block[cal + 1][row + 1] = average
    return block


# input should be integer
def rgb2ycbcr(red, green, blue):
    luminance        =  0.257 * red + 0.564 * green + 0.098 * blue + 16
    blue_chrominance = -0.148 * red - 0.291 * green + 0.439 * blue + 128
    red_chrominance  =  0.439 * red - 0.368 * green - 0.071 * blue + 128
    return [int(luminance), int(blue_chrominance), int(red_chrominance)]
