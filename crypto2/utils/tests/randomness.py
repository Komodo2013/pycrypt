import frequency_tests
import bitmaps
import util
import matrix_tests
import complexity

def center_print(text, width=100):
    padding = " " * ((width - len(text)) // 2)
    print(padding + text + padding)

def generate_stats(dir_to_bitmap):
    _3d_data, _2d_data, _binary_sequence = util.read_bitmap(dir_to_bitmap)

    print("*" * 100)
    center_print("Statistical Analysis of Bitmap")
    center_print("Located at " + dir_to_bitmap)
    print("\n")
    center_print("Frequency Tests")
    print(f"\tFrequency of 1s\n\t\t\t\033[35m{frequency_tests.frequency_test_monobit(_2d_data):2.3%}\033[0m")
    threshold = .1
    print(f"\tPercentage of 32-bit blocks with \033[32m< {threshold}\033[0m deviance from 50%\n"
          f"\t\t\t\033[35m{frequency_tests.frequency_test_block(_2d_data, 32):2.3%}\033[0m")
    print(f"\tPercentage of 64-bit blocks with \033[32m< {threshold}\033[0m deviance from 50%\n"
          f"\t\t\t\033[35m{frequency_tests.frequency_test_block(_2d_data, 64):2.3%}\033[0m")
    results = frequency_tests.runs_test(_2d_data)
    print(f"\tPercent difference of actual vs expected runs: \n\t\t\t\033[35m{results[0]:2.3%}\033[0m")
    print(f"\tPercent difference of actual vs expected mismatches: \n\t\t\t\033[35m{results[1]:2.3%}\033[0m")
    print(f"\n\tLongest run: \033[35m{'PASSED' if results[2][0] else 'FAILED'}\033[0m\n"
          f"\t\t\tMin Expected: \033[35m{results[2][2]}\033[0m\n"
          f"\t\t\tMax Expected: \033[35m{results[2][3]}\033[0m\n"
          f"\t\t\tActual: \033[35m{results[2][1]}\033[0m\n")

    center_print("Complexity Tests")
    """ # These tests take a while to complete
    results = complexity.maurer_universal_test(_binary_sequence, 16)
    print(f"\n\tMaurer Universal Statistics Test, size \033[32m16\033[0m"
          f"\t\tzlib: \033[35m{results[0]:3.5f}\033[0m"
          f"\t\tlzma: \033[35m{results[1]:3.5f}\033[0m"
          f"\t\tbz2: \033[35m{results[2]:3.5f}\033[0m")
    results = complexity.maurer_universal_test(bytearray(_binary_sequence), 32)
    print(f"\n\tMaurer Universal Statistics Test, size \033[32m32\033[0m"
          f"\t\tzlib: \033[35m{results[0]:3.5f}\033[0m"
          f"\t\tlzma: \033[35m{results[1]:3.5f}\033[0m"
          f"\t\tbz2: \033[35m{results[2]:3.5f}\033[0m")
    results = complexity.maurer_universal_test(bytearray(_binary_sequence), 64)
    print(f"\n\tMaurer Universal Statistics Test, size \033[32m64\033[0m"
          f"\t\tzlib: \033[35m{results[0]:3.5f}\033[0m"
          f"\t\tlzma: \033[35m{results[1]:3.5f}\033[0m"
          f"\t\tbz2: \033[35m{results[2]:3.5f}\033[0m")
    results = complexity.maurer_universal_test(bytearray(_binary_sequence), 128)
    print(f"\n\tMaurer Universal Statistics Test, size \033[32m128\033[0m"
          f"\t\tzlib: \033[35m{results[0]}\033[0m"
          f"\t\tlzma: \033[35m{results[1]}\033[0m"
          f"\t\tbz2: \033[35m{results[2]}\033[0m\n")
    print(f"\tLinear Complexity\n\t\t\t\033[35m{complexity.linear_complexity_test(_binary_sequence)}\033[0m")
    """
    true_rand = "0010001010100010010111001011000110011100001110101110010010100011101100101111010110111111010001111001011000101010100011010100011101011100000110010110111011111111010111001001100011110100010000100111011010000011111111001001000100000010101101111011011011100011110011101110101010000111111000000011000001111011110001010100010010001110110101011111101100111111011011010000100001111100010111110011011101010010010111110111111000011101000101010101100101000000100001100010101110010001010100000011100001101101001101111110001011110111010001101100010101100100001010010011111110001110000000101100111100101011111011010101001111001110010110111011010010000101111100100111000010100111001101011001000101011010101110100001000001000111110001011001010010011001100011111110101001011010001001001111000001000110010100011111101101111100100010111010000111100110010100010111111111111100110110011011100110000010110100110101011101011111010001001001100101001011110100011011000100011101010100010101101010110111101100001001000011011001010100001000000101000001000101011110110101010110010100010010001111101101101101000001011110101100111100100000011111111011011101101100111100001000100011000010011100001010000000011101101010111100000110000010011100110001111010000011110110000100111101011000011110011100100010000000010100011001111011111101111010110111110111000000110111001011011110110110110100011000100000101010101111101010001010011011100110001101111010110110000011000110101001111100101110100010101100110011000100010111101000011100001000000110011011000110000001111000011000100001101111101111001011101011001010010111000010010111110001000101100011101010000001111000001000011001000010010001010101010100100101010100111011001001101010001110111001101001001110111100011000100011111100011011010000011000001000001011110010101011110111001111011010100000111011101011000011101000010110001101110010100101100000001101011001100010000001011011110111000110110101101001011100110100000111110111100101110000100011011001011110110111011010101010000100100001101101111110011111100010011100001100110101111000001000111010011001111011010101011110001000000010001100110001001101111001011011001011011010000001000000011010101011111110100011000101011111011000011111011000000100000110100110011000000101110110101110001010001011011110001000011101100010010110111101111110011101000100101100001100010110010100100100000100000111101101000011110000011110010111000011011001010110011010100010001001010010100100101110110010101010000100100111011011010000100110001100101110010000010010010010111001000011001100000001100000000011110001001100000010101101000100110100010000111111101011101101100101001110100010101011111000100101100001010000011100100011011001110001000101111110001101110001101111010011000111100100001011101110101010101001111100110001011101010111110110001101110101111011100000001010010111101001000001000010111100111011011000111101010111110011010001110101100101100100010000011011110011000010101001101010011100000100111110110110101110111100100000101101000000110111011101110100101011100101011101101001100001111011000001001011001000101000010001010110011000100100110110111110001101000100000010101111111011110101010011101010111101000001111101001010110010010001101010111001011010111010010000111001010101001001110111011111101000000111010001000100111110011011110100101101010010100010101011001000111010000111111011001111000100100100000111111010011010000011010001011010010001100101001110001101000101001000100011001001011010011110100011001111010111101111000000011111011100010011111111100001100001101001011110000100001110110101111010010110111110011110100101011001011100100000001101010010001010111001010100110110110000100110000010000010111100011001111111110011011101100011000001101000111100101000110100010010011110101100100110100010101001010000110111101001100101011001101011100101011000010110101111111010000000000010110011000111101000010111101100100111001001111000011001000001011101010001010100010101111111001100010101000101011111011110100111101111110000110000001111001001000000100001111011010101110111101010100001100000101011010001000110100101001000110000000101001000001110011001100001"
    print(f"\tSerial Test (chi-squares, p-val)\n\t\t\t\033[35m{complexity.serial_test(_binary_sequence, 8)}\033[0m")
    print(f"\tApproximate Entropy Test\n\t\t\t\033[35m{complexity.approximate_entropy_test(_binary_sequence, 8)}\033[0m")
    print(f"\tCumulative Sums Test\n\t\t\t\033[35m{complexity.cumulative_sums_test(_binary_sequence)}\033[0m")

    #print(f"\tCumulative Sums Test\n\t\t\t\033[35m{complexity.cumulative_sums_test(true_rand)}\033[0m")




    center_print("Matrix Tests")
    print(f"\tBinary Matrix Rank Test\n\t\t\t\033[35m{matrix_tests.binary_matrix_rank_test(_3d_data)}\033[0m\n")
    matrix_tests.spectral_test(_3d_data)



generate_stats("C:\\Users\\jacobmichaellarsen\\PycharmProjects\\pycrypt\\crypto2\\ecc\\bittest_6.bmp")