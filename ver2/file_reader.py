
import marker

file = 'output.jpg'

with open(file, 'rb+') as image:
    hex_file = ''
    byte_file = image.read()
    for byte in byte_file:
        text = str(hex(int(byte))[2:].upper())
        if len(text) < 2:
            text = '0' + text
        hex_file += text

text = ''
i = 0
print('\nFile name:', file)
print('\n-------------------------------------\n')
for half_byte in hex_file:
    i += 1
    text += half_byte
    if text[-2:] == 'FF' and i % 2 == 0:
        # print(i, ' : ',hex_file[i-2:i+2])
        clear = marker.check_mark(hex_file[i-2:])
        if clear:
            text = ''
