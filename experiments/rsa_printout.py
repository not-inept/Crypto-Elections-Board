from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from random import SystemRandom

priv = RSA.generate(4096)
pub = priv.publickey()
print(priv.exportKey())
print(pub.exportKey())