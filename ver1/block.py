# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/24
# Python 8x8 Image block functions
# Clark Pu
# -------------------------------------


import numpy
import cordic


# f must be a 8x8 matrix
def dct(f):
    pi = 3.1415926535897932384626
    a = numpy.zeros((8,8))
    for i in range(0,8):
        if i == 0:
            c = 0.35355339059327376 # sqrt(1/8)
        else:
            c = 0.5 # sqrt(2/8)
        for j in range(0,8):
            a[i, j] = c * cordic.cos(pi * (j + 1/2) * i / 8)
    dct_f = a.dot(f).dot(a.T) # F = a·f·a' (这里F为变量dct_f)
    dct_f = numpy.fix(dct_f)
    return dct_f


# q is 8x8 DCT matrix, method = 0 for luminance, 1 for chrominance
def quantization(q, method):

    luminance_quantization_table= numpy.matrix(
    [[16,  11,  10,  16,  24,  40,  51,  61],
     [12,  12,  14,  19,  26,  58,  60,  55],
     [14,  13,  16,  24,  40,  57,  69,  56],
     [14,  17,  22,  29,  51,  87,  80,  62],
     [18,  22,  37,  56,  68, 109, 103,  77],
     [24,  35,  55,  64,  81, 104, 113,  92],
     [49,  64,  78,  87, 103, 121, 120, 101],
     [72,  92,  95,  98, 112, 100, 103,  99]])
    
    chrominance_quantization_table = numpy.matrix(
    [[17,  18,  24,  47,  99,  99,  99,  99],
     [18,  21,  26,  66,  99,  99,  99,  99],
     [24,  26,  56,  99,  99,  99,  99,  99],
     [47,  66,  99,  99,  99,  99,  99,  99],
     [99,  99,  99,  99,  99,  99,  99,  99],
     [99,  99,  99,  99,  99,  99,  99,  99],
     [99,  99,  99,  99,  99,  99,  99,  99],
     [99,  99,  99,  99,  99,  99,  99,  99]])
    
    if method == 1:
        return numpy.fix(q / luminance_quantization_table)
    else:
        return numpy.fix(q / chrominance_quantization_table)


# z must be a 8x8 matrix
def zigzag_scan(z):
    x = 0
    y = 0
    i = 0
    zigzag_list = [0] * 64
    direction = 1
    is_edge = False
    zigzag_list[0] = int(z[0,0])
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
            zigzag_list[i] = int(z[x, y])

        if x == 7 and y == 7:
            return zigzag_list
        
        i += 1
        x -= direction
        y += direction
        zigzag_list[i] = int(z[x, y])


# get the bit length of an integer
def bit_length(integer):
    length = 0
    while integer > 0:
        integer = integer >> 1
        length += 1
    return length


# block_list must be an integer list. mode should be 0 for luma, 1 for chroma
def huffman_encode(block_list, DC_EHUFCO, AC_EHUFCO, debug):
    # DC code
    value = abs(block_list[0])
    length = bit_length(value)
    result = bin(DC_EHUFCO[length])[2:] + bin(value)[2:]
    if debug:
        print('\nZigzag list:', block_list)
        print('DC value:', value, '.binary length:', length, '.huffman code:', result)
    # AC code
    zero_counter = 0
    for index in range(1,len(block_list)):
        if block_list[index] == 0:
            zero_counter += 1
        else:
            value = abs(block_list[index])
            while zero_counter > 15:
                zero_counter -= 16
                result += bin(AC_EHUFCO[240])[2:] # AC Luma EHUFCO[F/0]
                if debug:
                    print(' next huffman code +=', bin(AC_EHUFCO[240])[2:])
            length = (zero_counter << 4) + bit_length(value) # EHUFCO[ZERO/VALUE]
            result += bin(AC_EHUFCO[length])[2:] + bin(value)[2:]
            if debug:
                print('AC value:', value, '.binary length + << amount(zero):', length, '.zeros:', zero_counter, '.huffman code:', bin(AC_EHUFCO[length])[2:] + bin(value)[2:])
            zero_counter = 0
    # EOB
    EOB = bin(AC_EHUFCO[0])[2:]
    result += EOB
    if debug:
        print('EOB:', EOB)
    return result


# huffman_encode(0,0)

# 2x2 average flatten
def flatten(block):
    for cal in [0, 2, 4, 6]:
        for row in [0, 2, 4, 6]:
            average = (block[cal, row] + block[cal, row + 1] + block[cal + 1, row] + block[cal + 1, row + 1]) / 4
            block[cal, row] = average
            block[cal, row + 1] = average
            block[cal + 1, row] = average
            block[cal + 1, row + 1] = average
    return block


# input should be integer
def rgb2ycbcr(red, green, blue):
    luminance        =  0.257 * red + 0.564 * green + 0.098 * blue + 16
    blue_chrominance = -0.148 * red - 0.291 * green + 0.439 * blue + 128
    red_chrominance  =  0.439 * red - 0.368 * green - 0.071 * blue + 128
    return [int(luminance), int(blue_chrominance), int(red_chrominance)]


# # -------------------------------------
# # Debug

# # generate an 8x8 block sample
# f = numpy.random.randint(-128,127,(8,8))

# from PIL import Image
# sample = Image.open('coffee.png')
# sample = sample.convert('L')
# # sample.show()
# offset = 0
# for i in range(offset, offset + 8):
#     for j in range(offset, offset + 8):
#         f[i,j] = sample.getpixel((i,j))

# f_verification = f
# print('\nOriginal sample is:\n', f)

# # Calculation
# print('\nResult:')
# f = dct(f)
# print('\nDCT Matrix is:\n', f)
# f = quantization(f, 0)
# print('\nQuantization Matrix is:\n', f)
# f = zigzag_scan(f)
# print('\nZigzag Matrix is:\n', f)

# # Verification
# print('\nVerification:\n')
# from scipy import fftpack
# f_verification = fftpack.dct(f_verification, norm='ortho').T
# f_verification = fftpack.dct(f_verification, norm='ortho').T
# f_verification = numpy.fix(f_verification)
# print('\nDCT Matrix is:\n', f_verification)
# f_verification = quantization(f_verification, 0)
# print('\nQuantization Matrix is:\n', f_verification)
# zigzag_test_table = numpy.matrix(
#     [[ 1,   2,   6,  7,   15,  16,  77,  00],
#      [ 3,   5,   8,  14,  18,   7,  99,  66],
#      [ 4,   9,  13,  19,   7,  99,   6,  55],
#      [10,  12,  20,   7,  99,   6,   5,  44],
#      [11,  21,   7,  99,   6,   5,   4,  33],
#      [22,   7,  99,   6,   5,   4,   3,  22],
#      [77,  99,   6,   5,   4,   3,   2,  11],
#      [00,  66,  55,  44,  33,  22,  11,   0]])
# print('\nZigzag test:\n', zigzag_scan(zigzag_test_table))
