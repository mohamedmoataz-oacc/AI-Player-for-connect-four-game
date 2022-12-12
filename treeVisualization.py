from functools import partial
from tkinter import *
from board import Board
from minimaxTree import MinimaxTree

class TreeVisualizer():
    def __init__(self, tree: MinimaxTree) -> None:
        self.root = Tk()
        self.root.title("Tree Visualizer")
        self.root.geometry("1500x600")

        self.bg_canvas = Canvas(self.root, bg = '#f8b9c6', width = 1500, height = 600)
        self.bg_canvas.place(relx=0, rely=0)

        self.tree = tree
        self.parent = self.tree.root

        self.makeLevel()
        
        self.root.mainloop()

    def makeFrame(self, node, btext, bfunc):
        if btext == 'Child':
            f = Frame(self.root, bg = '#f8b9c6', width = 134, height = 150)
            Label(f, text = f'Score: {node.score}', bg = '#f8b9c6').place(relx=0.01, rely=0.83)
            Button(f, text = btext, bg="#FF7F50", font=("Helvetica", 8), command = partial(bfunc, node)).place(relx=0.6, rely=0.83)
        elif btext == 'Parent':
            f = Frame(self.root, bg = '#f8b9c6', width = 134, height = 150)
            Label(f, text = f'Score: {node.score}', bg = '#f8b9c6').place(relx=0.01, rely=0.05)
            Button(f, text = btext, bg="#FF7F50", font=("Helvetica", 8), command = bfunc).place(relx=0.6, rely=0.05)
        return f

    def boardToCanvas(self, node, btext, bfunc):
        frame = self.makeFrame(node, btext, bfunc)
        board = node.state
        board_canvas = Canvas(frame, width = 134, height = 116, bg = 'blue',
                highlightbackground = "blue", highlightcolor= "blue")
        if btext == 'Child': board_canvas.place(relx=0, rely=0)
        elif btext == 'Parent': board_canvas.place(relx=0, rely=0.23)
        columns = [i.copy() for i in board.columns]
        for column in columns:
            if len(column) < 6:
                x = len(column)
                for i in range(0, 6 - x):
                    column.append(2)
            column.reverse()

        for i in range(7):
            column = columns[i]
            for j in range(6):
                piece = column[j]
                if piece == 1:
                    out_color = 'black'
                    color = 'yellow'
                elif piece == 0:
                    out_color = 'black'
                    color = 'red'
                elif piece == 2:
                    color = 'white'
                    out_color = 'white'
                board_canvas.create_oval(8 + (i * 18), 8 + (j * 18), 18 + (i * 18), 18 + (j * 18),
                        fill = color, outline = out_color)
        return frame

    def makeLevel(self):
        self.boardToCanvas(self.parent, 'Parent', self.changeLevelUp).place(relx=0.45, rely=0.05)
        if len(self.parent.children) > 1:
            y = 0.8 / (len(self.parent.children) - 1)
            x = 0
            for child in self.parent.children:
                self.boardToCanvas(child, 'Child', self.changeLevelDown).place(relx = 0.05 + x, rely = 0.5)
                self.bg_canvas.create_line(750, 178, (0.1 + x) * 1500, 0.49 * 600)
                x += y
        elif len(self.parent.children) == 1:
            child = self.parent.children[0]
            self.boardToCanvas(child, 'Child', self.changeLevelDown).place(relx = 0.45, rely = 0.5)
            self.bg_canvas.create_line(750, 178, 750, 0.49 * 600)

    def changeLevelUp(self):
        if self.parent.parent is not None: self.parent = self.parent.parent
        else: return None
        self.deleteAllChildren()
        self.makeLevel()

    def changeLevelDown(self, node):
        self.parent = node
        self.deleteAllChildren()
        self.makeLevel()

    def deleteAllChildren(self):
        _list = self.root.winfo_children()
        for item in _list:
            item.destroy()
        self.bg_canvas = Canvas(self.root, bg = '#f8b9c6', width = 1500, height = 600)
        self.bg_canvas.place(relx=0, rely=0)

if __name__ == '__main__':
    b = Board()
    b.columns = [[0,0,0], [1,0,1,1], [0,1], [1,0,0], [1,1], [0,1,1], [1,0,0]]
    tv = TreeVisualizer(MinimaxTree(4, b, 1, False))