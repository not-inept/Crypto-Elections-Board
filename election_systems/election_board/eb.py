#!/usr/bin/env python

import tkinter as tk
import random
import string
import hashlib
import json
from phe import paillier
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from common.communications import Comm


class ElectionBoard():
    def __init__(self):
        self.voters = {}
        self.ca_location = ('localhost', 1337)
        self.bb_location = ('localhost', 6969)
        self.comm = Comm('eb', 5858)
        self.pPub, self.pPriv = paillier.generate_paillier_keypair()

    def registerVoter(self):
        user = len(self.voters)
        N = 64
        user = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(N))
        while user in self.voters:
            user = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(N))
        password = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(N))
        self.voters[user] = hashlib.sha256(
            password.encode('utf-8')).hexdigest()
        return user, password

    def isValidVoter(self, user, password):
        if (len(self.voters) > user):
            return self.voters[user] == hashlib.sha256(password).hexdigest()
        else:
            return False

    def startVote(self):
        # check to make sure that bb server is running at host
        try:
            self.comm.joinConn(self, self.bb_location[0], self.bb_location[1])
        except:
            return False
        return True

    def sendVote(self, user, password, vote):
        if (password is not None and self.isValidVoter(user, password)):
            encrypted_vote_list = [self.pPub.encrypt(v) for v in vote]
            self.voters[user] = None
            enc_expanded = [
                str(x.ciphertext()) for x in encrypted_vote_list
            ]
            self.comm.sendMessage(json.dumps(enc_expanded))
        else:
            quit()

    def receiveTotals(self):
        self.comm.sendMessage(json.dumps('ENDVOTING'))
        self.comm.closeConn()
        self.comm.initiateConn()
        res = json.loads(self.comm.receiveMessage('ca'))
        decrypted_total_list = [self.pPriv.decrypt(v) for v in res]
        return decrypted_total_list


# class that displays quit and confirm type buttons on each page
class ButtonFrame(tk.Frame):
    def __init__(self, master, buttonText, buttonCommand, quitCommand):
        tk.Frame.__init__(self, master)
        otherButton = tk.Button(self, text=buttonText, command=buttonCommand)
        quitButton = tk.Button(self, text='Quit', command=quitCommand)
        otherButton.pack(side=tk.LEFT, padx=60, pady=10)
        quitButton.pack(side=tk.RIGHT, padx=60, pady=10)


class ElectionBoardGUI(tk.Frame):
    def __init__(self, master):
        self.model = ElectionBoard()
        tk.Frame.__init__(self, master)
        master.minsize(400, 400)

        temp = tk.Frame(master)
        b1 = tk.Button(temp, text="Register Voter",
                       command=self.displayRegistration)
        b2 = tk.Button(temp, text="Start Vote",
                       command=self.displayStartVote)
        b1.pack()
        b2.pack()
        label1 = tk.Label(master, text="1st page")
        label1.pack()
        temp.pack()
        temp = ButtonFrame(master, "OK", self.quit, self.quit)
        temp.pack(side=tk.BOTTOM)

    # displays the registration screen
    def displayRegistration(self):
        print("register")
        user, passw = self.model.registerVoter()
        regWin = tk.Toplevel(self)
        regWin.title("Register Voter")
        username = tk.StringVar()
        username.set(user)
        usernameBox = tk.Entry(regWin, textvariable=username, relief='flat', state='readonly', readonlybackground='white', fg='black')
        usernameLabel = tk.Label(regWin, text="UserName: ")
        usernameLabel.pack()
        usernameBox.pack()
        password = tk.StringVar()
        password.set(passw)
        passwordBox = tk.Entry(regWin, textvariable=password, relief='flat', state='readonly', readonlybackground='white', fg='black')
        passwordLabel = tk.Label(regWin, text="Password: ")
        passwordLabel.pack()
        passwordBox.pack()
        temp = ButtonFrame(regWin, "OK", regWin.destroy, regWin.destroy)
        temp.pack(side=tk.BOTTOM)

    # displays the start voting screen
    def displayStartVote(self):
        print("startvote")
        voteWin = tk.Toplevel()
        voteWin.title("Start Voting")

        voteButton = tk.Button(voteWin, text="Vote",
                               command=self.displayVoting)
        voteButton.pack()
        endButt = tk.Button(voteWin, text="End Vote",
                            command=self.displayEndVoting)
        endButt.pack()

        temp = ButtonFrame(voteWin, "OK", voteWin.destroy, voteWin.destroy)
        temp.pack(side=tk.BOTTOM)

    def displayVoting(self):
        print("voting")
        voteWin = tk.Toplevel()
        voteWin.title("Voting Screen")

        temp = tk.Frame(voteWin)
        username = tk.StringVar()
        usernameBox = tk.Entry(temp, textvariable=username)
        usernameLabel = tk.Label(temp, text="UserName: ")
        usernameLabel.pack()
        usernameBox.pack()

        password = tk.StringVar()
        passwordBox = tk.Entry(temp, textvariable=password)
        passwordLabel = tk.Label(temp, text="Password: ")
        passwordLabel.pack()
        passwordBox.pack()

        voteText = tk.Label(temp, text="Who are you voting for?")
        voteText.pack()
        temp.pack()

        temp = ButtonFrame(voteWin, "Submit", voteWin.destroy, voteWin.destroy)
        temp.pack(side=tk.BOTTOM)

    def displayEndVoting(self):
        print("End Voting")
        voteWin = tk.Toplevel()
        voteWin.title("End Voting Screen")

        waitingLabel = tk.Label(voteWin,
                                text="waiting for tallies to finish...")
        waitingLabel.pack()

        temp = ButtonFrame(voteWin, "OK", voteWin.destroy, voteWin.destroy)
        temp.pack(side=tk.BOTTOM)


if __name__ == '__main__':
    window = tk.Tk()
    app = ElectionBoardGUI(window)
    app.master.title('Election Board Application')
    app.mainloop()
