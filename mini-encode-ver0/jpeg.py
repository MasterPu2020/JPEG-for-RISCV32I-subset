# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/7/4
# Python Image JPEG mini encode
# Only encode with fixed image size and fixed quantization table and huffman table
# Image Size: 128x128 8-bit
# Version 6.0
# Clark Pu
# -------------------------------------


import basicmath as bm
import packup


# Debug
def show(block_list):
    for i in range(0,8):
        k = ''
        for j in range(0,8):
            k += str(block_list[i*8 + j]) + ' '
        print(k)
    print()


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
    mcu_rows = int(hight / 16)
    mcu_cals = int(width / 16)
    
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
                            y, cb, cr = bm.rgb2ycbcr(r, g, b)
                            img_row.append(y)
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
    huffman_bit_stack = [0]
    stack_space = 32

    def block_encode(block:list, last_dc_value, stack, space, mode:int=0):
        # print('Original Block:')
        # show(block) # Debug
        block = bm.op(block, '-', 128)
        block = bm.dct(block) # Discrete Cosine Transform
        if mode == 0:
            quan_table = bm.luminance_quantization_table
        else:
            quan_table = bm.chrominance_quantization_table
        block = bm.divide(block, quan_table) # Quantization
        block = bm.zigzag_scan(block) # Zigzag Scan
        this_dc_value = block[0] # Differential DC Value
        block[0] = this_dc_value - last_dc_value 
        # print('Zigzag List:')
        # show(block) # Debug
        stack, space = bm.huffman_encode(block, stack, space, mode) # Huffman Encode
        return stack, space, this_dc_value 

    # Y Cb Cr subsampling and encode
    blockY = [0] * 64 # Y image blocks 32-bit * 64 integers
    blockCb = [0] * 64 # U image blocks 32-bit * 64 integers
    blockCr = [0] * 64 # V image blocks 32-bit * 64 integers
    index = 0
    counter = 0
    block_counter = 0
    last_dc_value = [0, 0, 0]
    while index < (mcu_rows * mcu_cals * 16 * 16 * 3):
        # Sampling
        blockY[counter]   = img_row[index]
        blockCb[counter] += img_row[index + 1]
        blockCr[counter] += img_row[index + 2]
        # Block encode
        if counter == 63:
            huffman_bit_stack, stack_space, last_dc_value[0] = block_encode(blockY, last_dc_value[0], huffman_bit_stack, stack_space, 0)
            counter = 0
            # Cb Cr subsampling
            if block_counter == 3:
                i = 0
                while i < 64:
                    blockCb[i] = int(blockCb[i] / 4)
                    blockCr[i] = int(blockCr[i] / 4)
                    i += 1
                # Cb Cr Block encode
                huffman_bit_stack, stack_space, last_dc_value[1] = block_encode(blockCb, last_dc_value[1], huffman_bit_stack, stack_space, 1)
                huffman_bit_stack, stack_space, last_dc_value[2] = block_encode(blockCr, last_dc_value[2], huffman_bit_stack, stack_space, 1)
                print('\r [Process]: (', index+3, '/', hight * width * 3, ')', end='')
                block_counter = 0
                i = 0
                while i < 64:
                    blockCb[i] = 0
                    blockCr[i] = 0
                    i += 1
            else:
                block_counter += 1
        else:
            counter += 1
        index += 3

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

    
    print('\r [Finished]\n')
    print(' Size:',int(len(hex_huffman_string) / 2), 'bytes.\n')

    # Generate file
    packup.save(file_path+'.jpg', hight, width, hex_huffman_string, bm.luminance_quantization_table, bm.chrominance_quantization_table)

