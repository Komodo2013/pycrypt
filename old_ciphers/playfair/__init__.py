import re

def prepare_message(message):
    message = re.sub(r"[^a-zA-Z]", "", message)  # Remove non-alphabetic characters
    message = re.sub(r"J", "I", message)  # Replace 'J' with 'I'
    message = re.sub(r"(?<=\w)([A-Z])", r" \1", message)  # Insert space between consecutive letters
    message = re.sub(r"(?<=\w)([A-Z])", r" \1", message)  # Insert space between consecutive letters (again)
    message = message.upper()  # Convert to uppercase
    return message

def generate_key_square(key):
    key = re.sub(r"[^a-zA-Z]", "", key)  # Remove non-alphabetic characters
    key = re.sub(r"J", "I", key)  # Replace 'J' with 'I'
    key = key.upper()  # Convert to uppercase
    key = re.sub(r"(?<=\w)([A-Z])", r" \1", key)  # Insert space between consecutive letters
    key = key.replace(" ", "")  # Remove spaces

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_square = list(key)

    for letter in alphabet:
        if letter not in key_square:
            key_square.append(letter)

    return key_square

def generate_bigram_pairs(message):
    pairs = re.findall(r"(?i)([A-Z])([A-Z])", message)
    return [pair for pair in pairs if pair[0] != pair[1]]

def encrypt(message, key):
    message = prepare_message(message)
    key_square = generate_key_square(key)
    bigram_pairs = generate_bigram_pairs(message)
    encrypted_message = ""

    for pair in bigram_pairs:
        row1, col1 = divmod(key_square.index(pair[0]), 5)
        row2, col2 = divmod(key_square.index(pair[1]), 5)

        if row1 == row2:
            encrypted_message += key_square[row1 * 5 + (col1 + 1) % 5]
            encrypted_message += key_square[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            encrypted_message += key_square[((row1 + 1) % 5) * 5 + col1]
            encrypted_message += key_square[((row2 + 1) % 5) * 5 + col2]
        else:
            encrypted_message += key_square[row1 * 5 + col2]
            encrypted_message += key_square[row2 * 5 + col1]

    return encrypted_message

def decrypt(message, key):
    key_square = generate_key_square(key)
    bigram_pairs = generate_bigram_pairs(message)
    decrypted_message = ""

    for pair in bigram_pairs:
        row1, col1 = divmod(key_square.index(pair[0]), 5)
        row2, col2 = divmod(key_square.index(pair[1]), 5)

        if row1 == row2:
            decrypted_message += key_square[row1 * 5 + (col1 - 1) % 5]
            decrypted_message += key_square[row2 * 5 + (col2 - 1) % 5]
        elif col1 == col2:
            decrypted_message += key_square[((row1 - 1) % 5) * 5 + col1]
            decrypted_message += key_square[((row2 - 1) % 5) * 5 + col2]
        else:
            decrypted_message += key_square[row1 * 5 + col2]
            decrypted_message += key_square[row2 * 5 + col1]

    return decrypted_message

# Example usage:
key = "JUMBLED"
message = "Meet me at the corner of fifth and state at four pm"

encrypted_message = encrypt(message, key)
print("Encrypted message:", encrypted_message)

decrypted_message = decrypt(encrypted_message, key)
print("Decrypted message:", decrypted_message)
