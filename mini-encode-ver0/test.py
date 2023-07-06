import basicmath as bm
from PIL import Image
import image2row
import packup
import jpeg


def see_row(file):
    img_row = jpeg.get_row(file)
    hight = img_row[0]
    width = img_row[1]
    img = Image.new('RGB', (hight, width))
    i = 0
    index = 2
    while index < (width * hight + 2):
        r = (img_row[index] >> 16) & 255
        g = (img_row[index] >> 8) & 255
        b = img_row[index] & 255
        x = i % width
        y = int(i / width)
        img.putpixel((x,y),(r,g,b))
        i += 1
        index += 1
    img.show()


image2row.convert('test.jpg')
jpeg.encode('image')

# see_row('image.row')
