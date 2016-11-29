#!/usr/bin/env python

import Tkinter as tk
import random
import string
import hashlib


class ElectionBoard():
    def __init__(self):
        self.votes = []
        self.voters = []

    def registerVoter(self):
        username = len(self.voters)
        N = 64
        password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
        self.voters.append(hashlib.sha256(password).hexdigest())
        return (username, password)

    def listenForVote(self):
        return


class CountingAuthority():
    def __init_(self):
        return


class ElectionBoardGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',
                                    command=self.quit)
        self.quitButton.grid()


app = ElectionBoardGUI()
app.master.title('Election Board Application')
app.mainloop()
