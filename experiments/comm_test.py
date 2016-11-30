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
        self.verified = False
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

    def verifyBlindSignature(self, them, res):
        try:
            res = json.loads(res)
        except ValueError:
            return False
        r = res['r']
        blind_signature = res['sig']
        msg = res['phrase']
        f = open('./' + them + '_rsa_public.pem', 'r')
        theirPub = RSA.importKey(f.read())
        f.close()
        signature = theirPub.unblind(blind_signature, r)
        hsh = SHA256.new()
        hsh.update(msg.encode('utf-8'))
        msgDigest = hsh.digest()
        return theirPub.verify(msgDigest, (signature,))

    def sendMessage(self, them, msg):
        return

    def receiveMessage(self, them, msg):
        return

    def sendHandshake(self, them):
        N = 512
        phrase = ''.join(SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(N))

        myPriv, myPub = None, None
        signature, r = self.blindSignRSA(myPriv, myPub, phrase)
        msg = json.dumps({'sig': signature, 'phrase': phrase, 'r': r})
        self.conn.send(msg)

    def receiveHandshake(self, them):
        res = self.conn.recv(4096)
        if not self.verifySignature(them, res):
            self.closeConn()
        else:
            self.verified = True

    def initiateConn(self, port):
        # create socket and make self visible
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', port))
        s.listen(0)
        self.con, address = s.accept()

    def joinConn(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.conn = self.s

    def closeConn(self):
        self.s.close()
