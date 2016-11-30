#!/usr/bin/env python

import tkinter as tk
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
        password = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(N))
        print(password)
        self.voters.append(hashlib.sha256(password).hexdigest())
        return (user, password)

    def isRegisteredVoter(self, user, password):
        if (len(self.voters) > user):
            return self.voters[user] == hashlib.sha256(password).hexdigest()
        else:
            return False

    def sendVotes(self, user, password, votes):
        if (self.isRegisteredVoter(user, password)):
            # sign votes/encrypt votes
            # send votes
            # zkp?
            return

    def startVote(self):
        return


class ElectionBoardGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        master.minsize(400, 400)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.registerButton = tk.Button(self, text='Register',
                                        command=self.displayRegistration)
        self.registerButton.grid()

        self.quitButton = tk.Button(self, text='Quit',
                                    command=self.quit)
        self.quitButton.grid()

    def displayRegistration(self):
        return


if __name__ == '__main__':
    window = tk.Tk()
    app = ElectionBoardGUI(window)
    app.master.title('Election Board Application')
    app.mainloop()
