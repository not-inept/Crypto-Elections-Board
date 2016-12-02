import json
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import tkinter as tk


class CountingAuthority():
    def __init__(self):
        self.bb_location = ('localhost', 6969)
        self.eb_location = ('localhost', 5858)
        self.comm = Comm('ca', 1337)

    def sendVotes(self):
        return

    def tallyVotes(self):
        return

    def receiveVotes(self):
        self.comm.initiateConn()


class CountingAuthorityGUI():
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        myLabel = tk.Label(master, text="Waiting for votes...")
        myLabel.pack()

    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()
