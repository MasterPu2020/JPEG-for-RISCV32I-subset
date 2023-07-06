# -------------------------------------
# Using UTF-8
# Last Modified Date: 2023/6/28
# JPEG Image file marker pre-decode and tail-encode
# Clark Pu
# -------------------------------------

SOI = 'FFD8' # Start of image marker
APPn = 'FFE0' # Reserved for application segments
DQT = 'FFDB' # Define quantization table(s)
SOF0 = 'FFC0' # Start of Frame (non-differential, Huffman coding) Baseline DCT
DHT = 'FFC4' # Define Huffman table(s)
SOS = 'FFDA' # Start of Scan
EOI = 'FFD9' # End of image marker

# Read the marker in byte
def read_in_byte(marker):
    i = 0
    table = ''
    for hex in marker:
        if i == 2:
            table += ' '
            i = 1
        else:
            i += 1
        table += hex
    return table.split()


# Format print a matrix
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


# DQT: Define quantization table marker decode
def dqt_analysis(marker, show_infor):
    table = read_in_byte(marker)
    if (table[0] + table[1]).upper() == DQT:
        Lq = int(table[2] + table[3], 16) # Quantization table definition length
        Pq = int(table[4][0], 16) # Quantization table element precision
        Tq = int(table[4][1], 16) # Quantization table destination identifier
        if show_infor:
            print('Quantization table definition length:', Lq)
            if Pq == 0:
                print('Quantization table element precision: 8-bit')
            elif Pq == 1:
                print('Quantization table element precision: 16-bit')
            else:
                print('Quantization table element precision: Unknown?')
            print('Quantization table destination identifier:', Tq)
        Qk = [0] * 64 # Quantization table element
        for i in range(0, 64):
            if Pq == 0:
                Qk[i] = int(table[5 + i], 16)
            elif Pq == 0:
                Qk[i] = int(table[6 - 1 + i*2] + table[6 + i*2], 16)
            else:
                return False
        if show_infor:
            print('Quantization table element:')
            format_print(Qk, 3, 8)
            print('\n-------------------------------------\n')
        return Qk
    else:
        return False

import base64

# APPn: Reserved for application segments decode
def appn_analysis(marker, show_infor):
    table = read_in_byte(marker)
    if (table[0] + table[1]).upper() == APPn:
        Lp = int(table[2] + table[3], 16) # Application data segment length
        identifier = base64.b16decode((table[4] + table[5] + table[6] + table[7] + table[8]).upper())
        if show_infor:
            print('Application data segment length:', Lp)
            if identifier == b'JFIF\x00':
                version = str(int(table[9], 16)) + '.' + str(int(table[10], 16))
                units = int(table[11], 16)
                if units == 0:
                    units = 'Aspect ratio. Ydensity : Xdensity'
                elif units == 1:
                    units = 'Dot per inch'
                elif units == 1:
                    units = 'Dot per centimeter'
                x_density = int(table[12] + table[13], 16)
                y_density = int(table[14] + table[15], 16)
                x_thumbnail = int(table[16], 16)
                y_thumbnail = int(table[17], 16)
                Thumbnail_data = table[18:18 + 3 * x_thumbnail * y_thumbnail]
                print('identifier:', identifier)
                print('version:', version)
                print('units:',units )
                print('Horizontal pixel units:', x_density)
                print('Vertical pixel units:', y_density)
                print('x thumbnail:', x_thumbnail)
                print('y thumbnail:', y_thumbnail)
                print('Thumbnail data:', Thumbnail_data)
            else:
                Api = '' # Application data byte
                for i in range(0, Lp - 2):
                    Api += table[4 + i].upper()
                Api = base64.b16decode(Api)
                print('Application data byte:', Api)
            print('\n-------------------------------------\n')
        return True
    else:
        return False
    

# SOS: Start of Scan marker decode
def sos_analysis(marker, show_infor):
    table = read_in_byte(marker)
    if (table[0] + table[1]).upper() == SOS:
        Ls = int(table[2] + table[3], 16) # Scan header length
        Ns = int(table[4], 16) # Number of image components in scan
        Cs = [0] * Ns # Scan component selector
        Td = [0] * Ns # DC entropy coding table destination selector
        Ta = [0] * Ns # AC entropy coding table destination selector
        for j in range(0, Ns):
            Cs[j] = int(table[5 + j * 2], 16)
            Td[j] = int(table[6 + j * 2][0], 16)
            Ta[j] = int(table[6 + j * 2][1], 16)
        Ss = int(table[7 + (Ns - 1) * 2], 16) # Start of spectral or predictor selection
        Se = int(table[8 + (Ns - 1) * 2], 16) # End of spectral selection
        Ah = int(table[9 + (Ns - 1) * 2][0], 16) # Successive approximation bit position high
        Al = int(table[9 + (Ns - 1) * 2][1], 16) # Successive approximation bit position low or point transform
        entropy_code = ''
        for byte in table[10 + (Ns - 1) * 2:-2]:
            entropy_code += byte.upper()
        if show_infor:
            print('Scan header length:', Ls)
            print('Number of image components in scan:', Ns)
            for j in range(0, Ns):
                print('\nScan component selector:', Cs[j] )
                print('DC entropy coding table destination selector:', Td[j])
                print('AC entropy coding table destination selector:', Ta[j])
            print('\nStart of spectral or predictor selection:', Ss)
            print('End of spectral selection:', Se)
            print('Successive approximation bit position high:', Ah)
            print('Successive approximation bit position low or point transform:', Al)
            print('\nEntropy code length:', len(entropy_code)/2, 'byte')
            print('Entropy code:', entropy_code)
            print('END:', table[-2:])
            print('\n-------------------------------------\n')
        return [Ls, Ns, Cs, Td, Ta, Ss, Se, Ah, Al, entropy_code]
    else:
        return False
    

