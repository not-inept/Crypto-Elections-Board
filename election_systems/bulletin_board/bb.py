#!/usr/bin/env python

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
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

    def receiveVotes(self, tkobj):
        app.update_idletasks()
        app.update()
        self.comm.initiateConn()
        keepGoing = True
        while keepGoing:
            res = self.comm.receiveMessage('eb')
            msg = json.loads(res)
            print(msg)
            if msg == 'ENDVOTING':
                keepGoing = False
            else:
                self.votes.append(msg)
                tkobj.updateVoteList()
            app.update_idletasks()
            app.update()
        self.comm.closeConn()
        self.comm.joinConn(self.ca_location[0], self.ca_location[1])
        self.comm.sendMessage(json.dumps(self.votes))
        self.comm.closeConn()
        quit()


class BulletinBoardGUI(tk.Frame):
    def __init__(self, master):
        self.model = BulletinBoard()
        f = open('../common/candidates.json', 'r')
        self.candidates = json.loads(f.read())
        f.close()
        tk.Frame.__init__(self, master)
        master.minsize(400, 400)
        self.master = master
        self.main = tk.Frame(self.master, width=400, height=400)
        self.updateVoteList()

    def receiveVotes(self):
        self.model.receiveVotes(self)

    def votersCollected(self):
        vLabel = tk.Label(text="Voters Calculated")
        vLabel.pack()
        quitButton = tk.Button(self, text="Quit", command=self.quit)
        quitButton.pack()

    def updateVoteList(self):
        self.main.destroy()
        # for i in range(len(self.model.votes)):
        #     for j in range(4):
        #         label = tk.Label(
        #             text='%d.%d' % (i, j), relief=tk.RIDGE)
        #         label.grid(row=i, column=j, sticky=tk.NSEW)
        # self.grid()
        innards = ''
        for i in range(len(self.model.votes)):
            innards += json.dumps(self.model.votes[i]) + '\n'
        self.main = tk.Frame(self.master, width=400, height=400)
        st = ScrolledText(self.main, width=400, height=400)
        st.pack()
        st.insert(tk.END, innards)
        self.main.pack(fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    window = tk.Tk()
    app = BulletinBoardGUI(window)
    app.master.title('Bulletin Board Application')
    app.receiveVotes()