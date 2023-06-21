import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import LinAlgError

def binary_matrix_rank_test(binary_matrix):
    try:
        return np.linalg.matrix_rank(binary_matrix)
    except LinAlgError:
        # Handle cases where matrix rank cannot be computed (e.g., non-square matrix)
        return None

def spectral_test(binary_matrix):
    # Perform 2D Discrete Fourier Transform
    dft = np.fft.fft2(binary_matrix)

    # Shift the zero-frequency component to the center
    dft_shift = np.fft.fftshift(dft)

    # Compute the power spectrum
    power_spectrum = np.abs(dft_shift) ** 2

    # Plot the power spectrum
    plt.imshow(np.log10(power_spectrum + 1), cmap='hot', origin='lower')
    plt.colorbar()
    plt.title('Power Spectrum')
    plt.xlabel('Frequency (kx)')
    plt.ylabel('Frequency (ky)')
    plt.show()
    return



