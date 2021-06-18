'''
Abstract Base Class for Data Extractor
'''

from re import split
from ai.models.base_model import BaseModel



class Parser(BaseModel):
    def __init__(self, game, location, logger):
        super().__init__(game, location, logger)


    def _raw_data_to_datapoint(self, line):
        datapoint = ''
        moves = eval(self._extract_moves(line))
        self.game.__init__()
        for move_pair in moves:
            if move_pair[0] == 'Win' \
                    or move_pair[0] == 'Draw' \
                    or move_pair[0] == 'Lose':
                datapoint = '[' + datapoint[0:-2] + ']\n'
                return datapoint
            for i in range(2):
                source, destination = self._convert_move(move_pair[i], not(bool(i)))
                if source == None or not self.game.move(source, destination):
                    datapoint = '[' + datapoint[0:-2] + ']\n'
                    return datapoint
                datapoint += f"({source}, {destination}), "
        datapoint = '[' + datapoint[0:-2] + ']\n'
        return datapoint


    def _generate_datapoint(self, moves):
        from copy import copy
        self.game.__init__()
        x_vector, y_vector = [], []
        moves = eval(moves)
        for source, destination in moves:
            x = copy(self.game.board)
            self.game.move(source, destination)
            y = (source, destination)
            x_vector.append(x)
            y_vector.append(y)
        return (x_vector, y_vector)


    def _extract_moves(self, line):
        game = split('[\d]+\.\s', line)
        datapoint = ''
        for it in range (1, len(game)):
            move = game[it].split('{')
            if len(move) > 1:
                white_move = split('[\?!#\+=]', move[0][0:-1])[0]
                black_move = split('[\?!#\+=]', move[-2].split()[-1])[0]
            else:
                white_move = split('[\?!#\+=]', move[0].split()[0])[0]
                black_move = split('[\?!#\+=]', move[0].split()[1])[0]
            datapoint += f"('{white_move}', '{black_move}'), " \
                    if it != len(game) - 1 else ""
        if white_move == black_move or '*' in black_move or '1-0' in black_move:
            white_move = 'Win'
            black_move = 'Lose'
        elif '1/2' in black_move:
            white_move = black_move = 'Draw'
        elif '0-1' in black_move:
            white_move = 'Lose'
            black_move = 'Win'
        datapoint += f"('{white_move}', '{black_move}')"
        return '[' + datapoint + ']\n'


    def _convert_move(self, move, is_white):
        if move[0] == 'O':
            piece = self.game.board.white_king if is_white else self.game.board.black_king
            destination = (piece.location[0]+2, piece.location[1]) \
                    if len(move) == 3 else (piece.location[0]-2, piece.location[1])
            return piece.location[0]*10 + piece.location[1], destination[0]*10 + destination[1]
        destination = (ord(move[-2])-97)*10 + int(move[-1])-1
        destination = destination//10, destination%10
        pieces = self.game.board.white_pieces if is_white else self.game.board.black_pieces
        candidates = []
        for cur_piece in pieces:
            ID = str(cur_piece).upper()
            if self.game.board.is_valid_move(cur_piece, destination) \
                    and ((move[0] == 'K' and ID == 'K') \
                    or (move[0] == 'Q' and ID == 'Q') \
                    or (move[0] == 'R' and ID == 'R') \
                    or (move[0] == 'N' and ID == 'N') \
                    or (move[0] == 'B' and ID == 'B') \
                    or (move[0] not in {'K', 'Q', 'R', 'N', 'B'} \
                    and ID == 'P')):
                candidates.append(cur_piece)
        piece = None
        if len(candidates) == 0:
            self.logger.warning(\
                f'Move was invalid.\n{self.game.board}\nMove: {is_white} - {move}\n')
            return None, None
        elif len(candidates) == 1:
            piece = candidates[0]
        else:
            identifier = move[1] if 'x' not in move else move[0] if move[1] == 'x' else move[1]
            for candidate in candidates:
                if (ord(identifier) >= 97 \
                        and candidate.location[0] == ord(identifier) - 97) \
                        or (ord(identifier) < 97 \
                        and candidate.location[1] == int(identifier) - 1):
                    piece = candidate
        if not piece:
            self.logger.warning(\
                f'Move was invalid.\n{self.game.board}\nMove: {is_white} - {move}\n')
            return None, None
        return piece.location[0]*10 + piece.location[1], destination[0]*10 + destination[1]

