from functools import partial
from tkinter import *
from PIL import Image, ImageTk
from board import Board
from connect4AIPlayer import Connect4AIPlayer
from treeVisualization import TreeVisualizer

class Connect4GUI():
    def __init__(self, human: bool, player: int, k: int, prunning: bool) -> None:
        self.root = Tk()
        self.root.title("Connect 4 game")
        self.root.geometry("1300x750")

        self.player = player # determines wich player is the human (or the 1st ai player if we choose ai vs ai)
        self.ai = (player + 1) % 2
        self.ai_player = Connect4AIPlayer(k, prunning, self.ai)
        self.thinking_tree = None
        
        self.yellow = ImageTk.PhotoImage(Image.open("yellow.png"))
        self.red = ImageTk.PhotoImage(Image.open("red.png"))
        self.c = Canvas(self.root)
        self.c.place(relx = 0.13, rely = 0.15, relwidth = 0.84, relheight= 0.84)
        if human:
            im = ImageTk.PhotoImage(Image.open("board.png"))
            self.c.create_image(400,320, image=im)
        
        if human:
            for i in range(1, 8):
                self.root.bind(str(i), self.callAddPiece)
        else:
            Button(self.root, text = "Next", bg="#FF4500", font=("Helvetica", 14),
                    command = self.nextTurn).place(relx = 0.75, rely = 0.75)

        self.pieces_in_columns = [0,0,0,0,0,0,0]
        self.rows_positions = {5: 79, 4: 171, 3: 274, 2: 364, 1: 461, 0: 554}
        self.columns_positions = {0: 93, 1: 191, 2: 287, 3: 388, 4: 484, 5: 580, 6: 674}

        Button(self.root, text = "Show minimax tree", bg="#FF4500", font=("Helvetica", 14),
                command = self.visualizeTree).place(relx = 0.75, rely = 0.35)

        self.board = Board()
        if self.ai == 0 and human:
            self.root.after(1000, partial(self.aiThink, self.board))

        if human: self.root.mainloop()

    def nextTurn(self):
        turn = self.board.turn
        if turn == 0:
            x = self.ai_player.decision(self.board.copy())
            self.thinking_tree = self.ai_player.last_turn_tree
            self.addPiece(x)
        if turn == 1:
            x = self.ai_player2.decision(self.board.copy())
            self.thinking_tree = self.ai_player2.last_turn_tree
            self.addPiece(x)

    def addAIAgent(self, k: int, prunning: bool):
        self.ai_player2 = Connect4AIPlayer(k, prunning, self.player)
        im = ImageTk.PhotoImage(Image.open("board.png"))
        self.c.create_image(400,320, image=im)
        x = self.ai_player.decision(self.board.copy())
        self.thinking_tree = self.ai_player.last_turn_tree
        self.addPiece(x)
        self.root.mainloop()

    def callAddPiece(self, num):
        pieces_in_column = self.pieces_in_columns[int(num.char) - 1]
        if pieces_in_column == 6: return None
        if self.player == self.board.turn:
            self.addPiece(num)

        self.root.after(1000, partial(self.aiThink, self.board))

    def aiThink(self, board):
        x = self.ai_player.decision(self.board.copy())
        self.thinking_tree = self.ai_player.last_turn_tree
        self.addPiece(x)


    def addPiece(self, column_num):
        if self.board.end: return None
        if not isinstance(column_num, int): column_num = int(column_num.char) - 1
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
            Label(self.root, text = f"\tPlayer1: {points[0]}\t\t\tPlayer2: {points[1]}", 
            fg="black", font=("Helvetica", 20)).place(relx=0.1, rely=0.08)

    def visualizeTree(self):
        if self.thinking_tree is not None:
            TreeVisualizer(self.thinking_tree)