# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/7/1
# Python Image JPEG encode and decode
# Version 5.0
# Clark Pu
# -------------------------------------


import basicmath as bm
import marker
import base64
from PIL import Image


# JPEG file encode
def encode(file_name:str):

    # Get the image data
    jpeg_file = file_name + '.bmp'
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
            y, cb, cr = bm.rgb2ycbcr(r,g,b)
            ycbcr_img.putpixel((cal,row), (y, cb, cr))

    # u v subsampling
    sub_ycbcr_img = Image.new('RGB', (int(img_width / 2), int(img_hight / 2)), (0,0,0))
    cb_img = bm.zero(int(img_width / 2), int(img_hight / 2))
    cr_img = bm.zero(int(img_width / 2), int(img_hight / 2))
    cal = 0
    row = 0
    while cal < img_width:
        while row < img_hight:
            y, cb, cr = ycbcr_img.getpixel((cal, row))
            dy, dcb, dcr = ycbcr_img.getpixel((cal+1, row))
            y, cb, cr = y + dy, cb + dcb, cr + dcr 
            dy, dcb, dcr = ycbcr_img.getpixel((cal, row+1))
            y, cb, cr = y + dy, cb + dcb, cr + dcr 
            dy, dcb, dcr = ycbcr_img.getpixel((cal+1, row+1))
            y, cb, cr = y + dy, cb + dcb, cr + dcr 
            y, cb, cr = int(y/4), int(cb/4), int(cr/4)
            sub_ycbcr_img.putpixel((int(cal/2), int(row/2)), (y, cb, cr))
            cb_img[int(cal/2)][int(row/2)] = cb
            cr_img[int(cal/2)][int(row/2)] = cr
            row += 2
        row = 0
        cal += 2

    # Conversion of DHT marker
    dc_y_EHUFCO, dc_y_EHUFSI, dc_dht_id0 = marker.readfile(jpeg_file, 'DHT', 0)
    ac_y_EHUFCO, ac_y_EHUFSI, ac_dht_id0 = marker.readfile(jpeg_file, 'DHT', 1)
    dc_c_EHUFCO, dc_c_EHUFSI, dc_dht_id1 = marker.readfile(jpeg_file, 'DHT', 2)
    ac_c_EHUFCO, ac_c_EHUFSI, ac_dht_id1 = marker.readfile(jpeg_file, 'DHT', 3)

    # Conversion of DQT marker
    dqt_id0, DQT_Y = marker.readfile(jpeg_file, 'DQT', 0)
    dqt_id1, DQT_C = marker.readfile(jpeg_file, 'DQT', 1)
    DQT_Y = bm.shape2m(DQT_Y)
    DQT_C = bm.shape2m(DQT_C)

    # Block Encode Pacakge. Must be YCbCr block
    def block_encode(block, last_dc_value, dht_code_dc, dht_size_dc, dht_code_ac, dht_size_ac, dqt):
        # Discrete Cosine Transform
        block = bm.op(block, '-', 128)
        block = bm.fdct(block)
        # Quantization
        block = bm.op(bm.op_block(block, '/', dqt), 'int')
        # Zigzag Scan
        block = bm.zigzag_scan(block)
        # Huffman Encode
        this_dc_value =block[0]
        block[0] = block[0] - last_dc_value
        block = bm.huffman_encode(block, dht_code_dc, dht_size_dc, dht_code_ac, dht_size_ac)
        return block, this_dc_value

    # Encode
    x_offset = 0
    y_offset = 0
    y_block = bm.zero(8,8)
    cb_block = bm.zero(8,8)
    cr_block = bm.zero(8,8)
    code = ''
    last_y_dc_value = 0
    last_cb_dc_value = 0
    last_cr_dc_value = 0
    for y_offset in range(0, int(img_hight / 16)):
        for x_offset in range(0, int(img_width / 16)):
            # Encode the minimum coded unit(MCU)
            mcu_code = ''
            for y_y in [0,8]:
                for y_x in [0,8]:
                    # Encode 4 Luma block
                    for cal in range(0,8):
                        for row in range(0,8):
                            y_block[cal][row] = ycbcr_img.getpixel((x_offset * 16 + cal + y_x, y_offset * 16 + row + y_y))[0]
                    fragment, last_y_dc_value = block_encode(y_block, last_y_dc_value, dc_y_EHUFCO, dc_y_EHUFSI, ac_y_EHUFCO, ac_y_EHUFSI, DQT_Y)
                    mcu_code += fragment
            # Encode 2 Chroma block
            for cal in range(0,8):
                for row in range(0,8):
                    cb_block[cal][row] = cb_img[x_offset * 8 + cal][y_offset * 8 + row]
                    cr_block[cal][row] = cr_img[x_offset * 8 + cal][y_offset * 8 + row]
            fragment, last_cb_dc_value = block_encode(cb_block, last_cb_dc_value, dc_c_EHUFCO, dc_c_EHUFSI, ac_c_EHUFCO, ac_c_EHUFSI, DQT_C)
            mcu_code += fragment
            fragment, last_cr_dc_value = block_encode(cr_block, last_cr_dc_value, dc_c_EHUFCO, dc_c_EHUFSI, ac_c_EHUFCO, ac_c_EHUFSI, DQT_C)
            mcu_code += fragment
            code += mcu_code
            # Show process
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
    print('\n\n')

    hex_code = ''
    # Fill the lefted area with 1 
    for i in range(0, 8 - len(code) % 8):
        code += '1'
    # 'FF' follows the '00'
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
    Ls = marker.readfile(jpeg_file, 'SOS', 0)[0]
    print('+=======================+')
    print('| Image original size: |', original_size, 'Byte.', original_size / 1024, 'KB')
    print('| Image  encoded size: |', encoded_size, 'Byte.', encoded_size / 1024, 'KB')
    print('+=======================+')

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
    with open('./encode.jpg', 'wb') as output_img:
        output_img.write(new_file)


