def atbash(text):
    """
    Encrypts/decrypts using the Atbash cipher.
    """
    converted_text = ""
    for char in text:
        if char.isalpha():
            # Shift the character by 25 positions to get the Atbash equivalent
            converted_char = chr(25 - (ord(char.upper()) - ord('A')) + ord('A'))
            # Preserve the original letter case
            if char.islower():
                converted_char = converted_char.lower()
            converted_text += converted_char
        else:
            converted_text += char
    return converted_text


ciphertext = "YV MLG ZUIZRW LU GSVRI UZXVH ULI R ZN DRGS GSVV GL WVOREVI GSVV, HZRGS GSV OLIW."
decrypted_text = atbash(ciphertext)

print("Ciphertext: {}".format(ciphertext))
print("Decrypted text: {}".format(decrypted_text))
