from board import Board

b = Board()

while not b.end:
    x = int(input("Enter the piece index: "))
    b.addPiece(x)
print(b.checkWinner())