import frequency_tests
import bitmaps
import util

def center_print(text, width=100):
    padding = " " * ((width - len(text)) // 2)
    print(padding + text + padding)

def generate_stats(dir_to_bitmap):
    _3d_data, _2d_data = util.read_bitmap(dir_to_bitmap)

    print("*" * 100)
    center_print("Statistical Analysis of Bitmap")
    center_print("Located at " + dir_to_bitmap)
    print("\n")
    center_print("Frequency Tests")
    print(f"\tFrequency of 1s\n\t\t\t\033[35m{frequency_tests.frequency_test_monobit(_2d_data):2.3%}\033[0m")
    threshold = .1
    print(f"\tPercentage of blocks with \033[32m< {threshold}\033[0m deviance from 50%\n"
          f"\t\t\t\033[35m{frequency_tests.frequency_test_block(_2d_data, 32):2.3%}\033[0m")
    print(f"\tPercentage of blocks with \033[32m< {threshold}\033[0m deviance from 50%\n"
          f"\t\t\t\033[35m{frequency_tests.frequency_test_block(_2d_data, 64):2.3%}\033[0m")
    results = frequency_tests.runs_test(_2d_data)
    print(f"\tPercent difference of actual vs expected runs: \n\t\t\t\033[35m{results[0]:2.3%}\033[0m")
    print(f"\tPercent difference of actual vs expected mismatches: \n\t\t\t\033[35m{results[1]:2.3%}\033[0m")
    print(f"\n\tLongest run: \033[35m{'PASSED' if results[2][0] else 'FAILED'}\033[0m\n"
          f"\t\t\tMin Expected: \033[35m{results[2][2]}\033[0m\n"
          f"\t\t\tMax Expected: \033[35m{results[2][3]}\033[0m\n"
          f"\t\t\tActual: \033[35m{results[2][1]}\033[0m\n")

generate_stats("C:\\Users\\jacobmichaellarsen\\PycharmProjects\\pycrypt\\crypto2\\ecc\\bittest_6.bmp")