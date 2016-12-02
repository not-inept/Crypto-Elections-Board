import tkinter as tk


class CountingAuthority():
    def __init__(self):
        self.bb_location = ('localhost', 6969)
        self.eb_location = ('localhost', 5858)


class CAGUI():
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        myLabel = tk.Label(master, text="Waiting for votes...")
        myLabel.pack()

    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()
