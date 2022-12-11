class Board():
    def __init__(self) -> None:
        self.columns = [[],[],[],[],[],[],[]]
        self.turn = 0
        self.end = False
        self.players = {0: 0, 1: 0}


    def generatePossibleMoves(self) -> list[int]:
        return [i for i in range(0,7) if len(self.columns[i]) < 6]

    def addPiece(self, column_num) -> bool:
        if column_num < 0 or column_num > 6 or not isinstance(column_num, int) or \
            column_num not in self.generatePossibleMoves():
            return None
        if self.turn == 0: self.columns[column_num].append(0)
        if self.turn == 1: self.columns[column_num].append(1)
        return self.switchTurn()

    def switchTurn(self) -> bool:
        for i in self.columns:
            if len(i) < 6:
                self.turn = (self.turn + 1) % 2
                return True
        self.end = True
        return False

    def copy(self):
        columns = [column.copy() for column in self.columns]
        b = Board()
        b.columns = columns
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
        rows = list(zip(*c))
        for row in rows:
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
        columns = [i.copy() for i in self.columns]
        for column in columns:
            if len(column) < 6:
                x = len(column)
                for i in range(0, 6 - x):
                    column.append(2)

        # self.printBoard()
        self.players[0], self.players[1] = 0, 0  
        self.checkColumnPoints(columns)
        self.checkRowPoints(columns)
        self.checkDiagonalPoints(columns)
        return [self.players[0], self.players[1]]

    def printBoard(self):
        columns = [i.copy() for i in self.columns]
        for column in columns:
            if len(column) < 6:
                x = len(column)
                for i in range(0, 6 - x):
                    column.append(2)

        y = list(zip(*columns))
        y.reverse()
        for i in y:
            print(i)
