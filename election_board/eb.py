#!/usr/bin/env python

import Tkinter as tk


class ElectionBoard():
    def __init__(self):
        self.votes = []

    def registerVoter(self):
        return

    def listenForVote(self):
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


app = ElectionBoard()
app.master.title('Election Board Application')
app.mainloop()