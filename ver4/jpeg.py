# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/7/1
# Python Image JPEG encode and decode
# Clark Pu
# -------------------------------------


import basicmath as bm
import marker
import base64
from PIL import Image


# JPEG file encode
def encode(file_name:str, show_process=False, show_detail=False, show_file_detail=False, show_dqt=False, show_dht=False, show_ycbcr=False, show_subsampling=False, use_bmp=False):

    jpeg_file = file_name + '.jpg'
    if use_bmp:
        rgb_img = Image.open(file_name + '.bmp').convert('RGB')
    else:
        rgb_img = Image.open(jpeg_file).convert('RGB')
    img_width, img_hight = rgb_img.size
    
    # # Force Debug
    # rgb_img = Image.new('RGB', (img_width, img_hight), (255,0,0))

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
    dc_y_EHUFCO, dc_y_EHUFSI, dc_dht_id0 = marker.readfile(jpeg_file, 'DHT', 0, show_dht)
    ac_y_EHUFCO, ac_y_EHUFSI, ac_dht_id0 = marker.readfile(jpeg_file, 'DHT', 1, show_dht)
    dc_c_EHUFCO, dc_c_EHUFSI, dc_dht_id1 = marker.readfile(jpeg_file, 'DHT', 2, show_dht)
    ac_c_EHUFCO, ac_c_EHUFSI, ac_dht_id1 = marker.readfile(jpeg_file, 'DHT', 3, show_dht)

    # Conversion of DQT marker
    dqt_id0, DQT_Y = marker.readfile(jpeg_file, 'DQT', 0, show_dqt)
    dqt_id1, DQT_C = marker.readfile(jpeg_file, 'DQT', 1, show_dqt)
    DQT_Y = bm.shape2m(DQT_Y)
    DQT_C = bm.shape2m(DQT_C)

    # Block Encode Pacakge. Must be YCbCr block
    def block_encode(block, last_dc_value, dht_code_dc, dht_size_dc, dht_code_ac, dht_size_ac, dqt, show_block_encode):
        if show_block_encode:
            print('\nOriginal Block:')
            bm.dis_block(block, 4)
        # Discrete Cosine Transform
        block = bm.op(block, '-', 128)
        block = bm.fdct(block)
        # if show_block_encode and show_detail:
        #     print('DCT Block:')
        #     bm.dis_block(bm.op(block, 'int'), 4)
        # Quantization
        block = bm.op(bm.op_block(block, '/', dqt), 'int')
        # if show_block_encode and show_detail:
        #     print('Quantized Block:')
        #     bm.dis_block(block, 4)
        # Zigzag Scan
        block = bm.zigzag_scan(block)
        # Huffman Encode
        this_dc_value =block[0]
        block[0] = block[0] - last_dc_value
        if show_block_encode:
            print('Zigzag List:')
            bm.display(block, 4, 8)
        block = bm.huffman_encode(block, dht_code_dc, dht_size_dc, dht_code_ac, dht_size_ac, debug=show_block_encode and show_detail)
        if show_block_encode:
            print('\nHuffman Code:', block, '\n--------------------------------------')
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
                    fragment, last_y_dc_value = block_encode(y_block, last_y_dc_value, dc_y_EHUFCO, dc_y_EHUFSI, ac_y_EHUFCO, ac_y_EHUFSI, DQT_Y, show_process)
                    mcu_code += fragment
                    # print('Luminace Block',int((x_offset * 16 + cal + y_x + 1)/8 - 1), int((y_offset * 16 + row + y_y + 1)/8 - 1))
            # Encode 2 Chroma block
            for cal in range(0,8):
                for row in range(0,8):
                    cb_block[cal][row] = cb_img[x_offset * 8 + cal][y_offset * 8 + row]
                    cr_block[cal][row] = cr_img[x_offset * 8 + cal][y_offset * 8 + row]
            fragment, last_cb_dc_value = block_encode(cb_block, last_cb_dc_value, dc_c_EHUFCO, dc_c_EHUFSI, ac_c_EHUFCO, ac_c_EHUFSI, DQT_C, show_process)
            mcu_code += fragment
            fragment, last_cr_dc_value = block_encode(cr_block, last_cr_dc_value, dc_c_EHUFCO, dc_c_EHUFSI, ac_c_EHUFCO, ac_c_EHUFSI, DQT_C, show_process)
            mcu_code += fragment
            code += mcu_code
            # Show process
            if show_process:
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
    if show_file_detail:
        marker.readfile(jpeg_file,'SOF0',0, show_file_detail)
    Ls = marker.readfile(jpeg_file, 'SOS', 0, show_file_detail)[0]
    filecode = marker.readfile(jpeg_file,'SOS',0,False)[9]
    if show_process:
        print('+=======================+')
        print('      Image real code:', filecode)
        print('   Image encoded code:', hex_code)
        print('+=======================+\n')
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
    with open('./output.jpg', 'wb') as output_img:
        output_img.write(new_file)

    if show_ycbcr:
        ycbcr_img.show()

    if show_subsampling:
        sub_ycbcr_img.show()


# JPEG file decode. Y:Cb:Cr = 2:1:!
def decode(file_name:str, debug=False, show_image=False, show_huffman_decode=False):
    # Extract file data
    file_code = marker.readfile(file_name+'.jpg','SOS', 0)[9]
    file_code = file_code.replace('FF00', 'FF')
    file_code = bin(int(file_code, 16))[2:]
    DQT_Y = bm.shape2m(marker.readfile(file_name+'.jpg', 'DQT', 0, debug)[1])
    DQT_C = bm.shape2m(marker.readfile(file_name+'.jpg', 'DQT', 1, debug)[1])
    # Extract file imformation
    msg = marker.readfile(file_name+'.jpg','SOF0', 0, debug)
    hight = msg[2]
    width = msg[3]
    block_amount = int((hight * width) / (16 * 16) * 6)
    if debug:
        print('Total Block to be decoded:', block_amount, '\n')
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
        block, file_code = bm.huffman_decode(file_code, mode=mode, debug=show_huffman_decode)
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
        if debug:
            if layer == 0:
                print('Luminace Block ', i%6+1, 'in MCU', int(i/6), '.image is:')
            elif layer == 1:
                print('Blue Chrominace Block in MCU', int(i/6), '.image is:')
            else:
                print('Red Chrominace Block in MCU', int(i/6-1), '.image is:')
            bm.dis_block(block)
        # Assembly the Image
        if layer == 0:
            if debug:
                print('Block L, Location: ', block_l[0], block_l[1], '\n\n')
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
            if debug:
                print('Block C, Location: ', block_c[0], block_c[1], '\n\n')
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
        if debug == False:
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
    # Show the final image
    if show_image:
        img_decoded.show()
    img_decoded.save('decoded_image.jpg')
