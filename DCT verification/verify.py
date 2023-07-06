

import block
import basemath as bs


matrix = [[16 for i in range(8)] for j in range(8)]
print('\nOriginal Matrix:')
bs.dis_block(matrix, 4)

# DCT
print('Matrix - 128:')
matrix = bs.op(matrix, 128, '-')
bs.dis_block(matrix, 4)

print('Matrix Forward DCT:')
matrix = block.fdct(matrix)
matrix = bs.op(matrix, 0, 'int')
bs.dis_block(matrix, 4)

# Reverse DCT
print('Matrix Inverse DCT:')
matrix = block.idct(matrix)
matrix = bs.op(matrix, 0, 'int')
bs.dis_block(matrix, 4)

print('Matrix + 128:')
matrix = bs.op(matrix, 128, '+')
bs.dis_block(matrix, 4)