
# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/7/9
# Python Image JPEG mini encode
# Integer Operation Only Version
# Version 7.1
# Author: Clark Pu
# -------------------------------------

import base64

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

hufftable = dc_y_EHUFCO + dc_y_EHUFSI + ac_y_EHUFCO + ac_y_EHUFSI + dc_c_EHUFCO + dc_c_EHUFSI + ac_c_EHUFCO + ac_c_EHUFSI

luminance_quantization_table = [4294967296] * 64 # 1 << 32 (/1)
chrominance_quantization_table = [4294967296] * 64

quantable = luminance_quantization_table + chrominance_quantization_table

pi_mul_2  = 411775 # pi << 16 * 2,  2^16 = 65536
pi        = 205887 # pi << 16
pi_div_2  = 102944 # pi << 16 / 2
pi_div_16 = 12868  # pi << 16 / 16
k = 39797 # 0.6072529350088812561694 << 16
# CORDIC variation of the angle: 0.7853982, 0.4636476, 0.2449787, 0.1243550, 0.0624188, 0.0312398, 0.0156237
sigma = [51471 , 30385 , 16054 , 8149 , 4090 , 2047 , 1023]

# This is just a simulation for the real UART interface. // reg [0:31] ram [0:N]
def get_row(file_path:str):
    with open(file_path, 'rb+') as image:
        img_row = []
        byte_file = image.read()
        double_word = ''
        index = 1
        for byte in byte_file:
            text = str(hex(int(byte))[2:].upper())
            if len(text) < 2:
                text = '0' + text
            double_word += text
            if index % 4 == 0:
                img_row.append(int(double_word, 16))
                double_word = ''
            index += 1
    return img_row 


