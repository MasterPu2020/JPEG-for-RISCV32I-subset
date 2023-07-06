# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/24
# Python JPEG marker reader
# Protocal: itu-t81
# Clark Pu
# -------------------------------------

def huffman_table_reader(hex_text, debug):
    
    i = 0
    table = ''
    for hex in hex_text:
        if i == 2:
            table += ' '
            i = 1
        else:
            i += 1
        table += hex
    table = table.split()
    
    if table[0] + table[1] == 'FFC4' or table[0] + table[1] == 'ffc4':
        Lh = int(table[2] + table[3], 16)
        Tc = int(table[4][0], 16) # 高4位
        if Tc == 0:
            Tc = 'DC table'
        elif Tc == 1:
            Tc = 'AC table'
        else:
            Tc = 'Unknown'
        Th = int(table[4][1], 16) # 低4位
        # Generate HUFFSIZE and HUFFCODE
        BITS = []
        for byte in table[5:5 + 16]:
            BITS.append(int(byte, 16))
        HUFFVAL = []
        for byte in table[5 + 16:]:
            HUFFVAL.append(int(byte, 16))

        if debug:
            print('\nDHT mark: FFC4')
            print('Huffman table definition length:', Lh)
            print('Table class:', Tc)
            print('Huffman table destination identifier:', Th)
            print('Huffman codes of length:', BITS)
            print('Huffman values:', HUFFVAL)

        return [[BITS],[HUFFVAL]]
    
        # # <Debug
        # L =[]
        # for byte in table[5:5 + 16]:
        #     L.append(int(byte, 16))
        # print('Huffman codes of length:\n', L)

        # offset = 0
        # index = 0
        # V = []
        # V_hex = []
        # for item in L:
        #     offset = offset + item
        #     element_hex = ''
        #     element = ''
        #     while index < offset:
        #         element_hex += (table[5 + 16 + index] + ' ').upper()
        #         element += str(int(table[5 + 16 + index], 16)) + ' '
        #         index += 1
        #     if element_hex != '':
        #         V_hex.append(element_hex.split())
        #         V.append(list(map(int, element.split())))
        # print('Huffman values:')
        # for item in V:
        #     print(item)

        # print('HEX Huffman values:')
        # length = 0
        # for item in V_hex:
        #     text = ''
        #     for word in item:
        #         text += word + ' '
        #         length += 1
        #     print(text)
        # print('Length is:', length, '. Sum of Li is:', sum(L))
        # # Debug>

    else:
        return 'failed'


def format_print(vector, space, enter):
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


def huffman_table_generate(marker, debug):
    
    [[BITS], [HUFFVAL]] = huffman_table_reader(marker, debug)
    if debug:
        print('\nBITS:')
        format_print(BITS, 4, 16)
        print('\nHUFFVAL:')
        format_print(HUFFVAL, 4, 16)

    # Generate HUFFSIZE
    HUFFSIZE = []
    k = 0
    i = 1
    j = 1
    while i < 16: # Bug with itu: i > 16
        while j <= BITS[i]:
            HUFFSIZE.append(i + 1) # Problem exist?: itu require: HUFFSIZE[k] = i
            k += 1
            j += 1
        i += 1
        j = 1
    HUFFSIZE.append(0)
    last_k = k
    if debug:
        print('\nHUFFSIZE:')
        format_print(HUFFSIZE, 3, 16)

    # Generate HUFFCODE
    HUFFCODE = [None] * last_k
    k = 0
    code = 0
    si = HUFFSIZE[0]
    while True:
        while HUFFSIZE[k] == si:
            HUFFCODE[k] = code
            code += 1
            k += 1
        if HUFFSIZE[k] == 0:
            break
        while not HUFFSIZE[k] == si: # 2**i
            code = code << 1 
            si += 1
    if debug:
        print('\nHUFFCODE:')
        format_print(HUFFCODE, 6, 16)

    # Generate EHUFCO and EHUFSI
    k = 0
    EHUFCO = [0] * (max(HUFFVAL) + 1)
    EHUFSI = [0] * (max(HUFFVAL) + 1)
    while k < last_k:
        i = HUFFVAL[k]
        EHUFCO[i] = HUFFCODE[k]
        EHUFSI[i] = HUFFSIZE[k]
        k += 1
    if debug:
        print('\nEHUFCO:')
        format_print(EHUFCO, 6, 16)
        print('\nEHUFSI:')
        format_print(EHUFSI, 3, 16)
        print('\n')

    return [[EHUFCO],[EHUFSI]]


# # Debug

# dc_luminance =   'ffc4001f0000010501010101010100000000000000000102030405060708090a0b'
# dc_chrominance = 'ffc400b5100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a161718191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9fa'
# ac_luminance =   'ffc4001f0100030101010101010101010000000000000102030405060708090a0b'
# ac_chrominace =  'ffc400b51100020102040403040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a35363738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9fa'

# huffman_table_generate(dc_luminance)
# huffman_table_generate(ac_luminance)
# huffman_table_generate(dc_chrominance)
# huffman_table_generate(ac_chrominace)