# SOF: Start of frame marker decode
def sof_analysis(marker, show_infor):
    table = read_in_byte(marker)
    if (table[0] + table[1]).upper() == SOF0:
        Lf = int(table[2] + table[3], 16) # Frame header length : 2 byte
        P  = int(table[4], 16) # Sample precision : 1 byte
        Y  = int(table[5] + table[6], 16) # Number of lines : 2 byte
        X  = int(table[7] + table[8], 16) # Number of samples per line : 2 byte
        Nf = int(table[9], 16) # Number of image components in frame : 1 byte
        if show_infor:
            print('\nFrame header length :', Lf)
            print('Sample precision :', P)
            print('Number of lines :', Y)
            print('Number of samples per line :', X)
            print('Number of image components in frame :', Nf)
        C  = [0] * Nf # Component identifier : 1 byte
        H  = [0] * Nf # Horizontal sampling factor : half byte
        V  = [0] * Nf # Vertical sampling factor : half byte
        Tq = [0] * Nf # Quantization table destination selector : 1 byte
        for i in range(0, Nf):
            C[i] = int(table[10 + i*3], 16)
            H[i] = int((table[11 + i*3])[0], 16)
            V[i] = int((table[11 + i*3])[1], 16)
            Tq[i] = int(table[12 + i*3], 16)
            if show_infor:
                print('\nComponent identifier :', C[i])
                print('Horizontal sampling factor:', H[i])
                print('Vertical sampling factor:', V[i])
                print('Quantization table destination selector:', Tq[i])
        print('\n-------------------------------------\n')
        return True
    else:
        return False


# DHT: define huffman table marker decode
def huffman_table_generate(marker, show_infor):
    table = table = read_in_byte(marker)
    if (table[0] + table[1]).upper() == DHT:
        Lh = int(table[2] + table[3], 16) # Huffman table definition length
        Tc = int(table[4][0], 16) # Table class – 0 = DC table or lossless table, 1 = AC table
        if Tc == 0:
            Tc = 'DC'
        elif Tc == 1:
            Tc = 'AC'
        else:
            Tc = 'Unknown'
        Th = int(table[4][1], 16) # Huffman table destination identifier
        # Generate HUFFSIZE and HUFFCODE
        BITS = []
        for byte in table[5:5 + 16]:
            BITS.append(int(byte, 16))
        HUFFVAL = []
        for byte in table[5 + 16 : Lh + 2]:
            HUFFVAL.append(int(byte, 16))
        # Generate HUFFSIZE
        HUFFSIZE = []
        k = 0
        i = 1
        j = 1
        while i < 16: # Bug with itu: i > 16
            while j <= BITS[i]:
                HUFFSIZE.append(i + 1) # Problem exist?: itu-t81 require: HUFFSIZE[k] = i
                k += 1
                j += 1
            i += 1
            j = 1
        HUFFSIZE.append(0)
        last_k = k
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
        # Generate EHUFCO and EHUFSI
        k = 0
        EHUFCO = [0] * (max(HUFFVAL) + 1)
        EHUFSI = [0] * (max(HUFFVAL) + 1)
        while k < last_k:
            i = HUFFVAL[k]
            EHUFCO[i] = HUFFCODE[k]
            EHUFSI[i] = HUFFSIZE[k]
            k += 1
        if show_infor:
            print('Huffman table definition length:', Lh)
            print('Table class:', Tc)
            print('Huffman table destination identifier:', Th)
            print('\nBITS:')
            format_print(BITS, 4, 16)
            print('\nHUFFVAL:')
            format_print(HUFFVAL, 4, 16)
            print('\nHUFFSIZE:')
            format_print(HUFFSIZE, 3, 16)
            print('\nHUFFCODE:')
            format_print(HUFFCODE, 6, 16)
            print('\nEHUFCO:')
            format_print(EHUFCO, 6, 16)
            print('\nEHUFSI:')
            format_print(EHUFSI, 3, 16)
            print('\n-------------------------------------\n')
        return [[EHUFCO],[EHUFSI]]
    else:
        return False


# From an image file read the marker
def readfile(file, marker_name, marker_index, show_infor):
    with open(file, 'rb+') as image:
        hex_file = ''
        byte_file = image.read()
        for byte in byte_file:
            text = str(hex(int(byte))[2:].upper())
            if len(text) < 2:
                text = '0' + text
            hex_file += text
    for i in range(0,len(hex_file)):
        if i % 2 == 0:
            if marker_name == 'APPn' and hex_file[i-2:i+2] == APPn:
                if marker_index > 0:
                    marker_index -= 1
                else:
                    return appn_analysis(hex_file[i-2:], show_infor)
            elif marker_name == 'DQT' and hex_file[i-2:i+2] == DQT:
                if marker_index > 0:
                    marker_index -= 1
                else:
                    return dqt_analysis(hex_file[i-2:], show_infor)
            elif marker_name == 'SOF0' and hex_file[i-2:i+2] == SOF0:
                if marker_index > 0:
                    marker_index -= 1
                else:
                    return sof_analysis(hex_file[i-2:], show_infor)
            elif marker_name == 'DHT' and hex_file[i-2:i+2] == DHT:
                if marker_index > 0:
                    marker_index -= 1
                else:
                    return huffman_table_generate(hex_file[i-2:], show_infor)
            elif marker_name == 'SOS' and hex_file[i-2:i+2] == SOS:
                if marker_index > 0:
                    marker_index -= 1
                else:
                    return sos_analysis(hex_file[i-2:], show_infor)
    return False
