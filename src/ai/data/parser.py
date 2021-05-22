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
                raise Exception
        destination = (ord(move[-2])-97)*10 + int(move[-1])-1
        destination = destination//10, destination%10
        pieces = self.game.board.white_pieces if is_white else self.game.board.black_pieces
        candidates = []
        if move[0] == 'K':
            for cur_piece in pieces:
                if isinstance(cur_piece, King) \
                        and cur_piece.is_valid_move(self.game.board, destination) \
                        and not self.game.check_after_move(cur_piece.location, destination):
                    candidates.append(cur_piece)
                    break
        elif move[0] == 'Q':
            for cur_piece in pieces:
                if isinstance(cur_piece, Queen) \
                        and cur_piece.is_valid_move(self.game.board, destination) \
                        and not self.game.check_after_move(cur_piece.location, destination):
                    candidates.append(cur_piece)
        elif move[0] == 'R':
            for cur_piece in pieces:
                if isinstance(cur_piece, Rook) \
                        and cur_piece.is_valid_move(self.game.board, destination) \
                        and not self.game.check_after_move(cur_piece.location, destination):
                    candidates.append(cur_piece)
        elif move[0] == 'N':
            for cur_piece in pieces:
                if isinstance(cur_piece, Knight) \
                        and cur_piece.is_valid_move(self.game.board, destination) \
                        and not self.game.check_after_move(cur_piece.location, destination):
                    candidates.append(cur_piece)
        elif move[0] == 'B':
            for cur_piece in pieces:
                if isinstance(cur_piece, Bishop) \
                        and cur_piece.is_valid_move(self.game.board, destination) \
                        and not self.game.check_after_move(cur_piece.location, destination):
                    candidates.append(cur_piece)
        else:
            for cur_piece in pieces:
                if isinstance(cur_piece, Pawn) \
                        and cur_piece.is_valid_move(self.game.board, destination) \
                        and not self.game.check_after_move(cur_piece.location, destination):
                    candidates.append(cur_piece)
        if len(candidates) == 0:
            return None, None
        elif len(candidates) == 1:
            piece = candidates[0]
        else:
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
                source, destination = self._convert_move(move_pair[i], not(bool(i%2)))
                if source == None or not self.game.move(source, destination):
                    datapoint = datapoint[0:-2] + ']\n'
                    return datapoint
                datapoint += f"({source}, {destination}), "
        datapoint = datapoint[0:-2] + ']'
        return datapoint

    def _move_to_datapoint(self, board, is_white, move):
        from ai.data.moves import MOVES
        datapoint = [0]*142
        from copy import deepcopy
        my_pieces = board.white_pieces if is_white else board.black_pieces
        their_pieces = board.white_pieces if not is_white else board.black_pieces
        for piece in my_pieces:
            piece_name = str(piece).upper()
            piece_ID = piece.ID if piece_name != 'Q' else 1
            moves = piece.move_IDs
            for piece_move in moves:
                temp_board = deepcopy(board)
                real_piece = temp_board[piece.location]
                move_coord = piece.move_IDs[piece_move](piece.location)
                key = piece_name + str(piece_ID) + str(piece_move)
                destination = (move_coord//10, move_coord%10)
                board_value = None
                if key == move:
                    continue
                if destination[0] >= 0 \
                    and destination[0] <= 7 \
                    and destination[1] >= 0 \
                    and destination[1] <= 7 \
                    and real_piece.is_valid_move(temp_board, destination):
                        temp_board.move(real_piece, destination)
                        board_value = temp_board.board_value()
                else:
                    board_value = 0
                board_value *= 1 if is_white else -1
                datapoint[MOVES[key]] = board_value
        min_loss = min(datapoint)
        max_loss = max(datapoint) + 0.05
        if min_loss < 0:
            for i in range(len(datapoint)):
                if datapoint[i] != 0 and i != MOVES[move.upper()]:
                    datapoint[i] += abs(min_loss)
        elif min_loss > 0:
            for i in range(len(datapoint)):
                if datapoint[i] != 0 and i != MOVES[move.upper()]:
                    datapoint[i] -= min_loss
        if max_loss < 0 and min_loss < 0:
            max_loss = abs(min_loss) - abs(max_loss)
        elif max_loss > 0 and min_loss > 0:
            max_loss = max_loss - min_loss
        else:
            max_loss += abs(min_loss)
        for i in range(len(datapoint)):
            if datapoint[i] != 0 and i != MOVES[move.upper()]:
                datapoint[i] /= max_loss
                datapoint[i] = round(datapoint[i], 4)
        datapoint[MOVES[move.upper()]] = 1.0
        '''
        datapoint = array(datapoint)
        '''
        return datapoint

    def _board_to_datapoint(self, board, is_white):
        piece_mapping = {'P': 1.0, 'B': 3.02, 'N' : 3.01, 'R': 5.0, 'Q': 9.0, 'K': 100.0}
        board_direction = range(8) if is_white else range(7, -1, -1)
        datapoint = [[None] * 8] * 8
        for row in board_direction:
            for column in range(8):
                if board[row,column].is_white == None:
                    datapoint[column][row] = 0
                elif board[row,column].is_white == is_white:
                    datapoint[column][row] = \
                            piece_mapping[str(board[row,column]).upper()] + board[row,column].ID/10
                else:
                    datapoint[column][row] = \
                        (piece_mapping[str(board[row,column]).upper()] + board[row,column].ID/10) * -1
        '''
        datapoint = array(datapoint)
        datapoint = datapoint.reshape(1, 8, 8, 1)
        '''
        return datapoint

    def _datapoint_to_board(self, datapoint):
        piece_mapping = {1 : 'P', -1: 'p', 3.2: 'B', -3.2: 'b', 3.1: 'N', -3.1:
                'n', 5: 'R', -5: 'r', 9: 'Q', -9: 'q', 100: 'K', -100: 'k'}
        from backend.board import Board
        white_pieces = set()
        black_pieces = set()
        for row in range(len(datapoint)):
            for column in range(len(datapoint)):
                if datapoint[column][row][0] == '1':
                    white_pieces.add(Pawn(True, (row, column)))
                if datapoint[column][row][0] == '2':
                    white_pieces.add(Bishop(True, (row, column)))
                if datapoint[column][row][0] == '3':
                    white_pieces.add(Knight(True, (row, column)))
                if datapoint[column][row][0] == '4':
                    white_pieces.add(Rook(True, (row, column)))
                if datapoint[column][row][0] == '5':
                    white_pieces.add(Queen(True, (row, column)))
                if datapoint[column][row][0] == '6':
                    white_pieces.add(King(True, (row, column)))
                if datapoint[column][row][0] == '-1':
                    white_pieces.add(Pawn(False, (row, column)))
                if datapoint[column][row][0] == '-2':
                    white_pieces.add(Bishop(False, (row, column)))
                if datapoint[column][row][0] == '-3':
                    white_pieces.add(Knight(False, (row, column)))
                if datapoint[column][row][0] == '-4':
                    white_pieces.add(Rook(False, (row, column)))
                if datapoint[column][row][0] == '-5':
                    white_pieces.add(Queen(False, (row, column)))
                if datapoint[column][row][0] == '-6':
                    white_pieces.add(King(False, (row, column)))
        return Board(white_pieces | black_pieces)

    def _prediction_to_move(self, prediction, board, is_white):
        print(max(prediction[0]))
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


