from board import Board


if __name__ == '__main__':
    board = Board('testWhite', 'testBlack')

    white_turn = True
    while board.has_kings():
        print(board)
        # Command format = <Origin> <Destination>
        # Origin = Destination = <Letter><Number>
        if white_turn:
            move = input('Enter white move: ')
        else:
            move = input('Enter black move: ')
        origin = move.split(' ')[0]
        origin_x, origin_y = ord(origin[0]) - 65, int(origin[1]) - 1
        destination = move.split(' ')[1]
        destination_x, destination_y= ord(destination[0]) - 65, int(destination[1]) - 1
        piece = board.board[origin_x][origin_y]
        if ((white_turn and piece.is_white) or (not(white_turn) and not(piece.is_white))) and piece.is_valid_move(board, destination):
            board.move(piece, (destination_x, destination_y))
            white_turn = not(white_turn)
        else:
            print('invalid move, please enter a valid move')

    print('game over')