

import marker
import basemath


# EHUFCO: huffman code, value is the value of the binary huffman code
# EHUFSI: huffman size, value is the size of the binary huffman code
# The index of the huffman code is the size of the data
# In AC tables, the index formed as Zero/DataSize


debug = True
marker_debug = False and debug
jpeg_file = 'night.jpg'
code = marker.readfile(jpeg_file,'SOS',0,False)[9]
code = code.replace('FF00', 'FF')
[[dc_y_EHUFCO],[dc_y_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 0, marker_debug)
[[ac_y_EHUFCO],[ac_y_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 1, marker_debug)
[[dc_c_EHUFCO],[dc_c_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 2, marker_debug)
[[ac_c_EHUFCO],[ac_c_EHUFSI]] = marker.readfile(jpeg_file, 'DHT', 3, marker_debug)

# print('\nEHUFCO:')
# marker.format_print(dc_y_EHUFCO, 4, 16)
# print('\nEHUFSI:')
# marker.format_print(dc_y_EHUFSI, 3, 16)
# print('\nEHUFCO:')
# marker.format_print(ac_y_EHUFCO, 6, 16)
# print('\nEHUFSI:')
# marker.format_print(ac_y_EHUFSI, 3, 16)

# binary to decimal with a reverse function
def get_value(value_bin):
    value = ''
    if value_bin == '': # if it is empty
        value = 'Empty'
    else:
        if value_bin[0] == '0':
            for bit in value_bin:
                if bit == '1':
                    value += '0'
                else:
                    value += '1'
            value = - int(value, 2)
        else:
            value = int(value_bin, 2)
    return value


# Index to code
def index2code(index, co, si):
    code = bin(co[index])[2:]
    size = si[index]
    # 补齐code
    for i in range(0, size - len(code)):
        code = '0' + code
    return code


# Search for code and convert to code length
def code2length(code, co, si):
    for index in range(0,len(co)):
        if code == index2code(index, co, si) and si[index] != 0:
            return index, si[index]
    return 0, 17


# Return the first value and rest of the DC code
def DCcode2value(code, co, si):
    fragment = ''
    i = 0
    if code != 'Failed':
        while i < len(code):
            fragment += code[i]
            # Check the if the fragment is a huffman code
            index, length = code2length(fragment, co, si)
            # It is a huffman code, then
            if length != 17: 
                # Get Data
                i += 1
                bin_data = code[i:i + index]
                data = get_value(bin_data)
                print('DC Code:', fragment, ' Code Size:', length, ' Data:', bin_data, ' : ', data, ' Data Size:', index)
                i += index
                return data, code[i:]
            i += 1
    return 0, 'Failed'


# Return the first value and rest of the AC code
def ACcode2value(code, co, si):
    fragment = ''
    i = 0
    if code != 'Failed':
        while i < len(code):
            fragment += code[i]
            # Check the if the fragment is a huffman code
            index, length = code2length(fragment, co, si)
            # It is a huffman code, then
            if length != 17:
                # Get Zeros / DataSize
                hex_index = hex(index)[2:]
                if len(hex_index) < 2:
                    data_size = index
                    zeros = 0
                    hex_index = '0' + hex_index
                else:
                    data_size = int(hex_index[1], 16)
                    zeros = int(hex_index[0], 16)
                # Get Data
                i += 1
                if (hex_index != '00'):
                    bin_data = code[i:i + data_size]
                    data = get_value(bin_data)
                else:
                    bin_data = 'Empty'
                    data = 'EOB'
                    zeros = 'EOB'
                print('AC Code:', fragment, ' Code Size:', length, ' Data:', bin_data, ' : ', data, 'Zeros:', zeros, ' Zeros/DataSize:', hex_index)
                i += data_size
                return zeros, data, code[i:]
            i += 1
    return 0, 'Failed'


print('\nRemained code length:', len(code))
print('Code remained:', code, '\n------------------------------')
code = bin(int(code, 16))[2:]
while len(code) > 6:
    for i in range(0,4):
        print('\nStage:L')
        data, code = DCcode2value(code, dc_y_EHUFCO, dc_y_EHUFSI)
        counter = 0
        while data != 'EOB' and code != '' and counter < 64:
            counter += 1
            print('No.', counter, ': ', end='')
            zeros, data, code = ACcode2value(code, ac_y_EHUFCO, ac_y_EHUFSI)
    
    print('\nStage:Cb')
    data, code = DCcode2value(code, dc_c_EHUFCO, dc_c_EHUFSI)
    counter = 0
    while data != 'EOB' and code != '' and counter < 64:
        counter += 1
        print('No.', counter, ': ', end='')
        zeros, data, code = ACcode2value(code, ac_c_EHUFCO, ac_c_EHUFSI)
    
    print('\nStage:Cr')
    data, code = DCcode2value(code, dc_c_EHUFCO, dc_c_EHUFSI)
    counter = 0
    while data != 'EOB' and code != '' and counter < 64:
        if len(code) < 20:
            print('Remained code length:', len(code))
            print('Code remained:', code, '\n------------------------------')
        counter += 1
        print('No.', counter, ': ', end='')
        zeros, data, code = ACcode2value(code, ac_c_EHUFCO, ac_c_EHUFSI)
        