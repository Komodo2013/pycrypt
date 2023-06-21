def generate_key_matrix(key):
    key = key.upper().replace("J", "I") # Convert to uppercase and replace 'J' with 'I'
    key = "".join(dict.fromkeys(key)) # Remove duplicate characters while preserving order

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_matrix = list(key)
    for char in alphabet:
        if char not in key_matrix:
            key_matrix.append(char)

    return key_matrix

def generate_bigrams(message):
    message = message.upper().replace("J", "I") # Convert to uppercase and replace 'J' with 'I'
    message = "".join(filter(str.isalpha, message)) # Remove non-alphabetic characters

    bigrams = []
    i = 0

    while i < len(message):
        if i == len(message) - 1 or message[i] == message[i + 1]:
            bigrams.append(message[i] + "X")
            i += 1
        else:
            bigrams.append(message[i] + message[i + 1])
            i += 2

    return bigrams

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i*5 + j] == char:
                return i, j

def encrypt(plain_text, key):
    key_matrix = generate_key_matrix(key)
    bigrams = generate_bigrams(plain_text)

    cipher_text = ""

    for bigram in bigrams:
        char1, char2 = bigram[0], bigram[1]
        row1, col1 = find_position(key_matrix, char1)
        row2, col2 = find_position(key_matrix, char2)

        if row1 == row2: # Same row
            col1 = (col1 + 1) % 5
            col2 = (col2 + 1) % 5
        elif col1 == col2: # Same column
            row1 = (row1 + 1) % 5
            row2 = (row2 + 1) % 5
        else: # Different row and column
            col1, col2 = col2, col1

        cipher_text += key_matrix[row1 * 5 + col1] + key_matrix[row2 * 5 + col2]

    return cipher_text

def decrypt(cipher_text, key):
    key_matrix = generate_key_matrix(key)
    bigrams = generate_bigrams(cipher_text)

    plain_text = ""

    for bigram in bigrams:
        char1, char2 = bigram[0], bigram[1]
        row1, col1 = find_position(key_matrix, char1)
        row2, col2 = find_position(key_matrix, char2)

        if row1 == row2: # Same row
            col1 = (col1 - 1) % 5
            col2 = (col2 - 1) % 5
        elif col1 == col2: # Same column
            row1 = (row1 - 1) % 5
            row2 = (row2 - 1) % 5
        else: # Different row and column
            col1, col2 = col2, col1

    plain_text += key_matrix[row1][col1] + key_matrix[row2][col2]

    return plain_text

# Example usage:
key = "KEYWORD"
message = "anything is here because I want it to be"

encrypted_message = encrypt(message, key)
print("Encrypted message:", encrypted_message)