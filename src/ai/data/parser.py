'''
Abstract Base Class for Data Extractor
'''

from abc import ABCMeta
from re import split
from backend.pieces.king import King
from backend.pieces.queen import Queen
from backend.pieces.rook import Rook
from backend.pieces.knight import Knight
from backend.pieces.bishop import Bishop
from backend.pieces.pawn import Pawn



class Parser(metaclass=ABCMeta):
    def __init__(self, game):
        self.game = game

    def _extract_moves(self, line):
        game = split('[\d]+\.\s', line)
        datapoint = '['
        for it in range (1, len(game) - 1):
            move = game[it].split('{')
            if len(move) > 1:
                white_move = split('[\?!#\+=]', move[0][0:-1])[0]
                black_move = split('[\?!#\+=]', move[-2].split()[-1])[0]
            else:
                white_move = split('[\?!#\+=]', move[0].split()[0])[0]
                black_move = split('[\?!#\+=]', move[0].split()[1])[0]
            datapoint += f"('{white_move}', '{black_move}'), "
        move = game[-1].split('{')
        if len(move) > 1:
            white_move = split('[\?!#\+=]', move[0][0:-1])[0]
            black_move = split('[\?!#\+=]', move[-2].split()[-1])[0]
        else:
            white_move = split('[\?!#\+=]', move[0].split()[0])[0]
            black_move = split('[\?!#\+=]', move[0].split()[1])[0]
        if white_move == black_move:
            black_move = 'None'
        elif '*' in black_move or '1-0' in black_move:
            black_move = 'None'
        elif '1/2' in black_move:
            black_move = 'Draw'
        elif '0-1' in black_move:
            white_move = 'None'
            black_move = 'None'
        if not white_move == 'None':
            datapoint += f"('{white_move}', '{black_move}'), "
        return datapoint[0:-2] + ']\n'

    def _convert_move(self, move, is_white):
        if move[0] == 'O':
            piece = self.game.board.white_king if is_white else self.game.board.black_king
            if len(move) == 3:
                destination = (piece.location[0]+2, piece.location[1])
            else:
                destination = (piece.location[0]-3, piece.location[1])
            if piece.is_valid_move(self.game.board, destination):
                return piece.location[0]*10 + piece.location[1], destination[0]*10 + destination[1]
            else:
                raise Exception

        destination = (ord(move[-2])-97)*10 + int(move[-1])-1
        destination = destination//10, destination%10
        pieces = self.game.board.white_pieces if is_white else self.game.board.black_pieces
        candidates = []

        if move[0] == 'K':
            for cur_piece in pieces:
                if isinstance(cur_piece, King):
                    candidates.append(cur_piece)
                    break
        elif move[0] == 'Q':
            for cur_piece in pieces:
                if isinstance(cur_piece, Queen) \
                        and cur_piece.is_valid_move(self.game.board, destination):
                    candidates.append(cur_piece)
        elif move[0] == 'R':
            for cur_piece in pieces:
                if isinstance(cur_piece, Rook) \
                        and cur_piece.is_valid_move(self.game.board, destination):
                    candidates.append(cur_piece)
        elif move[0] == 'N':
            for cur_piece in pieces:
                if isinstance(cur_piece, Knight) \
                        and cur_piece.is_valid_move(self.game.board, destination):
                    candidates.append(cur_piece)
        elif move[0] == 'B':
            for cur_piece in pieces:
                if isinstance(cur_piece, Bishop) \
                        and cur_piece.is_valid_move(self.game.board, destination):
                    candidates.append(cur_piece)
        else:
            for cur_piece in pieces:
                if isinstance(cur_piece, Pawn) \
                        and cur_piece.is_valid_move(self.game.board, destination):
                    candidates.append(cur_piece)
        if len(candidates) == 0:
            print(self.game)
            print(move)
            raise Exception
        elif len(candidates) == 1:
            piece = candidates[0]
        else:
            identifier = move[1]
            matches = 0
            if ord(identifier) >= 97:
                for candidate in candidates:
                    if candidate.location[0] == ord(identifier)-97:
                        piece = candidate
                        matches += 1
            else:
                for candidate in candidates:
                    if candidate.location[1] == int(identifier)-1:
                        piece = candidate
                        matches += 1
            if matches == 0 or matches > 1:
                print(f'move was: {move}')
                raise Exception
        return piece.location[0]*10 + piece.location[1], destination[0]*10 + destination[1]

    def _raw_data_to_datapoint(self, line):
        datapoint = '['
        moves = eval(self._extract_moves(line))
        self.game.__init__()
        from time import sleep
        for move in moves:
            white_move, black_move = move
            white_source, white_destination = self._convert_move(white_move, True)
            if not self.game.move(white_source, white_destination):
                print(self.game)
                print(f'Invalid move: {white_move}')
                raise Exception
            black_source, black_destination = self._convert_move(black_move, False)
            print(self.game.board)
            sleep(0.3)
            if not self.game.move(black_source, black_destination):
                print(self.game)
                print(f'Invalid move: {black_move}')
                raise Exception
            print(self.game.board)
            sleep(0.3)
            datapoint += f"(({white_source}, {white_destination}), ({black_source}, {black_destination})), "
        datapoint = datapoint[0:-2] + ']\n'
        return datapoint

    def move_to_datapoint(self, move):
        pass

    def _board_to_datapoint(self, board, is_white):
        if is_white:
            datapoint = [[board[column,row].value \
                        if board[column,row].is_white == is_white \
                        else board[column,row].value * -1 \
                    for column in range(8)] \
                    for row in range(8)]
        else:
            datapoint = [[board[column,row].value \
                        if board[column,row].is_white == is_white \
                        else board[column,row].value * -1 \
                    for column in range(8)] \
                    for row in range(7, -1, -1)]
        datapoint = array(datapoint)
        datapoint = datapoint.reshape(1, 8, 8, 1)
        return datapoint

    def _prediction_to_move(self, prediction):
        '''
        APART OF USING AI
        '''
        return prediction

    def _generate_datapoint(self, moves, iter=[0]):
        '''
        APART OF TRAINING
        THIS FUNCTION SHOULD DO THE load_dataset() in the cNN tutorial
        Map list of moves into: (np.array(shape=(X,8,8,1), np.array(X, 124,1))
        '''
        moves = eval(moves)
        test_data_x_0 = [[5, 3, 3, 9, 100, 3, 3, 5],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [-1, -1, -1, -1, -1, -1, -1, -1],
                [-5, -3, -3, -9, -100, -3, -3, -5]]
        test_data_y_0 = [0] * 124
        test_data_y_0[9] = 1
        test_data_x_1 = [[5, 3, 3, 9, 100, 3, 3, 5],
                [1, 1, 1, 1, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, -1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [-1, -1, -1, 0, -1, -1, -1, -1],
                [-5, -3, -3, -9, -100, -3, -3, -5]]
        test_data_y_1 = [0] * 124
        test_data_y_1[47] = 1
        test_data_x_2 = [[5, 3, 3, 9, 100, 3, 3, 5],
                [1, 1, 1, 1, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, -1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [-1, -1, -1, 0, -1, -1, -1, -1],
                [-5, -3, -3, -9, -100, -3, -3, -5]]
        test_data_y_2 = [0] * 124
        test_data_y_2[9] = 1
        test_data_x_3 = [[5, 0, 3, 9, 100, 3, 3, 5],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 3, 0, 0, 0, 0, 0],
                [0, 0, 0, -1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [-1, -1, 0, -1, -1, -1, -1, -1],
                [-5, -3, -3, -9, -100, -3, -3, -5]]
        test_data_y_3 = [0] * 124
        test_data_y_3[46] = 1
        ret_val = ([test_data_x_0, test_data_x_1], [test_data_y_0,
            test_data_y_1])
        if iter[0] % 2 == 0:
            ret_val = ([test_data_x_2, test_data_x_3], [test_data_y_2, test_data_y_3])
        iter[0] += 1
        return ret_val

