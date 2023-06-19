import base64
from PIL import Image


def generate_bitmap(list_in, filename, is_base64_encoded=False):
    if is_base64_encoded:
        for i in range(len(list_in)):
            list_in[i] = base64.b64decode(list_in[i])

    size = (len(list_in[1]) * 8, len(list_in))
    print(size)

    for i in range(len(list_in)):
        list_in[i] = int.from_bytes(list_in[i], "little")

    img = Image.new( 'RGB', size=size)  # Create a new image
    pixels = img.load()  # Create the pixel map

    for i in range(size[1]):  # For every row:
        for j in range(size[0]):  # For each pixel/bit
            if list_in[i] & 0x1:  # read the least significant bit (we reversed the direction of the bits above)
                pixels[j, i] = (255, 255, 255)  # Set the colour accordingly
            list_in[i] >>= 1

    img.show()
    img.save(filename, 'png')
