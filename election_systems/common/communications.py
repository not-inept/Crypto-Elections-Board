import socket
import json
from random import SystemRandom
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


class Comm():
    def __init__(self, me, port):
        self.s = None
        self.conn = None
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
            res = json.loads(res.decode())
        except ValueError:
            return False
        r = int(res['r'])
        blind_signature = res['sig'][0]
        msg = res['phrase']
        theirPub = self.getKey(them)
        signature = theirPub.unblind(blind_signature, r)
        hsh = SHA256.new()
        hsh.update(msg.encode('utf-8'))
        msgDigest = hsh.digest()
        return theirPub.verify(msgDigest, (signature,))

    def sendMessage(self, msg):
        blind, r = self.blindSignRSA(msg)
        msg = {'sig': blind, 'r': r, 'phrase': msg}
        self.conn.send(json.dumps(msg).encode('utf-8'))

    def receiveMessage(self, them):
        res = self.conn.recv(8192)
        if self.verifyBlindSignature(them, res):
            return json.loads(res.decode())['phrase']
        else:
            self.quit()

    def initiateConn(self):
        # create socket and make self visible
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('localhost', self.port))
        self.s.listen(1)
        print('initiated')
        self.conn, address = self.s.accept()

    def joinConn(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('attempting to join')
        self.s.connect((host, port))
        self.conn = self.s

    def closeConn(self):
        self.s.close()
        self.s = None
        self.conn = None

    def quit(self):
        self.closeConn()
        print('I should quit')
        quit()
