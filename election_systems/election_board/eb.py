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
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from common.communications import Comm


class ElectionBoard():
    def __init__(self):
        self.voters = {}
        self.ca_location = ('localhost', 1337)
        self.bb_location = ('localhost', 6969)
        self.comm = Comm('eb', 5858)
        self.pPub, self.pPriv = paillier.generate_paillier_keypair()
        self.voting = False
        self.waiting = False

    def registerVoter(self):
        if not self.voting:
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
        return None, None

    def isValidVoter(self, user, passw):
        return self.voters[user] == hashlib.sha256(
            passw.encode('utf-8')).hexdigest()

    def startVote(self):
        # check to make sure that bb server is running at host
        try:
            self.comm.joinConn(self.bb_location[0], self.bb_location[1])
            self.voting = True
        except:
            return False
        return True

    def sendVote(self, user, password, vote):
        if (password is not None and self.isValidVoter(
            user, password) and self.voting):
            encrypted_vote_list = [self.pPub.encrypt(v) for v in vote]
            self.voters[user] = None
            enc_expanded = [
                str(x.ciphertext()) for x in encrypted_vote_list
            ]
            self.comm.sendMessage(json.dumps(enc_expanded))
        else:
            quit()

    def receiveTotals(self):
        self.voting = False
        self.waiting = True
        self.comm.sendMessage(json.dumps('ENDVOTING'))
        self.comm.closeConn()
        self.comm.initiateConn()
        pub_rec = {'g': int(self.pPub.g), 'n': int(self.pPub.n)}
        self.comm.sendMessage(json.dumps(pub_rec))
        res = self.comm.receiveMessage('ca')
        print('got here')
        f = open('../common/comm.line', 'r')
        res = f.read()
        f.close()
        msg = json.loads(res)
        print(msg)
        tmp = [paillier.EncryptedNumber(self.pPub, int(v), 0) for v in msg]
        decrypted_total_list = [self.pPriv.decrypt(v) for v in tmp]
        print(decrypted_total_list)


# class that displays quit and confirm type buttons on each page
class ButtonFrame(tk.Frame):
    def __init__(self, master, buttonText, buttonCommand):
        tk.Frame.__init__(self, master)
        otherButton = tk.Button(self, text=buttonText, command=buttonCommand)
        # quitButton = tk.Button(self, text='Quit', command=quitCommand)
        otherButton.pack(side=tk.LEFT, padx=60, pady=10)
        # quitButton.pack(side=tk.RIGHT, padx=60, pady=10)


class ElectionBoardGUI(tk.Frame):
    def __init__(self, master):
        self.model = ElectionBoard()
        self.master = master
        self.voting = True
        f = open('../common/candidates.json', 'r')
        self.candidates = json.loads(f.read())
        f.close()
        tk.Frame.__init__(self, master)
        master.minsize(400, 400)

        self.main = tk.Frame(master, width=400, height=400)
        temp = ButtonFrame(self.main, "Register Voter",
                           self.displayRegistration)
        temp.pack(side=tk.LEFT)

        temp = ButtonFrame(self.main, "Start Vote",
                           self.displayStartVote)
        temp.pack(side=tk.RIGHT)

        temp = ButtonFrame(self.main, "Close", self.quit)
        temp.pack(side=tk.BOTTOM)

        self.main.pack(fill=tk.BOTH, expand=True)

    # displays the registration screen
    def displayRegistration(self):
        user, passw = self.model.registerVoter()
        regWin = tk.Toplevel(self)
        regWin.title("Register Voter")
        username = tk.StringVar()
        username.set(user)
        usernameBox = tk.Entry(
            regWin, textvariable=username, relief='flat',
            state='readonly', readonlybackground='white', fg='black')
        usernameLabel = tk.Label(regWin, text="UserName: ")
        usernameLabel.pack()
        usernameBox.pack()
        password = tk.StringVar()
        password.set(passw)
        passwordBox = tk.Entry(
            regWin, textvariable=password, relief='flat',
            state='readonly', readonlybackground='white', fg='black')
        passwordLabel = tk.Label(regWin, text="Password: ")
        passwordLabel.pack()
        passwordBox.pack()
        temp = ButtonFrame(regWin, "Close", regWin.destroy)
        temp.pack(side=tk.BOTTOM)

    # displays the start voting screen
    def displayStartVote(self):
        started = self.model.startVote()
        if started:
            self.voting = True
            self.master.title("Voting Period")
            self.main.destroy()
            self.main = tk.Frame(self.master, width=400, height=400)
            temp = ButtonFrame(self.main, "Vote", self.displayVoting)
            temp.pack(side=tk.LEFT)

            temp = ButtonFrame(self.main, "End Vote", self.displayEndVoting)
            temp.pack(side=tk.RIGHT)
            self.main.pack(fill=tk.BOTH, expand=True)

    def submitVote(self, user, passw, vote, me):
        if user == '' or passw == '' or vote == '':
            pass
        else:
            realVote = []
            vote = int(vote)
            for i in range(len(self.candidates['choices'])):
                if i == vote:
                    realVote.append(1)
                else:
                    realVote.append(0)
            self.model.sendVote(user, passw, realVote)
        me.destroy()

    def displayVoting(self):
        voteWin = tk.Toplevel()
        voteWin.title("Voting Card")

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

        voteText = tk.Label(temp, text=self.candidates['question'])
        voteText.pack()

        var = tk.StringVar()
        i = 0
        for candi in self.candidates['choices']:
            t = tk.Radiobutton(temp, text=candi, value=i, variable=var)
            i += 1
            t.pack()
        temp.pack()
        temp = ButtonFrame(voteWin, "Submit",
                           lambda: self.submitVote(username.get(),
                                                   password.get(),
                                                   var.get(),
                                                   voteWin))
        temp.pack(side=tk.BOTTOM)

    def displayEndVoting(self):
        print("End Voting")
        self.master.title("Waiting for Results")
        self.main.destroy()
        self.main = tk.Frame(self.master, width=400, height=400)

        waitingLabel = tk.Label(self.main,
                                text="Waiting for results to be tallied...")
        waitingLabel.pack()
        self.main.pack(fill=tk.BOTH, expand=True)
        self.update_idletasks()
        self.update()
        self.model.receiveTotals()


if __name__ == '__main__':
    window = tk.Tk()
    app = ElectionBoardGUI(window)
    app.master.title('Election Board Application')
    app.mainloop()
