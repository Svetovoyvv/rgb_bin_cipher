import sys
import pathlib
from PIL import Image

if len(sys.argv) < 3:
    print('usage: python cipher.py <path_to_file> <size: WxH>')
    sys.exit(1)

path = pathlib.Path(sys.argv[1])
if not path.exists() or path.is_dir():
    print('invalid path')
    sys.exit(1)
try:
    width, height = map(int, sys.argv[2].split('x'))
    assert width > 0 and height > 0
    assert width % 24 == 0
except ValueError:
    print('invalid size')
    sys.exit(1)
except AssertionError:
    print('Width and height must be positive and width must be a multiple of 24')
    sys.exit(1)

img = Image.open(path)
print('Converting to black and white')
img = img.convert('1')
img.save(path.parent / (path.name + '_bw.png'))
if img.size[0] != width or img.size[1] != height:
    print('resizing image')
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(path.parent / (path.name + '_resized.png'))
print('Converting to text')
r = ""
for x in range(img.height):
    for y in range(img.width):
        r += '0' if img.getpixel((y, x)) == 0 else '1'
    r += '\n'
with open(path.parent / (path.name + '.txt'), 'w') as f:
    f.write(r)
r = r.splitlines()
r = [int(i, 2).to_bytes(len(i)//8, 'big') for i in r]
print('Creating secret storage')

img = Image.new('RGB', (width // 24, height))
for i in range(img.size[0]):
    for j in range(img.size[1]):
        img.putpixel((i, j), (r[j][i*3], r[j][i*3+1], r[j][i*3+2]))
img.save(path.parent / (path.name + '_secret.png'))

