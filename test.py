from board import Board

b = Board()
b.columns = [[0,0,0,1,0,0], [1,0,1,1,1,0], [0,1,0,1,0,0], [1,0,0,1,1,1], [1,1,1,0,1,1], [0,1,0,1,0,1], [1,0,0,0,0,1]]

while not b.end:
    x = input("Enter the piece index: ")
    if x == 'p': print(b.checkWinner())
    else: b.addPiece(int(x))
print(b.checkWinner())