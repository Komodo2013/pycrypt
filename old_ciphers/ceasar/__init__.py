def caesar_simple_shift(text, key, encrypt=True):
    """
    converts the given text by a simple shift
    """
    converted_text = ""
    for char in text:
        if char.isalpha():
            if encrypt:
                # Shift the character by the key positions to get the Caesar equivalent
                converted_char = chr((ord(char.upper()) - ord('A') + key) % 26 + ord('A'))
            else:
                # Shift the character by the key positions to get the Caesar equivalent
                converted_char = chr((ord(char.upper()) - ord('A') - key) % 26 + ord('A'))

            # Preserve the original letter case
            if char.islower():
                converted_char = converted_char.lower()
            converted_text += converted_char
        else:
            converted_text += char
    return converted_text


def caesar_passphrase(text, passphrase, encrypt=True):
    """
    Converts the given plaintext using the Caesar cipher with a passphrase.
    """
    # Convert the passphrase to a key
    key = sum([ord(char) for char in passphrase])

    # Encrypt the text using the simple shift Caesar cipher with the key
    return caesar_simple_shift(text, key, encrypt=encrypt)


def letter_distance(a, b):
    """Get the distance between two letters in the English alphabet."""
    return (ord(b) - ord(a)) % 26


# Example usage
ciphertext = "KYV UZWWVIVETV SVKNVVE R IVGLSCZT REU VDGZIV ZJ KYV CFPRCKP FW FEV'J RIDP"
# FEV'J is interesting due to the apostrophe, presenting a weakness
# most words with an apostrophe will be either possession or contraction, so I should expect either an 's' or 't'
decrypted_text_1 = caesar_simple_shift(ciphertext, letter_distance("S", "J"), encrypt=False)
decrypted_text_2 = caesar_simple_shift(ciphertext, letter_distance("T", "J"), encrypt=False)

print("Ciphertext: {}".format(ciphertext))
print("Attempt 1: {}".format(decrypted_text_1))
# Outputs: THE DIFFERENCE BETWEEN A REPUBLIC AND EMPIRE IS THE LOYALTY OF ONE'S ARMY
print("Attempt 1: {}".format(decrypted_text_2))
# Outputs: UIF EJGGFSFODF CFUXFFO B SFQVCMJD BOE FNQJSF JT UIF MPZBMUZ PG POF'T BSNZ



