import math
import zlib
import lzma
import bz2

def maurer_universal_test(binary_sequence, block_length):
    sequence_length = len(binary_sequence)
    num_blocks = math.ceil(sequence_length / block_length)
    ncd_values = []

    # Compress each block and calculate the normalized compression distance (NCD)
    for i in range(num_blocks):
        start = i * block_length
        end = min(start + block_length, sequence_length)
        block = binary_sequence[start:end]

        # Compress the block using different compression algorithms
        compressed_size_zlib = len(zlib.compress(block))
        compressed_size_lzma = len(lzma.compress(block))
        compressed_size_bz2 = len(bz2.compress(block))

        # Calculate the NCD for each compression algorithm
        ncd_zlib = (compressed_size_zlib + len(block)) / max(compressed_size_zlib, len(block))
        ncd_lzma = (compressed_size_lzma + len(block)) / max(compressed_size_lzma, len(block))
        ncd_bz2 = (compressed_size_bz2 + len(block)) / max(compressed_size_bz2, len(block))

        # Store the NCD values for analysis
        ncd_values.append(ncd_zlib)
        ncd_values.append(ncd_lzma)
        ncd_values.append(ncd_bz2)

    return ncd_values
