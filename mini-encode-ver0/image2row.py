
# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/7/4
# Python Image to ROW data
# Version: 1.0
# Author: Clark Pu
# -------------------------------------

# File structure: 32-bit image width + 32-bit image hight + nx32-bit RGB pixel data
# Data Format: One pixel with 32-bit (Double Word) 
# RGB data align to lower bit
# +---------------------------------------------------+
# | 8-bit Zero | 8-bit Red | 8-bit Green | 8-bit Blue |
# +---------------------------------------------------+


from PIL import Image
import base64

def convert(file):
    # load image data
    rgb_img = Image.open(file).convert('RGB')
    img_width, img_hight = rgb_img.size

    # encode as row file
    row_img = [img_hight, img_width]
    max_index = img_width * img_hight
    index = 0
    while index != max_index:
        r, g, b = rgb_img.getpixel((index % img_width, int(index / img_width)))
        assert (r >= 0) and (g >= 0) and (b >= 0)
        pixel_data = (r << 16) + (g << 8) + b
        row_img.append(pixel_data)
        index += 1

    # base64 encode
    hexcode = ''
    for doubleword in row_img:
        hexcode += '0' * (8 - len(hex(doubleword)[2:])) + hex(doubleword)[2:].upper() # + '\n'
    row_data = base64.b16decode(hexcode)
    with open('./image.row', 'wb') as output_img:
        output_img.write(row_data)
    print('\n[Done]\n')
