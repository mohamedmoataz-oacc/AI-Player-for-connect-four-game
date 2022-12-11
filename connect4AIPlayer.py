from board import Board
from minimaxTree import MinimaxTree

class Connect4AIPlayer():
    def __init__(self, k: int, prunning: bool, player: int) -> None:
        self.k = k
        self.prunning = prunning
        self.player = player

    def decision(self, state: Board):
        tree = MinimaxTree(self.k, state, self.player, self.prunning)
        score = tree.root.score
        children = tree.root.children
        move = 0
        for i in children:
            if i.score == score:
                move = i.move
                break
        return move
        