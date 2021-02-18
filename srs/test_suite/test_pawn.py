from board import Board


moves = {'vertical_double':['A2 A4', 'A7 A5', 'A4 A5'],
         'vertical_single':['A2 A3', 'D7 D6', 'B2 B3', 'E7 E6'],
         'capture':['B2 B4', 'C7 C5', 'B4 C5'],
         'passant':['C2 C4', 'H7 H6','C4 C5', 'D7 D5', 'C5 D6']
}
         

def test_pawn_moves(name, moves):
    board = Board('testWhite', 'testBlack')
    print(f'\n\nTEST FOR {name}\n\n')

    white_turn = True
    for move in moves:
        print(board)
        print('\n')

        print(f'{"White turn" if white_turn else "Black turn"}')
        print(f'Executing move: {move}')
        # Parse the move
        origin = move.split(' ')[0]
        origin_x, origin_y = ord(origin[0]) - 65, int(origin[1]) - 1
        destination = move.split(' ')[1]
        destination_x, destination_y= ord(destination[0]) - 65, int(destination[1]) - 1

        # Execute the move
        piece = board.board[origin_x][origin_y]
        if ((white_turn and piece.is_white) or (not(white_turn) and not(piece.is_white))) and piece.is_valid_move(board, (destination_x, destination_y)):
            board.move(piece, (destination_x, destination_y))
            white_turn = not(white_turn)
        else:
            print('invalid move, please enter a valid move')
    print(board)

    
def test_pawn():
    for move in moves:
        test_pawn_moves(move, moves[move])

