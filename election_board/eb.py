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
        user = len(self.voters)
        N = 64
        password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
        self.voters.append(hashlib.sha256(password).hexdigest())
        return (user, password)

    def isRegisteredVoter(self, user, password):
        if (len(self.voters) > user):
            return self.voters[user] == hashlib.sha256(password).hexdigest()
        else:
            return False

    def collectVotes(self, user, password, votes):
        if (self.isRegisteredVoter(user, password)):
            # sign votes/encrypt votes
            # send votes
            # zkp?
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


if __name__ == 'main':
    app = ElectionBoardGUI()
    app.master.title('Election Board Application')
    app.mainloop()
