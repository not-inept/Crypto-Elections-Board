#!/usr/bin/env python

import tkinter as tk


# Graphical BulletenBoardGUI class manages data with BullitenBoard object
class BulletinBoard():
    def __init__(self):
        self.votes = []
        self.ca_location = ('localhost', 1337)
        self.eb_location = ('localhost', 5858)

    def verifyUniqueVotes(self):
        return

    def receiveVotes(self):
        return

    def listVotes(self):
        return

    def listenForEb(self):
        return


class BulletinBoardGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.bulletinBoard = BulletinBoard()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',
                                    command=self.quit)
        self.quitButton.grid()

        for i in range(100):
            for j in range(4):
                label = tk.Label(text='%d.%d' % (i, j), relief=tk.RIDGE)
                label.grid(row=i, column=j, sticky=tk.NSEW)

    def votersCollected(self):
        vLabel = tk.Label(text="Voters Calculated")
        vLabel.pack()
        quitButton = tk.Button(self, text="Quit", command=self.quit)
        quitButton.pack()


if __name__ == '__main__':
    app = BulletinBoardGUI()
    app.master.title('Bulletin Board Application')
    app.mainloop()
