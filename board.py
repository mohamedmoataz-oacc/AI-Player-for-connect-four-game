class Board():
    def __init__(self) -> None:
        self.columns = [[],[],[],[],[],[],[]] # The columns of the board
        self.rows = []
        self.pieces_in_columns = [0,0,0,0,0,0,0]
        self.turn = 0 # The player who has the turn
        self.end = False # To know if the game ended
        self.players = {0: 0, 1: 0} # The points of each player

    def generatePossibleMoves(self) -> list[int]:
        """
        A method that generates all the possible moves.
        Returns: a list of integers.
        """
        return [i for i in range(0,7) if len(self.columns[i]) < 6]

    def addPiece(self, column_num):
        """
        Adds a piece to the board if the board was not full.
        """
        if column_num < 0 or column_num > 6 or not isinstance(column_num, int) or \
            column_num not in self.generatePossibleMoves():
            return None
        
        x = self.pieces_in_columns[column_num]
        if x + 1 == max(self.pieces_in_columns) + 1:
            self.rows.append([2,2,2,2,2,2,2])
        
        self.columns[column_num].append(self.turn)
        self.rows[self.pieces_in_columns[column_num]][column_num] = self.turn
        self.pieces_in_columns[column_num] += 1
        self.switchTurn()

    def switchTurn(self):
        """
        Switches the turn between players.
        """
        for i in self.columns:
            if len(i) < 6:
                self.turn = (self.turn + 1) % 2
                return True
        self.end = True

    def copy(self):
        """
        Used to make a copy of the board.
        """
        columns = [column.copy() for column in self.columns]
        rows = [row.copy() for row in self.rows]
        pieces = self.pieces_in_columns.copy()
        b = Board()
        b.columns = columns
        b.rows = rows
        b.pieces_in_columns = pieces
        b.turn = self.turn
        b.end = self.end
        b.players = self.players.copy()
        return b

    def checkColumnPoints(self, c):
        for column in c:
            number = column[0]
            counter = 1
            for i in range(1,6):
                if column[i] == 2: break
                if column[i] == number:
                    counter += 1
                else:
                    number = column[i]
                    counter = 1
                if counter >= 4:
                    if number != 2:
                        self.players[number] += 1
                        # print(f"P{number} point from column starting at ({c.index(column)}, {i-3}) and ending at ({c.index(column)}, {i})")

    def checkRowPoints(self, c):
        for row in self.rows:
            number = row[0]
            counter = 1
            for i in range(1,7):
                if row[i] == number:
                    counter += 1
                else:
                    number = row[i]
                    counter = 1
                if counter >= 4:
                    if number != 2:
                        self.players[number] += 1
                        # print(f"P{number} point from row starting at ({rows.index(row)}, {i-3}) and ending at ({rows.index(row)}, {i})")

    def checkDiagonalPoints(self, c):
        for index in range(0, 4):
            column = c[index]
            for i in range(0, 3):
                if column[i] == c[index + 1][i + 1] and column[i] == c[index + 2][i + 2] \
                    and column[i] == c[index + 3][i + 3]:
                    if column[i] != 2:
                        self.players[column[i]] += 1
                        # print(f"P{column[i]} point from backward diagonal starting at (c{index}, r{i}) and ending at (c{index+3}, r{i+3})")
            for i in range(3, 6):
                if column[i] == c[index + 1][i - 1] and column[i] == c[index + 2][i - 2] \
                    and column[i] == c[index + 3][i - 3]:
                    if column[i] != 2:
                        self.players[column[i]] += 1
                        # print(f"P{column[i]} point from forward diagonal starting at (c{index}, r{i}) and ending at (c{index+3}, r{i-3})")

    def checkWinner(self) -> list[int]:
        """
        Checks the points of every player.
        """
        columns = [i.copy() for i in self.columns]

        # self.printBoard()
        self.players[0], self.players[1] = 0, 0  
        self.checkColumnPoints(columns)
        self.checkRowPoints(columns)
        self.checkDiagonalPoints(columns)
        return [self.players[0], self.players[1]]

    def printBoard(self):
        y = [row.copy() for row in self.rows]
        y.reverse()
        for i in y:
            print(i)

if __name__ == "__main__":
    b = Board()
    b.addPiece(3)
    b.addPiece(2)
    b.addPiece(4)
    b.addPiece(5)
    b.addPiece(3)
    b.addPiece(4)
    b.addPiece(1)
    b.printBoard()