from Board import Board

board = Board()
board.setBoard({'white': {4: 2, 3: 2, 5: 3, 1: 6, 2: 2},
                'black': {13: 4, 8: 3, 6: 4, 7: 2, 25: 1, 19: 1}})
b = board.getBoard()
b['white'] = {0: 14, 6: 1}
board.setBoard(b)
print(board.getMoves((5, 5), 'white'))
