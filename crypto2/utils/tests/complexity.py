import math
import zlib
import lzma
import bz2
from collections import defaultdict


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

def linear_complexity_test(binary_sequence):
    sequence_length = len(binary_sequence)//512
    L = 0  # Linear complexity
    m = -1  # Position of the last discrepancy
    n = 0  # Length of the linear feedback shift register (LFSR)
    C = [0] * sequence_length  # Coefficients of the LFSR

    u = [int(bit) for bit in binary_sequence]  # Convert binary sequence to list of integers

    for i in range(sequence_length):
        discrepancy = u[i]
        for j in range(1, n + 1):
            discrepancy ^= C[j] * u[i - j]

        if discrepancy == 1:
            temp = C.copy()
            t = i - m

            for j in range(t):
                C[i - j] ^= C[n - t - j]

            if n <= i / 2:
                n = i + 1 - n
                m = i
                C = temp

    L = n
    return L

def serial_test(binary_sequence, lag_length):
    sequence_length = len(binary_sequence)
    subsequence_count = sequence_length - lag_length + 1

    # Calculate the observed and expected frequencies of bit patterns
    observed_frequencies = defaultdict(int)
    expected_frequencies = 2**(lag_length - 1)

    for i in range(subsequence_count):
        subsequence = binary_sequence[i:i+lag_length]
        observed_frequencies[subsequence] += 1

    # Calculate the chi-square statistic
    chi_square = 0.0
    for freq in observed_frequencies.values():
        chi_square += ((freq - expected_frequencies)**2) / expected_frequencies

    # Calculate the degrees of freedom
    degrees_of_freedom = 2**(lag_length - 1) - 1

    # Calculate the p-value
    p_value = 1.0 - math.erf(chi_square / math.sqrt(2 * degrees_of_freedom))

    return chi_square, p_value

def approximate_entropy_test(binary_sequence, m):
    sequence_length = len(binary_sequence)
    patterns_m = {}
    patterns_m_plus_1 = {}

    for i in range(sequence_length - m + 1):
        pattern = binary_sequence[i:i+m]
        if pattern in patterns_m:
            patterns_m[pattern] += 1
        else:
            patterns_m[pattern] = 1

        pattern = binary_sequence[i:i+m+1]
        if pattern in patterns_m_plus_1:
            patterns_m_plus_1[pattern] += 1
        else:
            patterns_m_plus_1[pattern] = 1

    count_m = len(patterns_m)
    count_m_plus_1 = len(patterns_m_plus_1)

    sum_m = sum(patterns_m.values())
    sum_m_plus_1 = sum(patterns_m_plus_1.values())

    apen_m = 0
    for count in patterns_m.values():
        apen_m += count * (math.log(count) - math.log(sum_m))

    apen_m_plus_1 = 0
    for count in patterns_m_plus_1.values():
        apen_m_plus_1 += count * (math.log(count) - math.log(sum_m_plus_1))

    apen_m /= (sequence_length - m + 1)
    apen_m_plus_1 /= (sequence_length - m)

    approximate_entropy = apen_m - apen_m_plus_1

    return approximate_entropy

def cumulative_sums_test(binary_sequence):
    n = len(binary_sequence)
    s = [0] * (n + 1)  # Initialize cumulative sums array

    # Calculate cumulative sums
    for i in range(1, n + 1):
        s[i] = s[i - 1] + (1 if binary_sequence[i - 1] == 1 else -1)

    max_sum = max(abs(x) for x in s)  # Maximum absolute cumulative sum

    # Calculate the test statistic
    test_statistic = float(max_sum) / n

    return test_statistic


