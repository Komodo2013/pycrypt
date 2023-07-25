from crypto2.ecc.hash import Hasher
from random import randbytes


# Verify cert by calling verify on the certificate hash, private hash, and signature
def make_cert(PKInfo, PKInfo_Hash, valid_start, valid_end, public_key, signer_private, signer_public, signer_name):
    cert = f"Certificate Information:,{PKInfo},Fingerprint:{PKInfo_Hash.hex()},Validity{{" \
           f"Not valid before:{valid_start},Not valid after:{valid_end}}},Public Key:{public_key.hex()}," \
           f"Signer Information:{{Name:{signer_name}, Public Key:{signer_public}}}"
    H = Hasher()
    certihash = H.one_hash(cert)
    private_hash = H.one_hash(signer_private + certihash + randbytes(64))
    public_hash = H.one_hash(signer_public + certihash)
    signature = H.one_hash(private_hash + public_hash)

    cert += f"---BEGIN CERTIFICATE---{certihash.hex()}\n{private_hash.hex()}\n{signature.hex()}---END CERTIFICATE---"
    return cert


def make_keypair(PKInfo_Hash, private_secret):
    H = Hasher()
    private_key = H.one_hash(PKInfo_Hash + private_secret)
    public_key = H.one_hash(private_key + randbytes(64))
    return private_key, public_key


"""
PK Gen					-> Hash(PKInfo), PrK
PrK	+	Hash(PKInfo)		-> Hash(PuK)

PrK	+	Msg (Hash) +	Rand	-> Hash(PrKMsg)
PuK	+	Msg (Hash)		-> Hash(PuKMsg)

PrK_Msg_hash	+	PuK_Msg_hash	-> Hash(signature)

Message + Signature + PrK_Msg_hash		-> Bob
Certificate: PKInfo, Hash, PuK, issuer signature, issuer Prk_msg_hash
"""
def sign(private_key, public_key, message_hash):
    H = Hasher()
    private_hash = H.one_hash(private_key + message_hash + randbytes(64))
    public_hash = H.one_hash(public_key + message_hash)

    signature = H.one_hash(private_hash + public_hash)

    return signature, private_hash


"""
Msg						-> Msg (Hash)

PuK	+	Msg (Hash)		-> Hash(PuKMsg)

PrK_Msg_hash	+	PuK_Msg_hash	-> Hash(signature)
if sign == sign then valid. If message was received twice then invallid
"""
def verify(public_key, message_hash, private_hash, signature):
    H = Hasher()
    public_hash = H.one_hash(public_key + message_hash)
    computed = H.one_hash(private_hash + public_hash)

    return computed == signature