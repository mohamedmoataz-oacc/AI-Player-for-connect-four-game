from tkinter import *
from connect4GUI import Connect4GUI

x = ''
with open('x.txt', 'r') as file:
    x = file.readline()
class optionsGUI():
    def __init__(self, x1) -> None:
        if x1 == '1': return None
        with open('x.txt', 'w') as file:
            file.write('1')
        self.master = Tk()
        self.master.title("Connect 4 game")
        self.master.geometry("650x300")
        self.master.config(bg="#2F4F4F")

        self.var = IntVar()
        Radiobutton(self.master, text = "Human vs AI", variable = self.var, bg="#2F4F4F",
                value=1, font=("Helvetica", 18)).place(relx=0.1, rely=0.1)
        Radiobutton(self.master, text = "AI vs Human", variable = self.var, bg="#2F4F4F",
                value=2, font=("Helvetica", 18)).place(relx=0.1, rely=0.3)
        Radiobutton(self.master, text = "AI vs AI", variable = self.var, value = 3, bg="#2F4F4F",
                    command = self.addK, font=("Helvetica", 18)).place(relx=0.1, rely=0.5)

        self.name_var = StringVar()
        self.k1 = Entry(self.master, textvariable = self.name_var)
        self.p1var = BooleanVar()
        prunning1 = Checkbutton(self.master, text = "with prunning", font=("Helvetica", 14),
                    variable = self.p1var, bg="#2F4F4F", onvalue = True, offvalue = False)
        Label(self.master, text = "K1", font=("Helvetica", 14), bg="#2F4F4F").place(relx = 0.55, rely = 0.2)
        self.k1.place(relx = 0.65, relwidth = 0.1, rely = 0.2)
        prunning1.place(relx = 0.77, rely = 0.19)

        Button(self.master, text = "Start", font=("Helvetica", 14),
        command = self.start).place(relx=0.45, rely = 0.8, relwidth=0.1)

        self.master.mainloop()

    def addK(self):
        self.name_var2 = StringVar()
        self.k2 = Entry(self.master, textvariable = self.name_var2)
        self.p2var = BooleanVar()
        prunning2 = Checkbutton(self.master, text = "with prunning", font=("Helvetica", 14), 
                    variable = self.p2var, bg="#2F4F4F", onvalue = True, offvalue = False)
        prunning2.place(relx = 0.77, rely = 0.39)
        Label(self.master, text = "K2", font=("Helvetica", 14), bg="#2F4F4F").place(relx = 0.55, rely = 0.4)
        self.k2.place(relx = 0.65, relwidth = 0.1, rely = 0.4)

    def start(self):
        if self.var.get() != 0:
            self.master.destroy()
            global x
            x = True
        if self.var.get() == 1:
            if self.name_var.get() != '': Connect4GUI(True, 0, int(self.name_var.get()), self.p1var.get())
        elif self.var.get() == 2:
            if self.name_var.get() != '': Connect4GUI(True, 1, int(self.name_var.get()), self.p1var.get())
        elif self.var.get() == 3:
            if self.name_var.get() != '' and self.name_var2.get() != '':
                c4g = Connect4GUI(False, 1, int(self.name_var.get()), self.p1var.get())
                c4g.addAIAgent(int(self.name_var2.get()), self.p2var.get())
        with open('x.txt', 'w') as file:
            file.write('0')

optionsGUI(x)