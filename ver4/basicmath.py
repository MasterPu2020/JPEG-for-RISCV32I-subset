
# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/30
# Python basic math
# Clark Pu
# -------------------------------------


pi = 3.1415926535897932384626
sqrt0_5 = 0.707106781187


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


# define an zero matrix : NOT AN INTERGREATE FUNCTION
def zero(x=8, y=8):
    return [[0 for i in range(x)] for j in range(y)]


# Shape a vector into 8x8 matrix : NOT AN INTERGREATE FUNCTION
def shape2m(vector:list):
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
        raise SystemExit('Cannot shape into a matrix:', vector, 'length:', len(vector))


# Shape a 8x8 matrix into vector : NOT AN INTERGREATE FUNCTION
def shape2v(matrix:list):
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
def display(vector:list, space=4, enter=8):
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


# Format print a matrix in a matrix style : NOT AN INTERGREATE FUNCTION
def dis_block(matrix:list, space=4):
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
def dot(matrix_l:list, matrix_r:list):
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
def op(matrix_8x8:list, option:str, integer=1):
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
def op_block(matrix_l:list, option:str, matrix_r:list):
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
def cos(target:float):
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


# Discrete Cosine Transform
def fdct(s:list):
    S = zero(8, 8)
    for u in range(0,8):
        if u == 0:
            Cu = sqrt0_5
        else:
            Cu = 1
        for v in range(0,8):
            if v == 0:
                Cv = sqrt0_5
            else:
                Cv = 1
            unit = 0
            for x in range(0,8):
                for y in range(0,8):
                    unit += s[y][x] * cos(((2*x + 1) * u * pi) / 16) * cos(((2*y + 1) * v * pi) / 16)
            S[v][u] = (1/4) * Cu * Cv * unit
    return S


# Discrete Cosine Transform
def idct(S:list):
    s = zero(8,8)
    for x in range(0,8):
        for y in range(0,8):
            unit = 0
            for u in range(0,8):
                for v in range(0,8):
                    if u == 0:
                        Cu = sqrt0_5
                    else:
                        Cu = 1
                    if v == 0:
                        Cv = sqrt0_5
                    else:
                        Cv = 1
                    unit += S[v][u] * Cu * Cv * cos(((2*x + 1) * u * pi) / 16) * cos(((2*y + 1) * v * pi) / 16)
            s[y][x] = (1/4) *  unit
    return s


# get the bit length of an integer
def bit_length(integer:int):
    length = 0
    while integer > 0:
        integer = integer >> 1
        length += 1
    return length


# input should be integer
def rgb2ycbcr(red, green, blue):
    luminance        =  0.257 * red + 0.564 * green + 0.098 * blue + 16
    blue_chrominance = -0.148 * red - 0.291 * green + 0.439 * blue + 128
    red_chrominance  =  0.439 * red - 0.368 * green - 0.071 * blue + 128
    return int(luminance), int(blue_chrominance), int(red_chrominance)


# input should be integer
def ycbcr2rgb(luminance, blue_chrominance, red_chrominance):
    red   = 1.164 * (luminance - 16) + 1.596 * ( red_chrominance  - 128)
    green = 1.164 * (luminance - 16) - 0.392 * ( blue_chrominance - 128) -0.813 * (red_chrominance - 128)
    blue  = 1.164 * (luminance - 16) + 2.017 * ( blue_chrominance - 128)
    return int(red), int(green), int(blue)


# zigzag scan, input must be a 8x8 matrix, output is a 64 list
def zigzag_scan(z:list):
    x = 0
    y = 0
    i = 0
    zigzag_list = [0] * 64
    direction = 1
    is_edge = False
    zigzag_list[0] = z[0][0]
    while True:
        # meet edge
        if x == 0 or x == 7:
            y += 1
            is_edge = True
        elif y == 0 or y == 7:
            x += 1
            is_edge = True
        # If is edge
        if is_edge:
            is_edge = False
            direction = - direction
            i += 1
            zigzag_list[i] = z[y][x]
        # if is end
        if x == 7 and y == 7:
            return zigzag_list
        # normally forwarding
        i += 1
        x -= direction
        y += direction
        zigzag_list[i] = z[y][x]


