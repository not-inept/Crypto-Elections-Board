#!/usr/bin/env python

import tkinter as tk
import random
import string
import hashlib


class ElectionBoard():
    def __init__(self):
        self.voters = []
        self.ca_location = ('localhost', 1337)
        self.bb_location = ('localhost', 6969)

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

    def startVote(self):
        # check to make sure that bb server is running at host

        return

    def sendVote(self, user, password, vote):
        if (self.isRegisteredVoter(user, password)):
            # for
            # sign votes/encrypt votes
            # send votes
            # zkp?
            return


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
        regWin = tk.Toplevel(self)
        regWin.title("Register Voter")

        username = tk.StringVar()
        usernameBox = tk.Entry(regWin, textvariable=username)
        usernameLabel = tk.Label(regWin, text="UserName: ")
        usernameLabel.pack()
        usernameBox.pack()

        password = tk.StringVar()
        passwordBox = tk.Entry(regWin, textvariable=password)
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
        candidates = ["1", "2", "3", "4"]
        var = tk.StringVar()
        for candi in candidates:
            t = tk.Radiobutton(temp, text=candi, value=candi, variable=var)
            t.pack()
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
