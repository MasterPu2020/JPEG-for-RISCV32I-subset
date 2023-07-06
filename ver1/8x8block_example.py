# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/23
# Python 8x8 Image block process example
# Clark Pu
# -------------------------------------


import block
import numpy
import marker
from PIL import Image

show_ycbcr_pictrue = False
show_dct_matrix = False
show_quantization_matrix = False
show_huffman_table = False
show_huffman_code = True

# Sample an 8x8 image block and convert to YCbCr

rgb_img = Image.open('example.jpg').convert('RGB')
ycbcr_block = Image.new('RGB', (8,8), (0,0,0))
x_offset = 187 * 8
y_offset = 8 * 8

y_matrix = numpy.zeros((8,8))
cb_matrix = numpy.zeros((8,8))
cr_matrix = numpy.zeros((8,8))

for cal in range(0,8):
    for row in range(0,8):
        red, green, blue = rgb_img.getpixel((x_offset + cal, y_offset + row))
        y, cb, cr = block.rgb2ycbcr(red, green, blue)
        y_matrix[cal,row] , cb_matrix[cal,row], cr_matrix[cal,row] = y, cb, cr
        ycbcr_block.putpixel((cal,row), (y, cb, cr))

if show_ycbcr_pictrue:
    ycbcr_block.show()

# Decrete Cosine Transform

dct_y_matrix  = block.dct(y_matrix  - 128)
dct_cb_matrix = block.dct(block.flatten(cb_matrix) - 128)
dct_cr_matrix = block.dct(block.flatten(cr_matrix) - 128)
if show_dct_matrix:
    print('\nDCT matirxs:')
    print(dct_y_matrix,'\n')
    print(dct_cb_matrix,'\n')
    print(dct_cr_matrix,'\n')

# Quantization

q_y_matrix  = block.quantization(dct_y_matrix,  0)
q_cb_matrix = block.quantization(dct_cb_matrix, 1)
q_cr_matrix = block.quantization(dct_cr_matrix, 1)
if show_quantization_matrix:
    print('\nQuantization matirxs:')
    print(q_y_matrix ,'\n')
    print(q_cb_matrix,'\n')
    print(q_cr_matrix,'\n')

# Zigzag Scan

z_y_list  = block.zigzag_scan(q_y_matrix)
z_cb_list = block.zigzag_scan(q_cb_matrix)
z_cr_list = block.zigzag_scan(q_cr_matrix)

# Huffman Encode

dc_luminance_marker   = 'ffc4001f0000010501010101010100000000000000000102030405060708090a0b'
ac_luminance_marker = 'ffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9fa'
dc_chrominance_marker   = 'ffc4001f0100030101010101010101010000000000000102030405060708090a0b'
ac_chrominace_marker  = 'ffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9fa'
[[dc_y_EHUFCO],[dc_y_EHUFSI]] = marker.huffman_table_generate(dc_luminance_marker, show_huffman_table)
[[dc_c_EHUFCO],[dc_c_EHUFSI]] = marker.huffman_table_generate(dc_chrominance_marker, show_huffman_table)
[[ac_y_EHUFCO],[ac_y_EHUFSI]] = marker.huffman_table_generate(ac_luminance_marker, show_huffman_table)
[[ac_c_EHUFCO],[ac_c_EHUFSI]] = marker.huffman_table_generate(ac_chrominace_marker, show_huffman_table)

# print('\nAC Luma EHUFCO[F/0]:', bin(ac_y_EHUFCO[240])[2:])

huffman_code_y = block.huffman_encode(z_y_list, dc_y_EHUFCO, ac_y_EHUFCO, show_huffman_code)
huffman_code_cb = block.huffman_encode(z_cb_list, dc_c_EHUFCO, ac_c_EHUFCO, show_huffman_code)
huffman_code_cr = block.huffman_encode(z_cr_list, dc_c_EHUFCO, ac_c_EHUFCO, show_huffman_code)

final_code = huffman_code_y + huffman_code_cb + huffman_code_cr
print('\nFinal code: ', final_code, '\n')
