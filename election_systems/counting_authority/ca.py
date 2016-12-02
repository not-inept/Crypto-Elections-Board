import json
import os
import sys
import inspect
import tkinter as tk
from phe import paillier
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from common.communications import Comm


class CountingAuthority():
    def __init__(self):
        self.bb_location = ('localhost', 6969)
        self.eb_location = ('localhost', 5858)
        self.comm = Comm('ca', 1337)
        self.votes = None
        self.ebpPub = None

    def sendVotes(self):
        return

    def tallyVotes(self):
        return

    def receiveVotes(self):
        self.comm.initiateConn()
        res = self.comm.receiveMessage('bb')
        f = open('../common/comm.line', 'r')
        self.votes = json.loads(f.read())
        f.close()

        self.comm.closeConn()
        print(self.votes)
        self.comm.joinConn(self.eb_location[0], self.eb_location[1])
        res = self.comm.receiveMessage('eb')

        msg = json.loads(res)
        self.ebpPub = paillier.PaillierPublicKey(g=int(msg['g']),
                                                 n=int(msg['n']))
        for i in range(len(self.votes)):
            for j in range(len(self.votes[i])):
                self.votes[i][j] = paillier.EncryptedNumber(
                    self.ebpPub, int(self.votes[i][j]), 0)
        totals = []
        if (len(self.votes) > 0):
            totals = self.votes.pop(0)
        for i in self.votes:
            if len(self.votes) != len(totals):
                quit()
            for j in self.votes[i]:
                totals[j] += self.votes[i][j]
        totals_expanded = [
            str(x.ciphertext()) for x in totals
        ]
        f = open('../common/comm.line', 'w')
        f.write(json.dumps(totals_expanded))
        f.close()
        self.comm.sendMessage("SENTOFF"*10)
        self.comm.closeConn()
        quit()


class CountingAuthorityGUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        myLabel = tk.Label(master, text="Waiting for votes...")
        myLabel.pack()
        self.model = CountingAuthority()

    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()

    def receiveVotes(self):
        self.model.receiveVotes()


if __name__ == '__main__':
    window = tk.Tk()
    app = CountingAuthorityGUI(window)
    app.master.title('Counting Authority Application')
    app.receiveVotes()
    print('cool')
