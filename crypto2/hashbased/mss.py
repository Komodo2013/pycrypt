from crypto2.ecc.hash import Hasher

class MerkleSignatureScheme:
    def __init__(self, hash_function=None):
        if not hash_function:
            self.__hasher__ = Hasher()
            self.hash_function = self.__hasher__.one_hash
        else:
            self.hash_function = hash_function

    def create_signature(self, message):
        hash_tree = self.build_hash_tree(message)
        signature = hash_tree[-1]
        return signature

    def verify_signature(self, message, signature):
        hash_tree = self.build_hash_tree(message)
        if hash_tree[-1] == signature:
            return True
        return False

    def build_hash_tree(self, message):
        hash_values = []
        for chunk in message.split(b'\0'):
            hash_values.append(self.hash_function(chunk))

        while len(hash_values) > 1:
            new_hash_values = []
            for i in range(0, len(hash_values), 2):
                combined_hash = self.hash_function(hash_values[i] + hash_values[i + 1])
                new_hash_values.append(combined_hash)
            hash_values = new_hash_values

        return hash_values

def main():
    message = b'This is a message.'
    signature = MerkleSignatureScheme().create_signature(message)
    print(signature.hex())

    message = b'This is a1 message.'
    signature = MerkleSignatureScheme().create_signature(message)
    print(signature.hex())

    assert MerkleSignatureScheme().verify_signature(message, signature)
    print('valid')

if __name__ == '__main__':
    main()
