#!/usr/bin/env python

import tkinter as tk
import json
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from common.communications import Comm


# Graphical BulletenBoardGUI class manages data with BullitenBoard object
class BulletinBoard():
    def __init__(self):
        self.votes = []
        self.ca_location = ('localhost', 1337)
        self.eb_location = ('localhost', 5858)
        self.comm = Comm('bb', 6969)

    def receiveVotes(self):
        self.comm.initiateConn()
        keepGoing = True
        while keepGoing:
            res = self.comm.receiveMessage('eb')
            msg = json.loads(res)
            if msg == 'ENDVOTING':
                keepGoing = False
            else:
                self.votes.append(json.loads(msg['phrase']))
                self.listVotes()

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
                label = tk.Label(text='%d.%d' % (i, j), relief=tk.RIDGE)
                label.grid(row=i, column=j, sticky=tk.NSEW)


if __name__ == '__main__':
    app = BulletinBoardGUI()
    app.master.title('Bulletin Board Application')
    app.mainloop()
