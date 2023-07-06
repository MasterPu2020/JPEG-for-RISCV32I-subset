# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/28
# Python 8x8 Image block process example
# Clark Pu
# -------------------------------------


import block
import basemath
import marker
from PIL import Image


def print_matrix(matrix):
    for line in matrix:
        print(line)


def block_encode(red_matrix, green_matrix, blue_matrix, dc_y_EHUFCO, dc_c_EHUFCO, ac_y_EHUFCO, ac_c_EHUFCO, dqt_0, dqt_1):
    # Colour conversion to YCbCr
    y_matrix  = basemath.zero(8,8)
    cb_matrix = basemath.zero(8,8)
    cr_matrix = basemath.zero(8,8)
    for cal in range(0,8):
        for row in range(0,8):
            l, cb, cr = block.rgb2ycbcr(red_matrix[cal][row], green_matrix[cal][row], blue_matrix[cal][row])
            y_matrix[cal][row] , cb_matrix[cal][row], cr_matrix[cal][row] = l, cb, cr    
    # Decrete Cosine Transform
    dct_y_matrix  = block.dct(basemath.op(y_matrix, 128, '-'))
    dct_cb_matrix = block.dct(basemath.op(cb_matrix, 128, '-'))
    dct_cr_matrix = block.dct(basemath.op(cr_matrix, 128, '-'))
    # Quantization
    q_y_matrix = basemath.op(basemath.op_block(dct_y_matrix, dqt_0, '/'), 0, 'int')
    q_cb_matrix = basemath.op(basemath.op_block(dct_cb_matrix, dqt_1, '/'), 0, 'int')
    q_cr_matrix = basemath.op(basemath.op_block(dct_cr_matrix, dqt_1, '/'), 0, 'int')
    # Zigzag Scan
    z_y_list  = block.zigzag_scan(q_y_matrix)
    z_cb_list = block.zigzag_scan(q_cb_matrix)
    z_cr_list = block.zigzag_scan(q_cr_matrix)
    # Huffman Encode
    huffman_code_y = block.huffman_encode(z_y_list, dc_y_EHUFCO, ac_y_EHUFCO)
    huffman_code_cb = block.huffman_encode(z_cb_list, dc_c_EHUFCO, ac_c_EHUFCO)
    huffman_code_cr = block.huffman_encode(z_cr_list, dc_c_EHUFCO, ac_c_EHUFCO)
    
    
    code = huffman_code_y + huffman_code_cb + huffman_code_cr
    return code

# Sample an 8x8 image block

debug = False

file = '0.jpg'
rgb_img = Image.open(file).convert('RGB')
img_width, img_hight = rgb_img.size
debug_img = Image.new('RGB', (img_width, img_hight), (0,0,0))

x_offset = 0
y_offset = 0
code = ''

red_matrix   = basemath.zero(8,8)
green_matrix = basemath.zero(8,8)
blue_matrix  = basemath.zero(8,8)

# Conversion of DHT marker

[[dc_y_EHUFCO],[dc_y_EHUFSI]] = marker.readfile(file, 'DHT', 0, debug)
[[ac_y_EHUFCO],[ac_y_EHUFSI]] = marker.readfile(file, 'DHT', 1, debug)
[[dc_c_EHUFCO],[dc_c_EHUFSI]] = marker.readfile(file, 'DHT', 2, debug)
[[ac_c_EHUFCO],[ac_c_EHUFSI]] = marker.readfile(file, 'DHT', 3, debug)

# Conversion of DQT marker
dqt_0 = basemath.shape2m(marker.readfile(file, 'DQT', 0, debug))
dqt_1 = basemath.shape2m(marker.readfile(file, 'DQT', 1, debug))

print('Total blocks:', (int(img_hight / 8) * int(img_width / 8)))
for y_offset in range(0, int(img_hight / 8)):
    for x_offset in range(0, int(img_width / 8)):
        for cal in range(0,8):
            for row in range(0,8):
                red_matrix[cal][row], green_matrix[cal][row], blue_matrix[cal][row] = rgb_img.getpixel((x_offset * 8 + cal, y_offset * 8 + row))
                if debug:
                    y, cb, cr = block.rgb2ycbcr(red_matrix[cal][row], green_matrix[cal][row], blue_matrix[cal][row])
                    debug_img.putpixel((x_offset * 8 + cal, y_offset * 8 + row), (y, cb, cr))

        # Encode the block
        block_code = block_encode(red_matrix, green_matrix, blue_matrix, dc_y_EHUFCO, dc_c_EHUFCO, ac_y_EHUFCO, ac_c_EHUFCO, dqt_0, dqt_1)

        code += block_code
        if debug:
            print('Block',x_offset, y_offset, 'code:', block_code)
        else:
            process = (x_offset +  y_offset * int(img_width / 8)) / (int(img_hight / 8) * int(img_width / 8)) * 100
            print("\r Process: ", int(process), '%  [', end=' ')
            i = int(process / 5)
            for j in range(0,20):
                if i > 0:
                    print('=',end='')
                else:
                    print(' ',end='')
                i -= 1
            print(']',end='')

print('\n')
hex_code = ''
# 最高位对其，最低位不满1byte的全补0
for i in range(0, 8 - len(code) % 8):
    code += '0'
# 遇到FF后面补一个00
i = 0
while i < len(code) / 8:
    byte = hex(int(code[i*8:i*8+8], 2))[2:].upper()
    if len(byte) == 1:
        byte = '0' + byte
    hex_code += byte
    if byte == 'FF':
        hex_code += '00 '
    i += 1

# Output
marker.readfile(file,'SOS',0,True)
original_size = img_width * img_hight * 3
encoded_size = int(len(hex_code) / 2)

if debug:
    print('Image binary code: ', code)
    debug_img.show()

print('\nImage hex code:\n', hex_code)
print('\nImage original size:', original_size, 'Byte.', original_size / 1024, 'KB\n')
print('\nImage encoded size: ', encoded_size, 'Byte.', encoded_size / 1024, 'KB\n')
