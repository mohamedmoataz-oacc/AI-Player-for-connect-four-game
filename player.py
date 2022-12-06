class Player:
    def __init__(self) -> None:
        self.points = 0

    def addPoint(self):
        self.points += 1

    def getTotalPoints(self):
        return self.points