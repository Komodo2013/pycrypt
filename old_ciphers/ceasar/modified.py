def modified_ceasar_decrypt(message, shift):
    message = message.lower()
    alpha   = "abcdefghijklmnopqrstuvwxyz 123456789"
    shifted = alpha[shift:] + alpha[:shift]
    # shifted = "vwxyz123456789abcdefghijk lmnopqrstu"

    cipher = ""

    for char in message:
        cipher += alpha[shifted.index(char)]

    return cipher


# Example usage
message = "EZ9YLPNLFDAABEL9AILMNL7Z1FL17V96LMPLD423FL17V96LMQLYZ1Z9YL749LMLEBK".lower()

"""
for shift in range(36):
    decrypted = modified_ceasar_decrypt(message, -shift)
    print(f"{shift}, {decrypted}")
"""
# index 15 (corresponding with shift +15 seems the most likely to correct
# 15, teod 42 usppqt opx 12 megu gmaol 14 sjhiu gmaol 15 degeod mjo 1 tqz
# however obviously something is incorrect, it seems that a character was displaced
# I think this is correct because the numbers have a weird pattern, 42 = 12+14+15+1

alpha   = "abcdefghijklmnopqrstuvwxyz 123456789"
shifted = alpha[-15:] + alpha[:-15]
print(shifted) # vwxyz 123456789abcdefghijklmnopqrstu
# this seems to be the new alphabet
# since " " would make the most sense to displace, lets now try brute forcing each displacement
new_alpha = "vwxyz123456789abcdefghijklmnopqrstu"

for i in range(len(new_alpha)):
    test_alpha = new_alpha[:i] + " " + new_alpha[i:]
    cipher = ""

    for char in message:
        cipher += alpha[test_alpha.index(char)]

    print(cipher)

# The best result was
# send 42 troops now 12 left flank 14 right flank 15 defend lin 1 spy
