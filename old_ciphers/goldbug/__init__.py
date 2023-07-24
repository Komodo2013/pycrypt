import string

pairs = {
    'A': '5', 'B': '2', 'C': '-', 'D': '†', 'E': '8', 'F': '1', 'G': '3', 'H': '4', 'I': '6', 'J': ',', 'K': '7',
    'L': '0', 'M': '9', 'N': '*', 'O': '‡', 'P': '.', 'Q': '$', 'R': '(', 'S': ")", 'T': ';', 'U': '?', 'V': '¶',
    'W': "]", 'X': '¢', 'Y': ':', 'Z': '[',
    '5': 'A', '2': 'B', '-': 'C', '†': 'D', '8': 'E', '1': 'F', '3': 'G', '4': 'H', '6': 'I', ',': 'J', '7': 'K',
    '0': 'L', '9': 'M', '*': 'N', '‡': 'O', '.': 'P', '$': 'Q', '(': 'R', ")": 'S', ';': 'T', '?': 'U', '¶': 'V',
    "]": 'W', '¢': 'X', ':': 'Y', '[': 'Z',
    " ": ""
}

def goldbug_cipher(text):
    result = ""
    t = text.upper()

    for c in t:
        result += pairs[c]

    return result

# Example usage
plaintext = "The quick brown fox jumps over the lazy dog."
ciphertext = goldbug_cipher(plaintext)
print("Ciphertext:", ciphertext)

decoded_text = goldbug_cipher("528806*81(‡9;48;(88;4(‡?34;48)4‡;161;:188;‡?;")
print("Decoded text:", decoded_text)
