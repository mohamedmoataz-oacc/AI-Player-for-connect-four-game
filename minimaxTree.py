import time
from board import Board
from collections import deque

class Node():
    def __init__(self, state: Board, parent):
        self.parent = parent
        if self.parent is not None:
            # node type: 0 for max node and 1 for min node
            self.node_type: int = (self.parent.node_type + 1) % 2
            self.depth: int = self.parent.depth + 1
            self.move: int = None
            self.alpha: int = self.parent.alpha
            self.beta: int = self.parent.beta
        else:
            self.node_type = 0
            self.depth = 0
            self.move = None
            self.alpha = float('-inf')
            self.beta = float('inf')
        if self.node_type == 0: self.score = float('-inf')
        else: self.score = float('inf')
        self.children: list = []
        self.state: Board = state

    def addChild(self, state: Board, move: int):
        n = Node(state, self)
        n.move = move
        self.children.append(n)
        return n

    def getPrunningValues(self):
        self.alpha = self.parent.alpha
        self.beta = self.parent.beta


class MinimaxTree():
    def __init__(self, tree_depth, board: Board, player: int, prunning: bool):
        self.root: Node = Node(board, None)
        self.size: int = 1
        self.tree_depth: int = tree_depth
        self.player: int = player
        self.prunning: bool = prunning
        self.heuristic_points: dict = {
            self.player: {2: 20, 3: 30, 4: 105},
            (self.player + 1) % 2: {2: -25, 3: -35, 4: -100}
        }
        # self.num = 1
        self.constructTree()
        
    def calculateLeafNodeScore(self, node: Node):
        board = node.state
        columns = [i.copy() for i in board.columns]
                    
        # print(self.num, ":", end = " ")
        node.score = self.getColumnHeurstic(columns)
        node.score += self.getRowHeurstic(columns)
        node.score += self.getDiagonalHeurstic(columns)
        # print("")
        # self.num += 1

        if self.prunning:
            if node.node_type == 0: node.alpha = node.score
            elif node.parent.node_type == 1:  node.beta = node.score
        
    def constructTree(self):
        stack = deque()
        stack.append(self.root)
        current: Node = None
        while stack:
            current = stack.pop()
            if self.prunning and current.parent is not None: current.getPrunningValues()
            board = current.state
            moves = board.generatePossibleMoves()
            for move in moves:
                bcopy = board.copy()
                bcopy.addPiece(move)
                p = current.addChild(bcopy, move)
                self.size += 1
                if p.depth < self.tree_depth: stack.append(p)
                elif p.depth == self.tree_depth:
                    self.calculateLeafNodeScore(p)
                    self.passScore(p)
                    if self.prunning and current.alpha > current.beta: break

            # To view the element at the top of the stack without removing it
            if stack:
                t = stack.pop()
                stack.append(t)
            
                if t.depth <= current.depth:
                    diff = (current.depth - t.depth) + 1
                    for i in range(diff):
                        self.passScore(current)
                        current = current.parent
             
        while current.parent is not None:
            self.passScore(current)
            current = current.parent

    def passScore(self, node):
        if node.parent.node_type == 0:
            if node.score > node.parent.score:
                node.parent.score = node.score
                if self.prunning and node.beta > node.parent.alpha: node.parent.alpha = node.beta
        elif node.parent.node_type == 1:
            if node.score < node.parent.score:
                node.parent.score = node.score
                if self.prunning and node.alpha < node.parent.beta: node.parent.beta = node.alpha

    def getColumnHeurstic(self, columns):
        score = 0
        for column in columns:
            for i in range(4,7):
                numbers = column[i-4:i]

                zeros = numbers.count(0)
                ones = numbers.count(1)

                if zeros != 0 and ones != 0: continue
                elif zeros > 1:
                    score += self.heuristic_points[0][zeros]
                    # print(self.heuristic_points[0][zeros], end=", ")
                elif ones > 1:
                    score += self.heuristic_points[1][ones]
                    # print(self.heuristic_points[1][ones], end=", ")
        # print("|", end="")
        return score

    def getRowHeurstic(self, c):
        rows = list(zip(*c))
        score = 0
        for row in rows:
            for i in range(4,8):
                numbers = row[i-4:i]

                zeros = numbers.count(0)
                ones = numbers.count(1)

                if zeros != 0 and ones != 0: continue
                elif zeros > 1:
                    score += self.heuristic_points[0][zeros]
                    # print(self.heuristic_points[0][zeros], end=", ")
                elif ones > 1:
                    score += self.heuristic_points[1][ones]
                    # print(self.heuristic_points[1][ones], end=", ")
        # print("|", end="")
        return score

    def getDiagonalHeurstic(self, c):
        score = 0
        for index in range(0, 4):
            for i in range(0, 3):
                window1 = [c[index + j][i + j] for j in range(0, 4)]
                zeros = window1.count(0)
                ones = window1.count(1)

                if zeros != 0 and ones != 0: continue
                elif zeros > 1:
                    score += self.heuristic_points[0][zeros]
                    # print(self.heuristic_points[0][zeros], end=", ")
                elif ones > 1:
                    score += self.heuristic_points[1][ones]
                    # print(self.heuristic_points[1][ones], end=", ")
        # print("|", end="")

        for index in range(6, 2, -1):
            for i in range(0, 3):
                window1 = [c[index - j][i + j] for j in range(0, 4)]
                zeros = window1.count(0)
                ones = window1.count(1)

                if zeros != 0 and ones != 0: continue
                elif zeros > 1:
                    score += self.heuristic_points[0][zeros]
                    # print(self.heuristic_points[0][zeros], end=", ")
                elif ones > 1:
                    score += self.heuristic_points[1][ones]
                    # print(self.heuristic_points[1][ones], end=", ")
        # print("|", end="")
        return score


if __name__ == "__main__":
    b = Board()
    b.columns = [[0,0,0], [1,0,1,1], [0,1], [1,0,0], [1,1], [0,1,1], [1,0,0]]
    x1 = time.time()
    mimx = MinimaxTree(4, b, 0, False)
    x2 = time.time()
    print(f"Size: {mimx.size}\t\tTime: {x2 - x1}")
    x1 = time.time()
    mimx2 = MinimaxTree(10, b, 0, True)
    x2 = time.time()
    print(f"Size: {mimx2.size}\t\tTime: {x2 - x1}")
    # print(mimx2.root.score)
    # for i in mimx2.root.children:
    #     print(i.score, end="\t")