from player import Player

class Board():
    def __init__(self) -> None:
        self.columns = [[],[],[],[],[],[],[]]
        self.turn = 0
        self.end = False
        self.players = {0: Player(), 1: Player()}

    def generatePossibleMoves(self) -> list[int]:
        return [i for i in range(0,7) if len(self.columns[i]) < 6]

    def addPiece(self, column_num) -> bool:
        if column_num < 0 or column_num > 6 or not isinstance(column_num, int) or \
            column_num not in self.generatePossibleMoves():
            return None
        if self.turn == 0: self.columns[column_num].append(0)
        if self.turn == 1: self.columns[column_num].append(1)
        self.printBoard()
        return self.switchTurn()

    def switchTurn(self) -> bool:
        for i in self.columns:
            if len(i) < 6:
                self.turn = (self.turn + 1) % 2
                return True
        self.end = True
        return False

    def checkColumnPoints(self, c):
        for column in c:
            number = column[0]
            counter = 1
            for i in range(1,6):
                if counter >= 4:
                    if number != 2:
                        self.players[number].addPoint()
                        print(f"P{number} point from column")
                if column[i] == number:
                    counter += 1
                else:
                    number = column[i]
                    counter = 1

    def checkRowPoints(self, c):
        rows = zip(*c)
        for row in rows:
            number = row[0]
            counter = 1
            for i in range(1,7):
                if counter >= 4:
                    if number != 2:
                        self.players[number].addPoint()
                        print(f"P{number} point from row")
                if row[i] == number:
                    counter += 1
                else:
                    number = row[i]
                    counter = 1

    def checkDiagonalPoints(self, c):
        for index in range(0, 4):
            column = c[index]
            for i in range(0, 3):
                if column[i] == c[index + 1][i + 1] and column[i] == c[index + 2][i + 2] \
                    and column[i] == c[index + 3][i + 3]:
                    if column[i] != 2:
                        self.players[column[i]].addPoint()
                        print(f"P{column[i]} point from backward diagonal")
            for i in range(3, 6):
                if column[i] == c[index + 1][i - 1] and column[i] == c[index + 2][i - 2] \
                    and column[i] == c[index + 3][i - 3]:
                    if column[i] != 2:
                        self.players[column[i]].addPoint()
                        print(f"P{column[i]} point from forward diagonal")

    def checkWinner(self) -> list[int]:
        columns = [i.copy() for i in self.columns]
        for column in columns:
            if len(column) < 6:
                x = len(column)
                for i in range(0, 6 - x):
                    column.append(2)

        self.players[0].points, self.players[1].points = 0, 0  
        self.checkColumnPoints(columns)
        self.checkRowPoints(columns)
        self.checkDiagonalPoints(columns)
        return [self.players[0].getTotalPoints(), self.players[1].getTotalPoints()]

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
