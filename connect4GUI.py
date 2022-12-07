from tkinter import *
from PIL import Image, ImageTk
from board import Board

class Connect4GUI():
    def __init__(self, board: Board) -> None:
        self.root = Tk()
        self.root.title("Connect 4 game")
        self.root.geometry("1000x750")

        im = ImageTk.PhotoImage(Image.open("board.png"))
        Label(self.root, image = im).place(relx = 0.15, rely = 0.15)
        
        self.yellow = ImageTk.PhotoImage(Image.open("yellow.png"))
        self.red = ImageTk.PhotoImage(Image.open("red.png"))
        self.c = Canvas(self.root)
        self.c.create_image(400,320,image=im)
        self.c.place(relx = 0.13, rely = 0.15, relwidth = 0.84, relheight= 0.84)
        
        for i in range(1, 8):
            self.root.bind(str(i), self.addPiece)

        self.pieces_in_columns = [0,0,0,0,0,0,0]
        self.rows_positions = {5: 79, 4: 171, 3: 274, 2: 364, 1: 461, 0: 554}
        self.columns_positions = {0: 93, 1: 191, 2: 287, 3: 388, 4: 484, 5: 580, 6: 674}

        self.board = Board()

        self.root.mainloop()

    def addPiece(self, column_num):
        if self.board.end: return None
        column_num = int(column_num.char) - 1
        pieces_in_column = self.pieces_in_columns[column_num]
        if pieces_in_column == 6: return None
        self.pieces_in_columns[column_num] += 1
        if self.board.turn == 0: image = self.red
        elif self.board.turn == 1: image = self.yellow
        piece = self.c.create_image(self.columns_positions[column_num], 19, image = image)
        self.board.addPiece(column_num = column_num)
        end = self.rows_positions[pieces_in_column]
        y = 19
        def move():
            nonlocal y
            y += 5
            x = 5
            if y > end:
                x = 5 - (y - end)
                y = end
            self.c.move(piece, 0, x)
            if y != end: self.root.after(1, move)
        
        move()
        if self.board.end:
            points = self.board.checkWinner()
            Label(self.root, text = f"Player1: {points[0]}      Player2: {points[1]}").place(relx=0.3, rely=0.08)


Connect4GUI(Board())