# JPEG file encode: Real RISCV simulation
def encode(file_path:str):

    print('\n')

    # Image read
    img_row = [] # YCbCr image in real RAM, it is an 8-bit stack
    img_row_in_uart = get_row(file_path+'.row')
    hight = img_row_in_uart[0] # integer type without declare are all 32-bit
    width = img_row_in_uart[1]
    
    # Pre-define variables
    mcu_rows = hight >> 4
    mcu_cals = width >> 4
    
    mcu_x = 0
    mcu_y = 0
    block_x = 0
    block_y = 0
    pixel_x = 0
    pixel_y = 0

    # Re-order Minimum coded unit(MCU)
    while mcu_y < mcu_rows:
        address_offset0 = 16 * width * mcu_y + 2 # 2 double-word space is for the hight and width
        while mcu_x < mcu_cals:
            address_offset1 = 16 * mcu_x + address_offset0
            while block_y < 2:
                address_offset2 = 8 * width * block_y + address_offset1
                while block_x < 2:
                    address_offset3 = 8 * block_x + address_offset2
                    while pixel_x < 8:
                        address_offset4 = pixel_x + address_offset3
                        while pixel_y < 8:
                            address_offset = width * pixel_y + address_offset4
                            
                            # YCbCr convertion
                            r = (img_row_in_uart[address_offset] >> 16) & 255
                            g = (img_row_in_uart[address_offset] >> 8) & 255
                            b = img_row_in_uart[address_offset] & 255
                            l  = (( 1103806595 * r + 2422361555 * g +  420906795 * b) >> 32) + 16
                            cb = ((- 635655160 * r - 1249835483 * g + 1885490643 * b) >> 32) + 128
                            cr = (( 1885490643 * r - 1580547965 * g -  304942678 * b) >> 32) + 128
                            img_row.append(l)
                            img_row.append(cb)
                            img_row.append(cr)

                            pixel_y += 1
                        pixel_y = 0
                        pixel_x += 1
                    pixel_x = 0
                    block_x += 1
                block_x = 0
                block_y += 1
            block_y = 0
            mcu_x += 1
        mcu_x = 0
        mcu_y += 1
    
    # huffman_bit_stack is an 32-bit stack but used for 1-bit stack
    # Memory location start at UART interface. 
    global huffman_bit_stack
    global stack_space
    huffman_bit_stack = [0]
    stack_space = 32

    # ------------------------------------------------------------------
    # Super function: block endcode
    global block, this_dc_value, last_dc_value, mode 
    
    def block_encode():

        global block, this_dc_value, last_dc_value, mode, stack_space
        
        # 8x8 matrix subtraction
        # ------------------------------------------------------------------
        p = 0
        while p != 64:
            block[p] -= 128
            p += 1
        
        # Discrete Cosine Transform
        # ------------------------------------------------------------------
        s = block
        # CORDIC local cosine function
        global target, x1 # partly local
        def cos(): # target been << 16
            global target
            global x1
            # import math
            # x1 = int(math.cos(target / 2 ** 16) * 2 ** 16)
            # return # debug
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
            p = 0 # iteration of the routation direction
            while p != 7:
                if theta > target:
                    theta -= sigma[p] # clockwise
                    direction[p] = 1
                else:
                    theta += sigma[p] # anticlockwise
                    direction[p] = - 1
                p += 1
            # vector routation, 2 to the power using shift
            x1 = k
            y1 = 0
            p = 6
            while p != -1:
                if direction[p] == 1:
                    x1 = x1 - (y1 >> p)
                    y1 = (x1 >> p) + y1
                else:
                    x1 = x1 + (y1 >> p)
                    y1 = - (x1 >> p) + y1
                p -= 1
            # return cosine result
            if inverse:
                x1 = - x1 # integer been << 16 bit
            return
        
        block = [0] * 64 # python bug exist here

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
                        target = (2*x + 1) * u * pi_div_16
                        cos()
                        temp = (temp * x1) >> 8
                        target = (2*y + 1) * v * pi_div_16
                        cos()
                        temp = (temp * x1) >> 8
                        unit += temp
                temp = (Cu * Cv) >> 16
                temp = (temp * unit) >> 32
                temp = temp >> 2 # divide 4
                if temp < 0:
                    temp += 1
                block[v + u * 8] = temp

        # Discrete Cosine Transform END
        # ------------------------------------------------------------------

        # Quantization
        # ------------------------------------------------------------------
        p = 0
        quantable_offset = 0
        if mode != 0:
            quantable_offset = 64
        while p != 64:
            block[p] = (block[p] * quantable[p + quantable_offset]) >> 32 # take top 32-bit of the mul result
            p += 1

        # Zigzag Scan
        # ------------------------------------------------------------------
        z = block
        x = 0
        y = 0
        p = 0
        block = [0] * 64
        direction = 1
        is_edge = 0
        block[0] = z[0]
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
                p += 1
                block[p] = z[y * 8 + x]
            # if is end
            if x == 7 and y == 7:
                break
            # normally forwarding
            p += 1
            x -= direction
            y += direction
            block[p] = z[y * 8 + x]

        # Differential DC Value
        # ------------------------------------------------------------------
        this_dc_value = block[0] 
        block[0] = this_dc_value - last_dc_value 

        # Huffman Encode
        # ------------------------------------------------------------------
        # 0 for Luminace
        if mode == 0:
            DC_CODE = 0
            DC_SIZE = 12
            AC_CODE = 24
            AC_SIZE = 275
        else:
            DC_CODE = 526
            DC_SIZE = 538
            AC_CODE = 550
            AC_SIZE = 801

        global temp_data, data, data_size # partly local

        def get_data_and_size():
            global temp_data, data, data_size
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
            return

        # push_size must less than 32-bit
        # start with: huffman_bit_stack = [0], stack_space = 32.
        global push_bin, push_size # partly local
        def push():
            global stack_space, push_bin, push_size
            last_dword = huffman_bit_stack[-1]
            if push_size <= stack_space:
                last_dword = last_dword + (push_bin << (stack_space - push_size))
                huffman_bit_stack[-1] = last_dword # push
                stack_space = stack_space - push_size
            else:
                # fill last double word
                last_dword = last_dword | (push_bin >> (push_size - stack_space))
                huffman_bit_stack[-1] = last_dword # push
                # fill new double word
                push_size = push_size - stack_space
                bit = push_size
                trim = 0
                while bit != 0:
                    trim = (trim << 1) + 1
                    bit -= 1
                trim = trim & push_bin
                stack_space = 32 - push_size
                this_word = trim << stack_space
                huffman_bit_stack.append(this_word) # push
            return
        
        # DC code
        temp_data = block[0]
        get_data_and_size()
        code = hufftable[DC_CODE + data_size]
        code_size = hufftable[DC_SIZE + data_size]
        push_bin = (code << data_size) + data # less than 32-bit: max code size=16, max data size=10
        push_size = data_size + code_size
        push()

        # AC code
        zero_counter = 0
        for index in range(1,64):
            if block[index] == 0:
                zero_counter += 1
            else:
                while zero_counter > 15: # zeros over than 15
                    zero_counter -= 16
                    push_bin = hufftable[AC_CODE + 240] # AC [F/0]
                    push_size = hufftable[AC_SIZE + 240]
                    push()
                # Assembly
                temp_data = block[index]
                get_data_and_size()
                ac_index = (zero_counter << 4) + data_size
                code = hufftable[AC_CODE + ac_index]
                code_size = hufftable[AC_SIZE + ac_index]
                push_bin = (code << data_size) + data # less than 32-bit: max code size=16, max data size=10
                push_size = data_size + code_size
                push()
                zero_counter = 0
        
        # EOB
        if zero_counter != 0:
            push_bin = hufftable[AC_CODE + 0] # AC [0/0]
            push_size = hufftable[AC_SIZE + 0]
            push()

        return this_dc_value 
    
    # End of super function
    # ------------------------------------------------------------------

    # Y Cb Cr subsampling and encode
    blockY = [0] * 64 # Y image blocks 32-bit * 64 integers
    blockCb = [0] * 64 # U image blocks 32-bit * 64 integers
    blockCr = [0] * 64 # V image blocks 32-bit * 64 integers
    index = 0
    counter = 0
    block_counter = 0
    last_dc_value_y = 0
    last_dc_value_cb = 0
    last_dc_value_cr = 0
    while index < (mcu_rows * mcu_cals * 16 * 16 * 3):
        # Sampling
        blockY[counter]   = img_row[index]
        blockCb[counter] += img_row[index + 1]
        blockCr[counter] += img_row[index + 2]
        # Block encode and subsampling
        if counter == 63:
            # Y Block encode
            block = blockY
            last_dc_value = last_dc_value_y
            mode = 0
            block_encode()
            last_dc_value_y = this_dc_value
            # Cb Cr subsampling
            if block_counter == 3:
                i = 0
                while i < 64:
                    blockCb[i] = blockCb[i] >> 2 # divide 4
                    blockCr[i] = blockCr[i] >> 2 # divide 4
                    i += 1
                # Cb Block encode
                block = blockCb
                last_dc_value = last_dc_value_cb
                mode = 1
                block_encode()
                last_dc_value_cb = this_dc_value
                # Cr Block encode
                block = blockCr
                last_dc_value = last_dc_value_cr
                mode = 1
                block_encode()
                last_dc_value_cr = this_dc_value
                # Clear for re-sampling
                i = 0
                while i < 64:
                    blockCb[i] = 0
                    blockCr[i] = 0
                    i += 1
                block_counter = 0
            else:
                block_counter += 1
            counter = 0
        else:
            counter += 1
        index += 3
        print('\r [Process]: (', index, '/', mcu_rows * mcu_cals * 16 * 16 * 3, ')', end='')

    # Post process: read in byte and insert '00' for 'FF', and fill the last byte
    fill = 0
    while stack_space != 0:
        fill = (fill << 1) + 1
        stack_space -= 1
    huffman_bit_stack[-1] += fill

    # String process, only for simulation usage
    hex_huffman_string = ''
    for double_word in huffman_bit_stack:
        hex_huffman_string += '0' * (8 - len(hex(double_word)[2:])) + hex(double_word)[2:].upper()
    # Remove the redundent FF
    while hex_huffman_string[-2:] == 'FF':
        if (len(hex_huffman_string) % 2 != 0):
            hex_huffman_string = hex_huffman_string[:-1]
        else:
            hex_huffman_string = hex_huffman_string[:-2]
    # 'FF' follows the '00'
    i = 0
    new_huffstring = ''
    while i < len(hex_huffman_string) / 2:
        byte = hex_huffman_string[i*2:i*2+2]
        new_huffstring += byte
        if byte == 'FF':
            new_huffstring += '00'
        i += 1
    hex_huffman_string = new_huffstring
 
    print('\r [Finished] Size:', int(len(hex_huffman_string) / 2), 'bytes.          \n')

    # Generate file
    file_hex = 'FFD8FFE000104A46494600010100000100010000'
    file_hex += 'FFDB004300'

    for byte in quantable[0:64]:
        file_hex += '0' * (2 - len(hex(byte >> 32)[2:])) + hex(byte >> 32)[2:].upper()

    file_hex += 'FFDB004301'
    for byte in quantable[64:]:
        file_hex += '0' * (2 - len(hex(byte >> 32)[2:])) + hex(byte >> 32)[2:].upper()

    lines = '0' * (4 - len( hex(hight)[2:])) + hex(hight)[2:].upper()
    samples_per_line = '0' * (4 - len( hex(width)[2:])) + hex(width)[2:].upper()
    file_hex += 'FFC0001108' + lines + samples_per_line + '03012200021101031101'

    file_hex += 'FFC4001F0000010501010101010100000000000000000102030405060708090A0BFFC400B5100002010303020403050504040000017D01020300041105122131410613516107227114328191A1082342B1C11552D1F02433627282090A161718191A25262728292A3435363738393A434445464748494A535455565758595A636465666768696A737475767778797A838485868788898A92939495969798999AA2A3A4A5A6A7A8A9AAB2B3B4B5B6B7B8B9BAC2C3C4C5C6C7C8C9CAD2D3D4D5D6D7D8D9DAE1E2E3E4E5E6E7E8E9EAF1F2F3F4F5F6F7F8F9FAFFC4001F0100030101010101010101010000000000000102030405060708090A0BFFC400B51100020102040403040705040400010277000102031104052131061241510761711322328108144291A1B1C109233352F0156272D10A162434E125F11718191A262728292A35363738393A434445464748494A535455565758595A636465666768696A737475767778797A82838485868788898A92939495969798999AA2A3A4A5A6A7A8A9AAB2B3B4B5B6B7B8B9BAC2C3C4C5C6C7C8C9CAD2D3D4D5D6D7D8D9DAE2E3E4E5E6E7E8E9EAF2F3F4F5F6F7F8F9FA'
    file_hex += 'FFDA000C03010002110311003F00'
    file_hex += hex_huffman_string
    file_hex += 'FFD9' 
    file_code = base64.b16decode(file_hex)
    with open(file_path+'.jpg', 'wb') as output_file:
        output_file.write(file_code)
