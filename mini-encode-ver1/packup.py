# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/7/1
# Mini JPEG Image file general pack up
# Version 1.0
# Clark Pu
# -------------------------------------

import base64

# Start of image marker
SOI = 'FFD8' 

# APPn + JFIF + version1.1 + Aspect ratio + Horizontal and Vertical pixel units + x y thumbnail and no thumbnail data
ApplicationSegmentsHeader = 'FFE0' + '00104A46494600' + '0101' + '00' + '0001' + '0001' + '00' + '00'
# FFE04A46494600010100000100010000

# Self-defined quantization table
def QuantizationTable(table, identifier:int=0):
    # Marker, length = 67, precision = 8-bit, identifier = 0 for Luma, 1 for Chroma
    code = 'FFDB' + '0043' + '0' + str(identifier)
    for byte in table:
        code += '0' * (2 - len(hex(byte)[2:])) + hex(byte)[2:].upper()
    return code

# 4 Huffman table
FourHuffmanTable ='FFC4001F0000010501010101010100000000000000000102030405060708090A0BFFC400B5100002010303020403050504040000017D01020300041105122131410613516107227114328191A1082342B1C11552D1F02433627282090A161718191A25262728292A3435363738393A434445464748494A535455565758595A636465666768696A737475767778797A838485868788898A92939495969798999AA2A3A4A5A6A7A8A9AAB2B3B4B5B6B7B8B9BAC2C3C4C5C6C7C8C9CAD2D3D4D5D6D7D8D9DAE1E2E3E4E5E6E7E8E9EAF1F2F3F4F5F6F7F8F9FAFFC4001F0100030101010101010101010000000000000102030405060708090A0BFFC400B51100020102040403040705040400010277000102031104052131061241510761711322328108144291A1B1C109233352F0156272D10A162434E125F11718191A262728292A35363738393A434445464748494A535455565758595A636465666768696A737475767778797A82838485868788898A92939495969798999AA2A3A4A5A6A7A8A9AAB2B3B4B5B6B7B8B9BAC2C3C4C5C6C7C8C9CAD2D3D4D5D6D7D8D9DAE2E3E4E5E6E7E8E9EAF2F3F4F5F6F7F8F9FA'

# Start of Frame (non-differential, Huffman coding) Baseline DCT
def StartOfFrameHeader(hight:int, width:int):
    lines = '0' * (4 - len( hex(hight)[2:])) + hex(hight)[2:].upper()
    samples_per_line = '0' * (4 - len( hex(width)[2:])) + hex(width)[2:].upper()
    # Maeker + length = 17 + Sample precision = 8 + hight + width + component information
    code = 'FFC0' + '001108' + lines + samples_per_line + '03012200021101031101'
    return code

# Start of scan header: 3 componets
StartOfScanHeader = 'FFDA' + '000C03010002110311003F00'

# End of image marker
EOI = 'FFD9' 

# Packed Function and Save file
def save(file_path:str, image_hight:int, image_width:int, image_hex_code:str, quantization_table0:list, quantization_table1:list):
    file_hex = SOI
    file_hex += ApplicationSegmentsHeader
    file_hex += QuantizationTable(quantization_table0, 0)
    file_hex += QuantizationTable(quantization_table1, 1)
    file_hex += StartOfFrameHeader(image_hight, image_width)
    file_hex += FourHuffmanTable
    file_hex += StartOfScanHeader
    file_hex += image_hex_code
    file_hex += EOI
    file_code = base64.b16decode(file_hex)
    with open(file_path, 'wb') as output_file:
        output_file.write(file_code)
