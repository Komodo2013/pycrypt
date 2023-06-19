import math


def frequency_test_monobit(bits_list):
    # Count the number of 1s in the bit sequence
    num_ones = sum(bits_list)

    # Calculate the proportion of 1s
    return num_ones / len(bits_list)


def frequency_test_block(bits_list, block_length, threshold=.1):
    # Calculate the number of blocks
    num_blocks = len(bits_list) // block_length

    count_pass = 0
    for i in range(num_blocks):
        # Extract the current block
        block = bits_list[i * block_length : (i + 1) * block_length]
        proportion = sum(block) / block_length

        if threshold >= abs(proportion - .5):
            count_pass += 1

    return count_pass/num_blocks

def runs_test(bits_list):
    # Calculate the total number of bits
    num_bits = len(bits_list)

    # Initialize the counts
    count_runs = 1
    count_mismatches = 0
    longest = 0
    run = 0

    # Iterate over the bits
    for i in range(1, num_bits):
        # Check if the current bit differs from the previous bit
        if bits_list[i] != bits_list[i - 1]:
            count_runs += 1
            if longest < run:
                longest = run
            run = 0

        # Check if the current bit is a mismatch with the previous bit
        if bits_list[i] == bits_list[i - 1]:
            count_mismatches += 1
            run += 1

    # Calculate the expected number of runs and mismatches
    expected_runs = (2 * num_bits - 1) / 3
    expected_mismatches = 2 * ((num_bits / 2) - 1) / 3
    expected_longest_run_min = (1 / 2) * (math.log2(num_bits)) - 2 * math.sqrt((2 / 3) * num_bits)
    expected_longest_run_max = (1 / 2) * (math.log2(num_bits)) + 2 * math.sqrt((2 / 3) * num_bits)

    return ((count_runs - expected_runs)/expected_runs,
            (count_mismatches - expected_mismatches)/expected_mismatches,
            (expected_longest_run_min <= longest <= expected_longest_run_max, longest, expected_longest_run_min, expected_longest_run_max))
