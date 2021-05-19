'''
Abstract Base Class for Data Extractor
'''

from abc import ABCMeta
from re import split
from numpy import array
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
        if move == 'None':
            return None, None
        if move[0] == 'O':
            piece = self.game.board.white_king if is_white else self.game.board.black_king
            if len(move) == 3:
                destination = (piece.location[0]+2, piece.location[1])
            else:
                destination = (piece.location[0]-2, piece.location[1])
            if piece.is_valid_move(self.game.board, destination):
                return piece.location[0]*10 + piece.location[1], destination[0]*10 + destination[1]
            else:
                print(move)
                raise Exception
        destination = (ord(move[-2])-97)*10 + int(move[-1])-1
        destination = destination//10, destination%10
        pieces = self.game.board.white_pieces if is_white else self.game.board.black_pieces
        candidates = []
        if move[0] == 'K':
            for cur_piece in pieces:
                if isinstance(cur_piece, King) \
                        and cur_piece.is_valid_move(self.game.board, destination):
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
            print(move)
            print(self.game)
            raise Exception
        elif len(candidates) == 1:
            piece = candidates[0]
        else:
            matches = 0
            for candidate in candidates:
                if not self.game.check_after_move(candidate.location, destination):
                    matches += 1
                    piece = candidate
            if matches == 1:
                return piece.location[0]*10 + piece.location[1], destination[0]*10 + destination[1]
            matches = 0
            identifier = move[1] if 'x' not in move else move[0] if move[1] == 'x' else move[1]
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
                raise Exception
        return piece.location[0]*10 + piece.location[1], destination[0]*10 + destination[1]

    def _raw_data_to_datapoint(self, line):
        datapoint = '['
        moves = eval(self._extract_moves(line))
        self.game.__init__()
        for move_pair in moves:
            for i in range(len(move_pair)):
                try:
                    source, destination = self._convert_move(move_pair[i], not(bool(i%2)))
                except Exception:
                    print(line)
                    print(moves)
                if source == None:
                    datapoint = datapoint[0:-2] + ']\n'
                    return datapoint
                print(f'{source} -> {destination}')
                print(self.game)
                if not self.game.move(source, destination):
                    print(f'{source} -> {destination}')
                    print(self.game)
                    print(f'Invalid move: {move_pair[i]}')
                    datapoint = datapoint[0:-2] + ']\n'
                    raise Exception
                print(f'{source} -> {destination}')
                print(self.game)
                datapoint += f"({source}, {destination}), "
        datapoint = datapoint[0:-2] + ']'
        return datapoint

    def _move_to_datapoint(self, move):
        from ai.data.moves import MOVES
        datapoint = [0]*142
        datapoint[MOVES[move.upper()]] = 1
        datapoint = array(datapoint)
        return datapoint

    def _board_to_datapoint(self, board, is_white):
        board_direction = range(8) if is_white else range(7, -1, -1)
        datapoint = [[board[column,row].value \
                        if board[column,row].is_white == is_white \
                        else board[column,row].value * -1 \
                    for column in range(8)] \
                    for row in board_direction]
        datapoint = array(datapoint)
        datapoint = datapoint.reshape(1, 8, 8, 1)
        return datapoint

    def _prediction_to_move(self, prediction, board, is_white):
        from ai.data.moves import MOVES
        for i, val in enumerate(prediction[0]):
            if val == max(prediction[0]):
                prediction = i
                break
        for key in MOVES:
            if MOVES[key] == prediction:
                move = key
        my_piece, ID, move_ID = move[0], int(move[1]), move[2:]
        my_piece = my_piece if is_white else my_piece.lower()
        pieces = board.white_pieces if is_white else board.black_pieces
        for piece in pieces:
            if str(piece) == str(my_piece) and piece.ID == ID:
                return piece.get_move(int(move_ID))


