import time
from board import Board
from collections import deque
from multiprocessing import Process, Queue

class Node():
    def __init__(self, state: Board, parent):
        self.parent = parent # A node object refering this nodes parent.
        if self.parent is not None:
            # node type: 0 for max node and 1 for min node
            self.node_type: int = (self.parent.node_type + 1) % 2
            self.depth: int = self.parent.depth + 1
            self.move: int = None # The move to reach the board state that is stored in this node.
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
    def __init__(self, tree_depth, board: Board, player: int, prunning: bool, tree: bool = True):
        self.root: Node = Node(board, None)
        self.size: int = 1
        self.psize_q = Queue()
        self.psize_q.put({'size': 1})
        self.tree_depth: int = tree_depth # maximum depth for the tree
        self.player: int = player # which player is the ai (0 or 1)
        self.prunning: bool = prunning
        self.heuristic_points: dict = {
            self.player: {2: 20, 3: 30, 4: 105},
            (self.player + 1) % 2: {2: -25, 3: -35, 4: -100}
        }
        self.time = dict()
        self.num = 1
        self.tree = tree
        self.q = Queue()
        x1 = time.time()
        self.constructTree()
        x2 = time.time()
        self.time = x2 - x1

    def timer(func):
        def timed(*args):
            t1 = time.time()
            x = func(*args)
            t2 = time.time()
            if args[0].time.get(func.__name__) is None: args[0].time[func.__name__] = 0
            args[0].time[func.__name__] += t2 - t1
            return x
        return timed
        
    def calculateLeafNodeScore(self, node: Node):
        """
        Calculates a leaf node's score, alpha and beta values.
        """
        board = node.state
        columns = [i.copy() for i in board.columns]
        for column in columns:
            if len(column) < 6:
                x = len(column)
                for i in range(0, 6 - x):
                    column.append(2)
                    
        # print(self.num, ":", end = " ")
        node.score = self.getColumnHeurstic(board.columns)
        node.score += self.getRowHeurstic(board.rows)
        node.score += self.getDiagonalHeurstic(columns)
        self.num += 1
        # print("")

        if self.prunning:
            if node.node_type == 0: node.alpha = node.score
            elif node.parent.node_type == 1:  node.beta = node.score
        
    def threadIt(self, node: Node):
        size = 1
        stack = deque()
        stack.append(node)
        current: Node = None # the node containing the board state we are currently generating its children.

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
                if not self.tree: size += 1
                if p.depth < self.tree_depth and not bcopy.end: stack.append(p)
                elif p.depth == self.tree_depth or bcopy.end:
                    self.calculateLeafNodeScore(p)
                    # After calculating the score of the leaf node, we pass its score to its parent
                    self.passScore(p)
                    # If we are using alpha beta prunning and we find that alpha > beta,
                    # we stop adding children.
                    if self.prunning and current.alpha > current.beta: break

            if stack:
                # To view the element at the top of the stack without removing it
                t = stack.pop()
                stack.append(t)
            
                # if the node we are going to explore next has a depth less than or equals the node we just
                # explored, we pass the score of the node we just explored to its parent node.
                if t.depth <= current.depth:
                    diff = (current.depth - t.depth) + 1
                    for i in range(diff):
                        self.passScore(current)
                        current = current.parent
             
        # After we get out of the loop, the score of the parent of the last child node should be passed 
        # until it reaches the root node.
        while current.parent is not None:
            self.passScore(current)
            current = current.parent
        self.q.put((node.score, node.move))

    def constructTree(self):
        """
        Constructs the minimax tree using preorder tree traversal.
        """
        scores = []
        if self.tree:
            self.threadIt(self.root)
        elif self.tree_depth == 1:
            self.threadIt(self.root)
            for child in self.root.children:
                if child.score == self.root.score:
                    self.root.move = child.move
                    break
        else:
            moves = self.root.state.generatePossibleMoves()
            if len(moves) == 1:
                self.root.move = moves[0]
                return
            ts = []
            for move in moves:
                bcopy = self.root.state.copy()
                bcopy.addPiece(move)
                p = self.root.addChild(bcopy, move)
                t = Process(target = self.threadIt, args = (p,))
                t.start()
                ts.append(t)
            for t in ts:
                t.join()
            moves = []
            while not self.q.empty():
                s = self.q.get()
                scores.append(s[0])
                moves.append(s[1])
            self.size = self.psize_q.get()['size']
            self.root.score = max(scores)
            for i in range(len(scores)):
                if scores[i] == self.root.score:
                    self.root.move = moves[i]
                    break

    def passScore(self, node):
        if node.parent.node_type == 0:
            if node.score > node.parent.score:
                node.parent.score = node.score
                if self.prunning and node.beta > node.parent.alpha: node.parent.alpha = node.beta
        elif node.parent.node_type == 1:
            if node.score < node.parent.score:
                node.parent.score = node.score
                if self.prunning and node.alpha < node.parent.beta: node.parent.beta = node.alpha

    def checkWindow(self, window):
        zeros = window.count(0)
        ones = window.count(1)

        if zeros != 0 and ones != 0: return 0
        elif zeros > 1:
            # print(self.heuristic_points[0][zeros], end=", ")
            return self.heuristic_points[0][zeros]
        elif ones > 1:
            # print(self.heuristic_points[1][ones], end=", ")
            return self.heuristic_points[1][ones]
        else: return 0

    @timer
    def getColumnHeurstic(self, columns):
        score = 0
        y = 0
        for column in columns:
            y += 1
            if len(column) >= 4: x = 7
            else: x = len(column) + 3

            for i in range(4, x):
                numbers = column[i-4:i]
                score += self.checkWindow(numbers)
        # print("|", end="")
        return score

    @timer
    def getRowHeurstic(self, rows):
        score = 0
        x = 0
        for row in rows:
            x+=1
            for i in range(4,8):
                numbers = row[i-4:i]
                score += self.checkWindow(numbers)
        # print("|", end="")
        return score

    @timer
    def getDiagonalHeurstic(self, columns):
        score = 0
        for index in range(0, 4):
            for i in range(0, 3):
                window = [columns[index + j][i + j] for j in range(0, 4)]
                score += self.checkWindow(window)
        # print("|", end="")

        for index in range(6, 2, -1):
            for i in range(0, 3):
                window = [columns[index - j][i + j] for j in range(0, 4)]
                score += self.checkWindow(window)
        # print("|", end="")
        return score


if __name__ == "__main__":
    b = Board()
    b.columns = [[0,0,0], [1,0,1,1], [0,1], [1,0,0], [1,1], [0,1,1], [1,0,0]]
    b.rows = [[0,1,0,1,1,0,1], [0,0,1,0,1,1,0], [0,1,2,0,2,1,0], [2,1,2,2,2,2,2], [2,2,2,2,2,2,2], [2,2,2,2,2,2,2]]
    b.pieces_in_columns = [3,4,2,3,2,3,3]
    # b.turn = 1
    x1 = time.time()
    mimx = MinimaxTree(6, b, 1, True)
    x2 = time.time()
    print(f"Size: {mimx.size}\t\tTime: {x2 - x1}")
    print("")
    print(f"Root score: {mimx.root.score}")
    # b.printBoard()
    # for key, value in mimx.time.items():
    #     print(f"{key} total time: {round(value, 3)}")