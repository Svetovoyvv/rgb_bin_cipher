import sys
import pathlib
from PIL import Image

if len(sys.argv) < 2:
    print('usage: python extract.py <path_to_file>')
    sys.exit(1)

path = pathlib.Path(sys.argv[1])
if not path.exists() or path.is_dir():
    print('invalid path')
    sys.exit(1)

img = Image.open(path)
r = ''
for y in range(img.size[1]):
    for x in range(img.size[0]):
        t = img.getpixel((x, y))
        r += f'{t[0]:08b}{t[1]:08b}{t[2]:08b}'
    r += '\n'

with open(path.parent / (path.name + '.txt'), 'w') as f:
    f.write(r)
