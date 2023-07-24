import hashlib

# Function to generate a private key using the given seed and index
def generatePrivateKey(seed, index):
    return hashlib.sha256(seed.encode() + str(index).encode()).hexdigest()

# Function to generate an array of private keys
def generatePrivateKeys(seed, k):
    privateKeys = []
    for i in range(1, k+1):
        privateKey = generatePrivateKey(seed, i)
        privateKeys.append(privateKey)
    return privateKeys

# Function to compute the hash of a node by concatenating and hashing its children
def computeNodeHash(left, right):
    return hashlib.sha256(left.encode() + right.encode()).hexdigest()

# Function to construct the Merkle tree and return the root
def constructMerkleTree(privateKeys):
    merkleTree = privateKeys[:]
    n = len(merkleTree)

    while n > 1:
        newLevel = []
        i = 0

        while i < n:
            leftNode = merkleTree[i]
            rightNode = merkleTree[i + 1] if i + 1 < n else leftNode

            newNode = computeNodeHash(leftNode, rightNode)
            newLevel.append(newNode)

            i += 2

        merkleTree = newLevel
        n = len(merkleTree)

    root = merkleTree[0]
    return root

# Function to sign a message using a private key and Merkle tree
def sign(message, privateKey, merkleTree):
    messageDigest = hashlib.sha256(message.encode()).hexdigest()
    index = int(messageDigest, 16) % len(merkleTree)
    signature = privateKey[index]
    return signature

# Function to verify the signature using the message, signature, and public key (Merkle root)
def verify(message, signature, publicKey):
    messageDigest = hashlib.sha256(message.encode()).hexdigest()
    index = int(messageDigest, 16) % len(publicKey)
    computedPublicKey = publicKey[index]
    return computedPublicKey == signature

# Main function for demonstration
if __name__ == "__main__":
    seed = "ThisIsASecretSeed"
    k = 128  # Number of private keys (adjust as needed)

    privateKeys = generatePrivateKeys(seed, k)
    merkleRoot = constructMerkleTree(privateKeys)

    message = "Hello, world!"
    signature = sign(message, privateKeys, merkleRoot)
    print("Signature:", signature)

    isValid = verify(message, signature, merkleRoot)
    print("Signature Verification:", isValid)