# JPEG file decode. Y:Cb:Cr = 2:1:1
def decode(file_name:str):
    # Extract file data
    file_code = marker.readfile(file_name+'.jpg','SOS', 0)[9]
    file_code = file_code.replace('FF00', 'FF')
    file_code = bin(int(file_code, 16))[2:]
    DQT_Y = bm.shape2m(marker.readfile(file_name+'.jpg', 'DQT', 0)[1])
    DQT_C = bm.shape2m(marker.readfile(file_name+'.jpg', 'DQT', 1)[1])
    # Extract file imformation
    msg = marker.readfile(file_name+'.jpg','SOF0', 0)
    hight = msg[2]
    width = msg[3]
    block_amount = int((hight * width) / (16 * 16) * 6)
    # Decode image
    last_dc_value = [0,0,0] # Y, Cb, Cr
    this_dc_value = [0,0,0] # Y, Cb, Cr
    image_data = [bm.zero(width, hight), bm.zero(width, hight), bm.zero(width, hight)]
    max_block_l = [int(width/8)-1,int(hight/8)-1]
    max_block_c = [int(width/16)-1,int(hight/16)-1]
    block_l = [0,0]
    block_c = [0,0]
    for i in range(0,block_amount):
        # Differential DC value
        if i % 6 < 4:
            layer = 0
            mode = 'L'
        elif i % 6 == 4:
            layer = 1
            mode = 'C'
        else:
            layer = 2
            mode = 'C'
        # Huffman decode
        block, file_code = bm.huffman_decode(file_code, mode=mode)
        # Differential DC Value to DC Value
        this_dc_value[layer] = block[0] + last_dc_value[layer]
        block[0] = this_dc_value[layer]
        last_dc_value[layer] = this_dc_value[layer]
        # Reversed Quantization
        block = bm.shape2m(block)
        if layer == 0:
            block = bm.op_block(block, '*', DQT_Y)
        else: 
            block = bm.op_block(block, '*', DQT_C)
        block = bm.shape2v(block)
        # Reversed Zigzag
        block = bm.reverse_zigzag_scan(block)
        # Reversed DCT
        block = bm.idct(block)
        block = bm.op(block, '+', 128)
        block = bm.op(block, 'int')
        # Assembly the Image
        if layer == 0:
            for x in range(0,8):
                for y in range(0,8):
                    image_data[0][x + block_l[0] * 8][y + block_l[1] * 8] = block[x][y]
            if block_l[0] == max_block_l[0] and i % 6 == 3:
                block_l[0] = 0
                block_l[1] += 1
            else:
                if i % 6 == 0:
                    block_l[0] += 1
                    block_l[1] += 0
                elif i % 6 == 1:
                    block_l[0] -= 1
                    block_l[1] += 1
                elif i % 6 == 2:
                    block_l[0] += 1
                    block_l[1] += 0
                elif i % 6 == 3:
                    block_l[0] += 1
                    block_l[1] -= 1
        else:
            for x in range(0,8):
                for y in range(0,8):
                    image_data[layer][2*x + block_c[0] * 16    ][2*y + block_c[1] * 16    ] = block[x][y]
                    image_data[layer][2*x + block_c[0] * 16 + 1][2*y + block_c[1] * 16    ] = block[x][y]
                    image_data[layer][2*x + block_c[0] * 16    ][2*y + block_c[1] * 16 + 1] = block[x][y]
                    image_data[layer][2*x + block_c[0] * 16 + 1][2*y + block_c[1] * 16 + 1] = block[x][y]
            if layer == 2:
                if block_c[0] == max_block_c[0]:
                    if block_c[1] == max_block_c[1]:
                        break
                    block_c[0] = 0
                    block_c[1] += 1
                else:
                    block_c[0] += 1
        # Show process
        process = i / block_amount * 100
        print("\r Process: ", int(process), '%  [', end=' ')
        pr = int(process / 5)
        for j in range(0,20):
            if pr > 0:
                print('=',end='')
            else:
                print(' ',end='')
            pr -= 1
        print(']',end='')
    
    # Convert to RGB and Save the image
    img_decoded = Image.new('RGB', (width, hight), (0,0,0))
    for x in range(0,width):
        for y in range(0,hight):
            r, g, b = bm.ycbcr2rgb(image_data[0][x][y], image_data[1][x][y], image_data[2][x][y])
            img_decoded.putpixel((x, y), (r, g, b))
    
    print('\r[ Image Decoding finished ]. File code remained:', file_code, '\n')
    img_decoded.save('decoded_image.jpg')
