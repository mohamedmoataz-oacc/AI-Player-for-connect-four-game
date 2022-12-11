from tkinter import *
from connect4GUI import Connect4GUI
from board import Board

class optionsGUI():
    def __init__(self) -> None:
        self.master = Tk()
        self.master.title("Connect 4 game")
        self.master.geometry("500x500")

        self.var = IntVar()
        Radiobutton(self.master, text = "Human vs AI", variable = self.var, value=1).place(relx=0.2, rely=0.3)
        Radiobutton(self.master, text = "AI vs Human", variable = self.var, value=2).place(relx=0.2, rely=0.4)
        Radiobutton(self.master, text = "AI vs AI", variable = self.var, value=3).place(relx=0.2, rely=0.5)

        Button(self.master, text = "Start", command = self.start).place(relx=0.3, rely = 0.8)

        self.master.mainloop()

    def start(self):
        if self.var.get() != 0: self.master.destroy()
        if self.var.get() == 1: Connect4GUI(True, 0)
        elif self.var.get() == 2: Connect4GUI(True, 1)

optionsGUI()