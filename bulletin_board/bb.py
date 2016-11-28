#!/usr/bin/env python

import Tkinter as tk


# Graphical BulletenBoardGUI class manages data with BullitenBoard object
class BulletinBoard():
    def __init__(self):
        self.votes = []

    def verifyUniqueVotes(self):
        return

    def receiveVotes(self):
        return

    def listVotes(self):
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
                l = tk.Label(text='%d.%d' % (i, j), relief=tk.RIDGE)
                l.grid(row=i, column=j, sticky=tk.NSEW)


app = BulletinBoardGUI()
app.master.title('Bulletin Board Application')
app.mainloop()
