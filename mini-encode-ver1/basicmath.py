
# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/7/3
# Basic math algorithm optimized for RISCV
# Version 6.0
# Clark Pu
# -------------------------------------


# EHUFCO: huffman code, value is the value of the binary huffman code
# EHUFSI: huffman size, value is the size of the binary huffman code
# The index of the huffman code is the size of the data
# But in AC tables, the index formed as Zero/DataSize
dc_y_EHUFCO = [0, 2, 3, 4, 5, 6, 14, 30, 62, 126, 254, 510]
dc_y_EHUFSI = [2, 3, 3, 3, 3, 3, 4, 5, 6, 7, 8, 9]
ac_y_EHUFCO = [
  10,     0,     1,     4,    11,    26,   120,   248,  1014, 65410, 65411, 0, 0, 0, 0, 0,
   0,    12,    27,   121,   502,  2038, 65412, 65413, 65414, 65415, 65416, 0, 0, 0, 0, 0,
   0,    28,   249,  1015,  4084, 65417, 65418, 65419, 65420, 65421, 65422, 0, 0, 0, 0, 0,
   0,    58,   503,  4085, 65423, 65424, 65425, 65426, 65427, 65428, 65429, 0, 0, 0, 0, 0,
   0,    59,  1016, 65430, 65431, 65432, 65433, 65434, 65435, 65436, 65437, 0, 0, 0, 0, 0,
   0,   122,  2039, 65438, 65439, 65440, 65441, 65442, 65443, 65444, 65445, 0, 0, 0, 0, 0,
   0,   123,  4086, 65446, 65447, 65448, 65449, 65450, 65451, 65452, 65453, 0, 0, 0, 0, 0,
   0,   250,  4087, 65454, 65455, 65456, 65457, 65458, 65459, 65460, 65461, 0, 0, 0, 0, 0,
   0,   504, 32704, 65462, 65463, 65464, 65465, 65466, 65467, 65468, 65469, 0, 0, 0, 0, 0,
   0,   505, 65470, 65471, 65472, 65473, 65474, 65475, 65476, 65477, 65478, 0, 0, 0, 0, 0,
   0,   506, 65479, 65480, 65481, 65482, 65483, 65484, 65485, 65486, 65487, 0, 0, 0, 0, 0,
   0,  1017, 65488, 65489, 65490, 65491, 65492, 65493, 65494, 65495, 65496, 0, 0, 0, 0, 0,
   0,  1018, 65497, 65498, 65499, 65500, 65501, 65502, 65503, 65504, 65505, 0, 0, 0, 0, 0,
   0,  2040, 65506, 65507, 65508, 65509, 65510, 65511, 65512, 65513, 65514, 0, 0, 0, 0, 0,
   0, 65515, 65516, 65517, 65518, 65519, 65520, 65521, 65522, 65523, 65524, 0, 0, 0, 0, 0,
2041, 65525, 65526, 65527, 65528, 65529, 65530, 65531, 65532, 65533, 65534]
ac_y_EHUFSI = [
 4,  2,  2,  3,  4,  5,  7,  8, 10, 16, 16,  0,  0,  0,  0,  0,
 0,  4,  5,  7,  9, 11, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  5,  8, 10, 12, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  6,  9, 12, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  6, 10, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  7, 11, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  7, 12, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  8, 12, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  9, 15, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  9, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  9, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0, 10, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0, 10, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0, 11, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
11, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
dc_c_EHUFCO = [0, 1, 2, 6, 14, 30, 62, 126, 254, 510, 1022, 2046]
dc_c_EHUFSI = [2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
ac_c_EHUFCO = [
   0,     1,     4,    10,    24,    25,    56,   120,   500,  1014,  4084, 0, 0, 0, 0, 0,
   0,    11,    57,   246,   501,  2038,  4085, 65416, 65417, 65418, 65419, 0, 0, 0, 0, 0,
   0,    26,   247,  1015,  4086, 32706, 65420, 65421, 65422, 65423, 65424, 0, 0, 0, 0, 0,
   0,    27,   248,  1016,  4087, 65425, 65426, 65427, 65428, 65429, 65430, 0, 0, 0, 0, 0,
   0,    58,   502, 65431, 65432, 65433, 65434, 65435, 65436, 65437, 65438, 0, 0, 0, 0, 0,
   0,    59,  1017, 65439, 65440, 65441, 65442, 65443, 65444, 65445, 65446, 0, 0, 0, 0, 0,
   0,   121,  2039, 65447, 65448, 65449, 65450, 65451, 65452, 65453, 65454, 0, 0, 0, 0, 0,
   0,   122,  2040, 65455, 65456, 65457, 65458, 65459, 65460, 65461, 65462, 0, 0, 0, 0, 0,
   0,   249, 65463, 65464, 65465, 65466, 65467, 65468, 65469, 65470, 65471, 0, 0, 0, 0, 0,
   0,   503, 65472, 65473, 65474, 65475, 65476, 65477, 65478, 65479, 65480, 0, 0, 0, 0, 0,
   0,   504, 65481, 65482, 65483, 65484, 65485, 65486, 65487, 65488, 65489, 0, 0, 0, 0, 0,
   0,   505, 65490, 65491, 65492, 65493, 65494, 65495, 65496, 65497, 65498, 0, 0, 0, 0, 0,
   0,   506, 65499, 65500, 65501, 65502, 65503, 65504, 65505, 65506, 65507, 0, 0, 0, 0, 0,
   0,  2041, 65508, 65509, 65510, 65511, 65512, 65513, 65514, 65515, 65516, 0, 0, 0, 0, 0,
   0, 16352, 65517, 65518, 65519, 65520, 65521, 65522, 65523, 65524, 65525, 0, 0, 0, 0, 0,
1018, 32707, 65526, 65527, 65528, 65529, 65530, 65531, 65532, 65533, 65534]
ac_c_EHUFSI = [
 2,  2,  3,  4,  5,  5,  6,  7,  9, 10, 12,  0,  0,  0,  0,  0,
 0,  4,  6,  8,  9, 11, 12, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  5,  8, 10, 12, 15, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  5,  8, 10, 12, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  6,  9, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  6, 10, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  7, 11, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  7, 11, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  8, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  9, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  9, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  9, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0,  9, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0, 11, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
 0, 14, 16, 16, 16, 16, 16, 16, 16, 16, 16,  0,  0,  0,  0,  0,
10, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16]

# Default Quantization tables provided in itu-t81
luminance_quantization_table = [
16,  11,  10,  16,  24,  40,  51,  61,
12,  12,  14,  19,  26,  58,  60,  55,
14,  13,  16,  24,  40,  57,  69,  56,
14,  17,  22,  29,  51,  87,  80,  62,
18,  22,  37,  56,  68, 109, 103,  77,
24,  35,  55,  64,  81, 104, 113,  92,
49,  64,  78,  87, 103, 121, 120, 101,
72,  92,  95,  98, 112, 100, 103,  99]
chrominance_quantization_table = [
17,  18,  24,  47,  99,  99,  99,  99,
18,  21,  26,  66,  99,  99,  99,  99,
24,  26,  56,  99,  99,  99,  99,  99,
47,  66,  99,  99,  99,  99,  99,  99,
99,  99,  99,  99,  99,  99,  99,  99,
99,  99,  99,  99,  99,  99,  99,  99,
99,  99,  99,  99,  99,  99,  99,  99,
99,  99,  99,  99,  99,  99,  99,  99]

# CORDIC variation of the angle
sigma = [0.7853982, 0.4636476, 0.2449787, 0.1243550, 0.0624188, 0.0312398, 0.0156237]


# 8x8 matrix subtraction
def subtract(matrix:list, integer:int):
    index = 0
    while index != 64:
        matrix[index] -= integer
        index += 1
    return matrix


# 8x8 matrix divide by 8x8 matrix
def divide(matrix_l:list, matrix_r:list):
    index = 0
    matrix = [0] * 64
    while index != 64:
        matrix[index] = int(matrix_l[index] / matrix_r[index])
        index += 1
    return matrix


# Discrete Cosine Transform 
# Need more effort to perform an 32-bit integer multiplication to replace 32-bit float multiplication
def dct(s:list):
    
    pi = 3.141592653589

    # CORDIC cosine function
    def cos(target:float):
        # constraint in -pi/2 ~ pi/2
        inverse = False
        while target > 3.141592653589:
            target -= 6.283185307178
        if target > 1.5707963267945:
            inverse = True
            target -= 3.141592653589
        elif target < - 1.5707963267945:
            inverse = True
            target += 3.141592653589
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
        x = 39797 # parameter K6 << 16 : 0.6072529350088812561694 * 65536
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
            return - x / 65536 # It never over than +-1, can be used in integer multiplication
        else:
            return x / 65536
        
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


# input should be integer
def rgb2ycbcr(red, green, blue):
    luminance        =  0.257 * red + 0.564 * green + 0.098 * blue + 16
    blue_chrominance = -0.148 * red - 0.291 * green + 0.439 * blue + 128
    red_chrominance  =  0.439 * red - 0.368 * green - 0.071 * blue + 128
    return int(luminance), int(blue_chrominance), int(red_chrominance)


# zigzag scan, input is a 64 list, output is a 64 list
def zigzag_scan(z:list):
    x = 0
    y = 0
    i = 0
    zigzag_list = [0] * 64
    direction = 1
    is_edge = 0
    zigzag_list[0] = z[0]
    while True:
        # meet edge
        if x == 0 or x == 7:
            y += 1
            is_edge = 1
        elif y == 0 or y == 7:
            x += 1
            is_edge = 1
        # If is edge
        if is_edge == 1:
            is_edge = 0
            direction = - direction
            i += 1
            zigzag_list[i] = z[y * 8 + x]
        # if is end
        if x == 7 and y == 7:
            return zigzag_list
        # normally forwarding
        i += 1
        x -= direction
        y += direction
        zigzag_list[i] = z[y * 8 + x]


# block_list is an integer list. this is the zigzag data list.
# double_word_list is the list of huffman encoded data.  In RISCV can use it as push and pop
# push data size must less than 32-bit: max code size=16, max data size=10, always less than 32.
# space is the empty bit data space of last double-word in double_word_list. integer: range at 0 ~ 31 (start with 32)
def huffman_encode(block_list:list, double_word_list:list=[], last_double_word_space:int=0, mode=0):

    # 0 for Luminace
    if mode == 0:
        DC_EHUFCO = dc_y_EHUFCO
        DC_EHUFSI = dc_y_EHUFSI
        AC_EHUFCO = ac_y_EHUFCO
        AC_EHUFSI = ac_y_EHUFSI
    else:
        DC_EHUFCO = dc_c_EHUFCO
        DC_EHUFSI = dc_c_EHUFSI
        AC_EHUFCO = ac_c_EHUFCO
        AC_EHUFSI = ac_c_EHUFSI

    def get_data_and_size(temp_data:int):
        temp_data_size = 0
        less = 0
        if temp_data < 0:
            temp_data = ~ temp_data + 1
            less = 1
        data = temp_data
        while temp_data != 0:
            temp_data = temp_data >> 1
            temp_data_size += 1
        data_size = temp_data_size
        if less == 1:
            trim = 0
            while temp_data_size != 0:
                trim = (trim << 1) + 1
                temp_data_size -= 1
            data = (~ data) & trim
        return data, data_size
    
    # push_size must less than 32-bit
    # start with: double_word_list = [0], space = 32.
    def push(space, push_bin, push_size):
        last_dword = double_word_list[-1]
        if push_size <= space:
            last_dword = last_dword + (push_bin << (space - push_size))
            double_word_list[-1] = last_dword # push
            space = space - push_size
        else:
            # fill last double word
            last_dword = last_dword | (push_bin >> (push_size - space))
            double_word_list[-1] = last_dword # push
            # fill new double word
            push_size = push_size - space
            bit = push_size
            trim = 0
            while bit != 0:
                trim = (trim << 1) + 1
                bit -= 1
            trim = trim & push_bin
            space = 32 - push_size
            this_word = trim << space
            double_word_list.append(this_word) # push
        return space
    
    # DC code
    data = block_list[0]
    data, data_size = get_data_and_size(data)
    code = DC_EHUFCO[data_size]
    code_size = DC_EHUFSI[data_size]
    push_bin = (code << data_size) + data # less than 32-bit: max code size=16, max data size=10
    push_size = data_size + code_size
    space = push(last_double_word_space, push_bin, push_size)

    # AC code
    zero_counter = 0
    for index in range(1,64):
        if block_list[index] == 0:
            zero_counter += 1
        else:
            while zero_counter > 15: # zeros over than 15
                zero_counter -= 16
                push_bin = AC_EHUFCO[240] # AC [F/0]
                push_size = AC_EHUFSI[240]
                space = push(space, push_bin, push_size)
            # Assembly
            data = block_list[index]
            data, data_size = get_data_and_size(data)
            ac_index = (zero_counter << 4) + data_size
            code = AC_EHUFCO[ac_index]
            code_size = AC_EHUFSI[ac_index]
            push_bin = (code << data_size) + data # less than 32-bit: max code size=16, max data size=10
            push_size = data_size + code_size
            space = push(space, push_bin, push_size)
            zero_counter = 0
    
    # EOB
    if zero_counter != 0:
        push_bin = AC_EHUFCO[0] # AC [0/0]
        push_size = AC_EHUFSI[0]
        space = push(space, push_bin, push_size)

    return double_word_list, space

