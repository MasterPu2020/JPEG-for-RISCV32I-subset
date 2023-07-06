# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/25
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


def block_encode(red_matrix, green_matrix, blue_matrix, dc_y_EHUFCO, dc_c_EHUFCO, ac_y_EHUFCO, ac_c_EHUFCO, debug):
    # Colour conversion to YCbCr
    y_matrix  = basemath.matrix_zero(8,8)
    cb_matrix = basemath.matrix_zero(8,8)
    cr_matrix = basemath.matrix_zero(8,8)
    for cal in range(0,8):
        for row in range(0,8):
            l, cb, cr = block.rgb2ycbcr(red_matrix[cal][row], green_matrix[cal][row], blue_matrix[cal][row])
            y_matrix[cal][row] , cb_matrix[cal][row], cr_matrix[cal][row] = l, cb, cr    
    # Decrete Cosine Transform
    dct_y_matrix  = block.dct(basemath.matrix_op(y_matrix, 128, '-'))
    dct_cb_matrix = block.dct(basemath.matrix_op(cb_matrix, 128, '-'))
    dct_cr_matrix = block.dct(basemath.matrix_op(cr_matrix, 128, '-'))
    # Quantization
    q_y_matrix  = block.quantization(dct_y_matrix,  0)
    q_cb_matrix = block.quantization(dct_cb_matrix, 1)
    q_cr_matrix = block.quantization(dct_cr_matrix, 1)
    # Zigzag Scan
    z_y_list  = block.zigzag_scan(q_y_matrix)
    z_cb_list = block.zigzag_scan(q_cb_matrix)
    z_cr_list = block.zigzag_scan(q_cr_matrix)
    # Huffman Encode
    huffman_code_y = block.huffman_encode(z_y_list, dc_y_EHUFCO, ac_y_EHUFCO)
    huffman_code_cb = block.huffman_encode(z_cb_list, dc_c_EHUFCO, ac_c_EHUFCO)
    huffman_code_cr = block.huffman_encode(z_cr_list, dc_c_EHUFCO, ac_c_EHUFCO)
    code = huffman_code_y + huffman_code_cb + huffman_code_cr
    # if debug:
    #     print(hex(int(huffman_code_y, 2))[2:], hex(int(huffman_code_cb, 2))[2:], hex(int(huffman_code_cr, 2))[2:])
    return code


# Conversion of DHT marker

dc_luminance_marker   = 'ffc4001f0000010501010101010100000000000000000102030405060708090a0b'
ac_luminance_marker   = 'ffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9fa'
dc_chrominance_marker = 'ffc4001f0100030101010101010101010000000000000102030405060708090a0b'
ac_chrominace_marker  = 'ffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9fa'
[[dc_y_EHUFCO],[dc_y_EHUFSI]] = marker.huffman_table_generate(dc_luminance_marker, False)
[[dc_c_EHUFCO],[dc_c_EHUFSI]] = marker.huffman_table_generate(dc_chrominance_marker, False)
[[ac_y_EHUFCO],[ac_y_EHUFSI]] = marker.huffman_table_generate(ac_luminance_marker, False)
[[ac_c_EHUFCO],[ac_c_EHUFSI]] = marker.huffman_table_generate(ac_chrominace_marker, False)

# Sample an 8x8 image block

debug = True

file = '0.jpg'
rgb_img = Image.open(file).convert('RGB')
img_width, img_hight = rgb_img.size
debug_img = Image.new('RGB', (img_width, img_hight), (0,0,0))

x_offset = 0
y_offset = 0
code = ''

red_matrix   = basemath.matrix_zero(8,8)
green_matrix = basemath.matrix_zero(8,8)
blue_matrix  = basemath.matrix_zero(8,8)

print('Total blocks:', (int(img_hight / 8) * int(img_width / 8)))
for y_offset in range(0, int(img_hight / 8)):
    for x_offset in range(0, int(img_width / 8)):
        for cal in range(0,8):
            for row in range(0,8):
                red_matrix[cal][row], green_matrix[cal][row], blue_matrix[cal][row] = rgb_img.getpixel((x_offset * 8 + cal, y_offset * 8 + row))
                if debug:
                    y, cb, cr = block.rgb2ycbcr(red_matrix[cal][row], green_matrix[cal][row], blue_matrix[cal][row])
                    debug_img.putpixel((x_offset * 8 + cal, y_offset * 8 + row), (y, cb, cr))
        block_code = block_encode(red_matrix, green_matrix, blue_matrix, dc_y_EHUFCO, dc_c_EHUFCO, ac_y_EHUFCO, ac_c_EHUFCO, debug)
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
hex_code = hex(int(code, 2))[2:].upper()
# 最高位对其，最低位不满1byte的全补0
# 遇到FF后面补一个00
# 没有处理正负号，还需补充一下代码
original_size = img_width * img_hight * 3
encoded_size = int(len(hex_code) / 2)

if debug:
    print('Image binary code: ', code)
    debug_img.show()

print('\nImage hex code:\n', hex_code)
print('\nImage original size:', original_size / 1024, 'KB\n')
print('\nImage encoded size: ', encoded_size / 1024, 'KB\n')