# reversed zigzag scan, input must be a 8x8 matrix, output is a 64 list
def reverse_zigzag_scan(zigzag_list:list):
    x = 0
    y = 0
    i = 0
    z = zero(8,8)
    direction = 1
    is_edge = False
    z[0][0] = zigzag_list[0]
    while True:
        # meet edge
        if x == 0 or x == 7:
            y += 1
            is_edge = True
        elif y == 0 or y == 7:
            x += 1
            is_edge = True
        # If is edge
        if is_edge:
            is_edge = False
            direction = - direction
            i += 1
            z[y][x] = zigzag_list[i]
        # if is end
        if x == 7 and y == 7:
            return z
        # normally forwarding
        i += 1
        x -= direction
        y += direction
        z[y][x] = zigzag_list[i]


# block_list must be an integer list. EHUFCO EHUFSI tables are list, explained in itu-t81
def huffman_encode(block_list:list, DC_EHUFCO:list=[], DC_EHUFSI:list=[], AC_EHUFCO:list=[], AC_EHUFSI:list=[], mode='Self-defined', debug=False):
    
    # Auto file the huffman table, L is default
    if mode == 'C':
        DC_EHUFCO = dc_c_EHUFCO
        DC_EHUFSI = dc_c_EHUFSI
        AC_EHUFCO = ac_c_EHUFCO
        AC_EHUFSI = ac_c_EHUFSI
        if debug:
            print('Using default Chrominace Huffman table decodeing.')
    elif mode == 'L':
        DC_EHUFCO = dc_y_EHUFCO
        DC_EHUFSI = dc_y_EHUFSI
        AC_EHUFCO = ac_y_EHUFCO
        AC_EHUFSI = ac_y_EHUFSI
        if debug:
            print('Using default Luminace Huffman table decodeing.')
    elif debug:
        print('Using Self-defined Huffman table decodeing.')
    
    # decimal to binary with a reverse function
    def get_value(value):
        value_bin = ''
        if value != 0: # not empty: value 0 has 0 data size
            if value < 0:
                for bit in bin(-value)[2:]: # tmd shabi bug
                    if bit == '1':
                        value_bin += '0'
                    else:
                        value_bin += '1'
            else:
                value_bin = bin(value)[2:]
        return value_bin
    
    # Look for the DC code
    def DC_code(data:str): # input is data binary string
        data_size = len(data)
        code = bin(DC_EHUFCO[data_size])[2:]
        code_size = DC_EHUFSI[data_size]
        code = '0' * (code_size - len(code)) + code
        if debug:
            print('          Code Size:', code_size, ' Data Size:', data_size)
        return code
    
    # Look for the AC code
    def AC_code(zero_counter:int, data:str): # input is data binary string and amout of zeros
        zeros_and_data_size = (zero_counter << 4) + len(data) # EHUFCO[ZERO/VALUE]
        code = bin(AC_EHUFCO[zeros_and_data_size])[2:]
        code_size = AC_EHUFSI[zeros_and_data_size]
        code = '0' * (code_size - len(code)) + code
        if debug:
            print('          Code Size:', code_size, ' Zeros / Data Size:', (zero_counter << 4) , len(data))
        return code
    
    # DC code
    data = get_value(block_list[0])
    code = DC_code(data)
    result = code + data
    if debug:
        print('Index: 0  DC Code:', code, ' (bin)Data:', data, ' Data:', block_list[0])
    
    # AC code
    zero_counter = 0
    for index in range(1,len(block_list)):
        if block_list[index] == 0:
            zero_counter += 1
        else:
            while zero_counter > 15: # zeros over than 15
                zero_counter -= 16
                result += AC_code(15,get_value(0)) # AC Luma EHUFCO[F/0]
                if debug:
                    print('Index:', index, ' AC Code:', AC_code(15,get_value(0)), '16 Zeros: EHUFCO[F/0]')
            data = get_value(block_list[index])
            code = AC_code(zero_counter, data)
            result += code + data
            if debug:
                print('Index:', index, ' AC Code:', code, ' (bin)Data:', data, ' Data:', block_list[index])
            zero_counter = 0
    
    # EOB
    if zero_counter != 0:
        result += AC_code(0,get_value(0)) # AC Luma EHUFCO[0/0]
        if debug:
            print('Index:', index, 'End of Block:', AC_code(0,get_value(0)))
    return result
    

