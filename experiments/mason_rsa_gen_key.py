from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from random import SystemRandom
import json

# Signing authority (SA) key
def generateKeys(names):
    for e in names:
        priv = RSA.generate(4096)
        pub = priv.publickey()
        m = priv.exportKey()
        f = open('./' + e + '_rsa_private.pem', 'w+')
        f.write(m)
        f.close()
        m = priv.publickey().exportKey()
        f = open('./' + e + '_rsa_public.pem', 'w+')
        f.write(m)
        f.close()


generateKeys(['bb','eb','ca'])