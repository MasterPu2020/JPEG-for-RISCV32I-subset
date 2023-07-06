# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/28
# Python Image JPEG encode
# Clark Pu
# -------------------------------------


import block
import basemath
import marker
import base64
from PIL import Image


debug = False
marker_debug = False and debug

print('\n')
file_name = 'green'
bmp_file = file_name + '.bmp'
jpeg_file = file_name + '.jpg'
rgb_img = Image.open(jpeg_file).convert('RGB')
img_width, img_hight = rgb_img.size

# convert image into an YCbCr image
if img_width % 16 != 0:
    img_width += 16 - img_width % 16
if img_hight % 16 != 0:
    img_hight += 16 - img_hight % 16
ycbcr_img = Image.new('RGB', (img_width, img_hight), (0,0,0))
for cal in range(0,img_width):
    for row in range(0,img_hight):
        if cal < rgb_img.size[0] and row < rgb_img.size[1]:
            r, g, b = rgb_img.getpixel((cal,row))
        else:
            r, g, b = [144,144,144]
        y, cb, cr = block.rgb2ycbcr(r,g,b)
        ycbcr_img.putpixel((cal,row), (y, cb, cr))

# u v subsampling
sub_ycbcr_img = Image.new('RGB', (int(img_width / 2), int(img_hight / 2)), (0,0,0))
cb_img = basemath.zero(int(img_width / 2), int(img_hight / 2))
cr_img = basemath.zero(int(img_width / 2), int(img_hight / 2))
cal = 0
row = 0
while cal < img_width:
    while row < img_hight:
        y, cb, cr = ycbcr_img.getpixel((cal, row))
        sub_ycbcr_img.putpixel((int(cal/2), int(row/2)), (y, cb, cr ))
        cb_img[int(cal/2)][int(row/2)] = cb
        cr_img[int(cal/2)][int(row/2)] = cr
        row += 2
    row = 0
    cal += 2

# Conversion of DHT marker
[[dc_y_EHUFCO],[dc_y_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 0, marker_debug)
[[ac_y_EHUFCO],[ac_y_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 1, marker_debug)
[[dc_c_EHUFCO],[dc_c_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 2, marker_debug)
[[ac_c_EHUFCO],[ac_c_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 3, marker_debug)

# Conversion of DQT marker
DQT_Y = basemath.shape2m(marker.readfile(jpeg_file, 'DQT', 0, marker_debug))
DQT_C = basemath.shape2m(marker.readfile(jpeg_file, 'DQT', 1, marker_debug))

# Above Are Verified

# Encode
x_offset = 0
y_offset = 0
y_block = basemath.zero(8,8)
cb_block = basemath.zero(8,8)
cr_block = basemath.zero(8,8)
code = ''
for y_offset in range(0, int(img_hight / 16)):
    for x_offset in range(0, int(img_width / 16)):
        # Encode the minimum coded unit(MCU)
        mcu_code = ''
        last_y_dc_value = 0
        last_cb_dc_value = 0
        last_cr_dc_value = 0
        for y_y in [0,8]:
            for y_x in [0,8]:
                # Encode 4 Luma block
                for cal in range(0,8):
                    for row in range(0,8):
                        y_block[cal][row] = ycbcr_img.getpixel((x_offset * 16 + cal + y_x, y_offset * 16 + row + y_y))[0]
                fragment, last_y_dc_value = block.encode(y_block, last_y_dc_value, dc_y_EHUFCO, dc_y_EHUFSI, ac_y_EHUFCO, ac_y_EHUFSI, DQT_Y)
                mcu_code += fragment
        # Encode 2 Chroma block
        for cal in range(0,8):
            for row in range(0,8):
                cb_block[cal][row] = cb_img[x_offset * 8 + cal][y_offset * 8 + row]
                cr_block[cal][row] = cr_img[x_offset * 8 + cal][y_offset * 8 + row]
        fragment, last_cb_dc_value = block.encode(cr_block, last_cb_dc_value, dc_c_EHUFCO, dc_c_EHUFSI, ac_c_EHUFCO, ac_c_EHUFSI, DQT_C)
        mcu_code += fragment
        fragment, last_cr_dc_value = block.encode(cr_block, last_cr_dc_value, dc_c_EHUFCO, dc_c_EHUFSI, ac_c_EHUFCO, ac_c_EHUFSI, DQT_C)
        mcu_code += fragment
        code += mcu_code
        # Show process
        if debug:
            print('Block',x_offset, y_offset, 'MCU code:', mcu_code)
        else:
            process = (x_offset +  y_offset * int(img_width / 16)) / (int(img_hight / 16) * int(img_width / 16)) * 100
            print("\r Process: ", int(process), '%  [', end=' ')
            i = int(process / 5)
            for j in range(0,20):
                if i > 0:
                    print('=',end='')
                else:
                    print(' ',end='')
                i -= 1
            print(']',end='')
hex_code = ''
# 最高位对其，最低位不满1byte的全补1
for i in range(0, 8 - len(code) % 8):
    code += '1'
# 遇到FF后面补一个00
i = 0
while i < len(code) / 8:
    byte = hex(int(code[i*8:i*8+8], 2))[2:].upper()
    if len(byte) == 1:
        byte = '0' + byte
    hex_code += byte
    if byte == 'FF':
        hex_code += '00'
    i += 1

# Output
original_size = img_width * img_hight * 3
encoded_size = int(len(hex_code) / 2)
print('\n')
# marker.readfile(jpeg_file,'SOF0',0,marker_debug)
Ls = marker.readfile(jpeg_file,'SOS',0,marker_debug)[0]
filecode = marker.readfile(jpeg_file,'SOS',0,False)[9]
print('\n   Image real code:', filecode)
print('\nImage encoded code:', hex_code)
print('\nImage original size:', original_size, 'Byte.', original_size / 1024, 'KB\n')
print('\nImage encoded size: ', encoded_size, 'Byte.', encoded_size / 1024, 'KB\n')

# New image jpeg_file:
with open(jpeg_file, 'rb+') as image:
    hex_file = ''
    byte_file = image.read()
    for byte in byte_file:
        text = str(hex(int(byte))[2:].upper())
        if len(text) < 2:
            text = '0' + text
        hex_file += text
for i in range(0,len(hex_file)):
    if i % 2 == 0:
        if hex_file[i-2:i+2] == marker.SOS:
            information = hex_file[:i + Ls * 2 + 2]
new_file = base64.b16decode(information + hex_code + marker.EOI)
with open('./output.jpg', 'wb') as output_img:
    output_img.write(new_file)

# new_img = Image.open('./output.jpg')
# ycbcr_img.show()
# sub_ycbcr_img.show()
# new_img.show()