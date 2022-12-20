from board import Board
from minimaxTree import MinimaxTree

class Connect4AIPlayer():
    def __init__(self, k: int, prunning: bool, player: int) -> None:
        self.k = k
        self.prunning = prunning
        self.player = player
        self.last_turn_state = None

    def decision(self, state: Board):
        tree = MinimaxTree(self.k, state, self.player, self.prunning, False)
        self.last_turn_state = state
        return [tree.root.move, round(tree.time, 2), tree.size]
        