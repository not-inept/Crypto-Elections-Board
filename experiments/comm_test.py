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
        f = open('../common/' + self.me + '_rsa_public.pem', 'r')
        self.pub = RSA.importKey(f.read())
        f.close()
        f = open('./' + self.me + '_rsa_private.pem', 'r')
        self.priv = RSA.importKey(f.read())
        f.close()

    def getKey(self, them):
        f = open('../common/' + them + '_rsa_public.pem', 'r')
        key = RSA.importKey(f.read())
        f.close()
        return key

    def blindSignRSA(self, msg):
        r = SystemRandom().randrange(self.pub.n >> 10, self.pub.n)
        hsh = SHA256.new()
        hsh.update(msg.encode('utf-8'))
        msgDigest = hsh.digest()
        blind = self.pub.blind(msgDigest, r)
        blind_signature = self.priv.sign(blind, 0)
        return blind_signature, r

    def verifyBlindSignature(self, them, res):
        try:
            res = json.loads(res)
        except ValueError:
            return False
        r = res['r']
        blind_signature = res['sig']
        msg = res['phrase']
        theirPub = self.getKey(them)
        signature = theirPub.unblind(blind_signature, r)
        hsh = SHA256.new()
        hsh.update(msg.encode('utf-8'))
        msgDigest = hsh.digest()
        return theirPub.verify(msgDigest, (signature,))

    def sendMessage(self, msg):
        blind, r = self.bindSignRSA(msg)
        msg = {'sig': blind, 'r': r, 'phrase': msg}
        self.s.send(msg)

    def receiveMessage(self, them):
        res = self.s.recv(8192)
        if self.verifyBlindSignature(them, res):
            return res
        else:
            self.quit()

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

    def quit(self):
        self.s.close()
        self.s = None
        self.con = None
        print('I should quit')
        quit()