# Huffman decode for only one block
# file_code must be binary code and has removed the '00' followed by 'FF'
def huffman_decode(file_code:str, DC_EHUFCO:list=[], DC_EHUFSI:list=[], AC_EHUFCO:list=[], AC_EHUFSI:list=[], mode:str='self-defined', debug:bool=False):
    
    block = []

    # Auto file the huffman table, L is default
    if mode == 'C':
        DC_EHUFCO = dc_c_EHUFCO
        DC_EHUFSI = dc_c_EHUFSI
        AC_EHUFCO = ac_c_EHUFCO
        AC_EHUFSI = ac_c_EHUFSI
        if debug:
            print('Using default Chrominace Huffman table decodeing.')
    elif mode == 'L':
        DC_EHUFCO = dc_y_EHUFCO
        DC_EHUFSI = dc_y_EHUFSI
        AC_EHUFCO = ac_y_EHUFCO
        AC_EHUFSI = ac_y_EHUFSI
        if debug:
            print('Using default Luminace Huffman table decodeing.')
    elif debug:
        print('Using Self-defined Huffman table decodeing.')

    # binary to decimal with a reverse function
    def bin2int(value_bin:str):
        value = ''
        if value_bin == '': # if it is empty
            value = 0
        else:
            if value_bin[0] == '0':
                for bit in value_bin:
                    if bit == '1':
                        value += '0'
                    else:
                        value += '1'
                value = - int(value, 2)
            else:
                value = int(value_bin, 2)
        return value

    # Search in the file code and convert to data size and code size
    def code2sizes(filecode, co, si):
        for data_size in range(0,len(co)):
            # Index of EHUFCO and EHUFSI (the data_size) convert to huffman code
            code = bin(co[data_size])[2:]
            code_size = si[data_size]
            for i in range(0, code_size - len(code)):
                code = '0' + code
            # find the first huffcode with matchs the filecode fragment
            if filecode == code and code_size != 0:
                return data_size, code_size
        return 'NotFind', 'NotFind'

    # Return the first value and rest of the DC code
    def DCcode2value(file_code):
        fragment = ''
        i = 0
        while i < len(file_code):
            fragment += file_code[i]
            # Check the if the fragment is a huffman code
            data_size, code_size = code2sizes(fragment, DC_EHUFCO, DC_EHUFSI)
            # Found it is a huffman code, then
            if code_size != 'NotFind':
                # Get Data
                i += 1
                bin_data = file_code[i:i + data_size]
                data = bin2int(bin_data)
                if debug:
                    print('DC Code:', fragment, ' Code Size:', code_size, ' Data:', bin_data, ' : ', data, ' Data Size:', data_size)
                i += data_size
                return data, file_code[i:]
            i += 1
        raise SystemExit('Failed to find the DC value. Exit with file code:', file_code)

    # Return the first value and rest of the AC code
    def ACcode2value(file_code):
        fragment = ''
        i = 0
        while i < len(file_code):
            fragment += file_code[i]
            # Check the if the fragment is a huffman code
            zeros_and_data_size, code_size = code2sizes(fragment, AC_EHUFCO, AC_EHUFSI)
            # Found it is a huffman code, then
            if code_size != 'NotFind':
                # Get Data
                i += 1
                if (zeros_and_data_size != 0): # Not the end of block
                    # Get Zeros / DataSize and Data
                    if len(hex(zeros_and_data_size)[2:]) < 2:
                        data_size = zeros_and_data_size
                        zeros = 0
                    else:
                        data_size = int(hex(zeros_and_data_size)[3], 16)
                        zeros = int(hex(zeros_and_data_size)[2], 16)
                    bin_data = file_code[i:i + data_size]
                    data = bin2int(bin_data)
                else:
                    # End of block
                    if debug:
                        print('AC Code:', fragment, 'EOB')
                    return 'EOB', 'EOB', file_code[i:]
                if debug:
                    print('AC Code:', fragment, ' Code Size:', code_size, ' Data:', bin_data, ' : ', data, 'Zeros:', zeros)
                return zeros, data, file_code[i+data_size:]
            i += 1
        raise SystemExit('Failed to find the AC value. Exit with file code:', file_code)

    # Differential DC values
    data, file_code = DCcode2value(file_code)
    block.append(data)
    index = 1

    # AC values
    while 1:
        if index > 63:
            # print('Warnning: Block index out of 64, no EOB find.')
            break
        zeros, data, file_code = ACcode2value(file_code)
        if zeros == 'EOB':
            break
        for i in range(0,zeros):
            block.append(0)
            index += 1
        block.append(data)
        index += 1

    # EOB fill zeros
    while index < 64:
        block.append(0)
        index += 1

    if debug:
        print('Block is:')
        display(block)

    return block, file_code

