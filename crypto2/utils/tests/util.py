from PIL import Image

def read_bitmap(dir):

    with open(dir, "rb") as file:
        img = Image.open(file)
        img = img.convert('1')

        w, h = img.size
        bit_array = [[0] * w for _ in range(h)]

        for y in range(h):
            for x in range(w):
                bit_array[y][x] = 1 if img.getpixel((x, y)) else 0

    bits_list = [bit for row in bit_array for bit in row]

    binary_sequence = bytes(bits_list)

    return bit_array, bits_list, binary_sequence
