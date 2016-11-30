import string
import socket
import json
from random import SystemRandom
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


class Comm():
    def __init__(self, me, port):
        self.s = None
        self.con = None
        self.me = me
        self.port = port
        f = open('./' + self.me + '_rsa_public.pem', 'r')
        self.pub = RSA.importKey(f.read())
        f.close()

    def getKey(who):
        return

    def blindSignRSA(self, priv, pub, msg):
        r = SystemRandom().randrange(pub.n >> 10, pub.n)
        hsh = SHA256.new()
        hsh.update(msg.encode('utf-8'))
        msgDigest = hsh.digest()
        blind = pub.blind(msgDigest, r)
        blind_signature = priv.sign(blind, 0)
        return blind_signature, r

    def verifySignature(self, them, blind_signature, msg, r):
        f = open('./' + them + '_rsa_public.pem', 'r')
        theirPub = RSA.importKey(f.read())
        f.close()
        signature = theirPub.unblind(blind_signature, r)
        hsh = SHA256.new()
        hsh.update(msg.encode('utf-8'))
        msgDigest = hsh.digest()
        return theirPub.verify(msgDigest, (signature,))

    def sendHandshake(self, them):
        N = 512
        phrase = ''.join(SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(N))

        myPriv, myPub = None, None
        signature, r = self.blindSignRSA(myPriv, myPub, phrase)
        msg = json.dumps({'sig': signature, 'phrase': phrase, 'r': r})
        self.conn.send(msg)

    def receiveHandshake(self):
        return

    def initiateConn(self):
        return

    def joinConn(self):
        return
