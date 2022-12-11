from tkinter import *
from connect4GUI import Connect4GUI

class optionsGUI():
    def __init__(self) -> None:
        self.master = Tk()
        self.master.title("Connect 4 game")
        self.master.geometry("500x500")

        self.var = IntVar()
        Radiobutton(self.master, text = "Human vs AI", variable = self.var, value=1).place(relx=0.1, rely=0.1)
        Radiobutton(self.master, text = "AI vs Human", variable = self.var, value=2).place(relx=0.1, rely=0.2)
        Radiobutton(self.master, text = "AI vs AI", variable = self.var, value = 3,
                    command = self.addK).place(relx=0.1, rely=0.3)

        self.name_var = StringVar()
        self.k1 = Entry(self.master, textvariable = self.name_var)
        self.p1var = BooleanVar()
        prunning1 = Checkbutton(self.master, text = "with prunning", 
                    variable = self.p1var, onvalue = True, offvalue = False)
        Label(self.master, text = "K1").place(relx = 0.55, rely = 0.15)
        self.k1.place(relx = 0.65, relwidth = 0.1, rely = 0.15)
        prunning1.place(relx = 0.77, rely = 0.14)
        
        

        Button(self.master, text = "Start", command = self.start).place(relx=0.15, rely = 0.4)

        self.master.mainloop()

    def addK(self):
        self.name_var2 = StringVar()
        self.k2 = Entry(self.master, textvariable= self.name_var2)
        self.p2var = BooleanVar()
        prunning2 = Checkbutton(self.master, text = "with prunning", 
                    variable = self.p2var, onvalue = True, offvalue = False)
        prunning2.place(relx = 0.77, rely = 0.24)
        Label(self.master, text = "K2").place(relx = 0.55, rely = 0.25)
        self.k2.place(relx = 0.65, relwidth = 0.1, rely = 0.25)

    def start(self):
        if self.var.get() != 0: self.master.destroy()
        if self.var.get() == 1:
            if self.name_var.get() != '': Connect4GUI(True, 0, int(self.name_var.get()), self.p1var.get())
        elif self.var.get() == 2:
            if self.name_var.get() != '': Connect4GUI(True, 1, int(self.name_var.get()), self.p1var.get())
        elif self.var.get() == 3:
            if self.name_var.get() != '' and self.name_var2.get() != '':
                c4g = Connect4GUI(False, 1, int(self.name_var.get()), self.p1var.get())
                c4g.addAIAgent(int(self.name_var2.get()), self.p2var.get())

optionsGUI()