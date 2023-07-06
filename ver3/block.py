# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/28
# Python 8x8 Image block functions
# Clark Pu
# -------------------------------------


import basemath
debug = False

# f must be a 8x8 matrix
# Discrete Cosine Transform
def dct(s):

    # from scipy import fftpack
    # import numpy
    # dct_f = (numpy.array(s))
    # dct_f = fftpack.dct(fftpack.dct(dct_f[0:8, 0:8], norm='ortho').T, norm='ortho').T
    # print(numpy.fix(dct_f))

    S = basemath.zero(8,8)
    for u in range(0,8):
        if u == 0:
            Cu = 0.70710578 # sqrt(1/2)
        else:
            Cu = 1
        for v in range(0,8):
            if v == 0:
                Cv =  0.70710678 # sqrt(1/2)
            else:
                Cv = 1
            unit = 0
            for x in range(0,8):
                for y in range(0,8):
                    unit += s[y][x] * basemath.cos(((2 * x + 1) * u * basemath.pi) / 16) * basemath.cos(((2 * y + 1) * v * basemath.pi) / 16)
            S[v][u] = (1/4) * Cu * Cv * unit

    # basemath.dis_block(basemath.op(S, 0, 'int'), 4)
    return S


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
        return basemath.op_block(q, luminance_quantization_table, '/')
    else:
        return basemath.op_block(q, chrominance_quantization_table, '/')


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
                for bit in bin(-value)[2:]:
                    if bit == '1':
                        value_bin += '0'
                    else:
                        value_bin += '1'
            else:
                value_bin = bin(value)[2:]
        if debug:
            print(value_bin) #Debug
        return value_bin
    
    # Look for the DC code
    def DC_code(value):
        length = len(value)
        code = bin(DC_EHUFCO[length])[2:]
        size = DC_EHUFSI[length]
        code = '0' * (size - len(code)) + code
        if debug:
            print(code) #Debug
        return code
    
    # Look for the AC code
    def AC_code(zero_counter, value):
        length = (zero_counter << 4) + len(value) # EHUFCO[ZERO/VALUE]
        code = bin(AC_EHUFCO[length])[2:]
        size = AC_EHUFSI[length]
        code = '0' * (size - len(code)) + code
        if debug:
            print(code) #Debug
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


# Block Encode Pacakge. Must be YCbCr block
def encode(block, last_dc_value, dht_code_dc, dht_size_dc, dht_code_ac, dht_size_ac, dqt):
    if debug:
        basemath.dis_block(block, 4)
    # Discrete Cosine Transform
    block = basemath.op(block, 128, '-')
    block = dct(block)
    if debug:
        basemath.dis_block(basemath.op(block, 0, 'int'), 4)
    # Quantization
    block = basemath.op(basemath.op_block(block, dqt, '/'), 0, 'int')
    # basemath.dis_block(dqt, 4)
    if debug:
        basemath.dis_block(block, 4)
    # Zigzag Scan
    block = zigzag_scan(block)
    if debug:
        basemath.display(block, 4, 8)
    # Huffman Encode
    this_dc_value =block[0]
    block[0] = block[0] - last_dc_value
    block  = huffman_encode(block, dht_code_dc, dht_size_dc, dht_code_ac, dht_size_ac)
    if debug:
        print('\n', block, '\n--------------------------------------')
    return block, this_dc_value

