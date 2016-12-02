import json
import os
import sys
import inspect
import tkinter as tk
from common.communications import Comm
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


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
        res = self.comm.receiveMessage('bb')
        msg = json.loads(res)
        self.comm.closeConn()
        print(msg)
        self.votes = msg


class CountingAuthorityGUI(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        myLabel = tk.Label(master, text="Waiting for votes...")
        myLabel.pack()
        self.model = CountingAuthority()

    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()

    def receiveVotes(self):
        self.model.receiveVotes()


if __name__ == '__main__':
    window = tk.Tk()
    app = CountingAuthorityGUI(window)
    app.master.title('Counting Authority Application')
    app.receiveVotes()
    print('cool')
