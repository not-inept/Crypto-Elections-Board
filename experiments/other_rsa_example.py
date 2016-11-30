from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from random import SystemRandom

# Signing authority (SA) key
priv = RSA.generate(4096)
pub = priv.publickey()

## Protocol: Blind signature ##

# must be guaranteed to be chosen uniformly at random
r = SystemRandom().randrange(pub.n >> 10, pub.n)
msg = "my message" * 50 # large message (larger than the modulus)

# hash message so that messages of arbitrary length can be signed
hsh = SHA256.new()
hsh.update(msg.encode('utf-8'))
msgDigest = hsh.digest()

# user computes
msg_blinded = pub.blind(msgDigest, r)

# SA computes
msg_blinded_signature = priv.sign(msg_blinded, 0)
print(msg_blinded_signature)
# user computes
msg_signature = pub.unblind(msg_blinded_signature[0], r)


# Someone verifies
hsh = SHA256.new()
hsh.update(msg.encode('utf-8'))

msgDigest = hsh.digest()
print("Message is authentic: " + str(pub.verify(msgDigest, (msg_signature,))))