import time
from board import Board
from collections import deque

class Node():
    def __init__(self, state: Board, parent):
        self.parent = parent
        if self.parent is not None:
            # node type: 0 for max node and 1 for min node
            self.node_type = (self.parent.node_type + 1) % 2
            self.depth = self.parent.depth + 1
            self.alpha = self.parent.alpha
            self.beta = self.parent.beta
        else:
            self.node_type = 0
            self.depth = 0
            self.alpha = float('-inf')
            self.beta = float('inf')
        if self.node_type == 0: self.score = float('-inf')
        else: self.score = float('inf')
        self.children = []
        self.state = state
        
    def addChild(self, state: Board):
        n = Node(state, self)
        self.children.append(n)
        return n

    def getPrunningValues(self):
        self.alpha = self.parent.alpha
        self.beta = self.parent.beta


class MinimaxTree():
    def __init__(self, tree_depth, board: Board, player: int, prunning: bool):
        self.root = Node(board, None)
        self.size = 1
        self.tree_depth = tree_depth
        self.player = player
        self.prunning = prunning
        self.constructTree()
        
    def calculateLeafNodeScore(self, node: Node):
        board = node.state
        points: list[int] = board.checkWinner()
        if self.player == 0: node.score = points[0] - points[1]
        else: node.score = points[1] - points[0]

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
                p = current.addChild(bcopy)
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


b = Board()
b.columns = [[0,0,0], [1,0,1,1], [0,1], [1,0,0], [1,1], [0,1,1], [1,0,0]]
# x1 = time.time()
# mimx = MinimaxTree(4, b, 0, True)
# x2 = time.time()
# print(f"Size: {mimx.size}\t\tTime: {x2 - x1}")
x1 = time.time()
mimx2 = MinimaxTree(1, b, 0, True)
x2 = time.time()
print(f"Size: {mimx2.size}\t\tTime: {x2 - x1}")
print(mimx2.root.score)
for i in mimx2.root.children:
    print(i.score, end="\t")