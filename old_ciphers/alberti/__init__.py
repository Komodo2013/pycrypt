class AlbertiCipher:
    def __init__(self, alphabets):
        self.alphabets = alphabets
        self.alpha = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                      "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    def encrypt(self, message):
        index = 0
        message = message.upper()
        ciphertext = ""

        for char in message:
            if char == " ":
                ciphertext += " "
                continue
            ciphertext += self.alphabets[index % len(self.alphabets)][self.alpha.index(char)]
            index += 1

        return ciphertext

    def decrypt(self, ciphertext):
        index = 0
        ciphertext = ciphertext.upper()
        message = ""

        for char in ciphertext:
            if char == " ":
                message += " "
                continue
            message += self.alpha[self.alphabets[index % len(self.alphabets)].index(char)]
            index += 1

        return message


# Example usage:
inner_alphabet = "FZBVKIXAYMEPLSDHJORGNQCUTW"
outer_alphabet = "GOXBFWTHQILAPZJDESVYCRKUHN"

cipher = AlbertiCipher([inner_alphabet, outer_alphabet])

message = "SJFSG HDKKRKS LQSJO BKPFZVV PFRV GHFZ GJGGP"

# Decryption
decrypted_message = cipher.decrypt(message)
print("Decrypted message:", decrypted_message)
