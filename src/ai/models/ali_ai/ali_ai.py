from ai.models.base_model import BaseModel


class AliAI(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def train(self):
        return True

    def edge_cases(self, board, is_white):
        if len(board.history) < 1:
            return (41, 43)
        elif len(board.history) < 2:
            if board[33].is_white is not None \
                or board[53].is_white is not None \
                or board[52].value == 3:
                return (36, 34)
            return (46, 44)
        return None
             
    def _resign(self, board, is_white):
        if len(board.history) >= 5:
            value = sum([value[3] for value in board.history[-5:]])
            if (value <= -10 and is_white) or (value >= 10 and not is_white):
                return True
        return False

    def predict(self, board, is_white):
        if self._resign(board, is_white):
            return False
        if x := self.edge_cases(board, is_white):
            return x
        from copy import copy
        my_piece = board.white_pieces if is_white else board.black_pieces
        their_piece = board.black_pieces if is_white else board.white_pieces
        best_move = None
        board_value = None
        candidate_piece = None
        for piece in my_piece:
            for move in piece.moves(board):
                temp_board = copy(board)
                temp_board.move(temp_board[piece.location], ((move//10),(move%10)))
                cur_value = temp_board.value()
                (board_value, best_move, candidate_piece) = (cur_value, move, piece) if board_value is None \
                    else (cur_value, move, piece) if (cur_value > board_value and is_white) or (cur_value < board_value and not is_white) \
                    else (board_value, best_move, candidate_piece)
                '''
                if is_white:
                    if best_move is None:
                        best_move = cur_value
                        candidate_piece = piece
                    elif cur_value > best_move:
                        best_move = cur_value
                        candidate_piece = piece
                else:
                    if cur_value is None:
                        best_move = cur_value
                        candidate_piece = piece
                    elif cur_value < best_move:
                        best_move = cur_value
                        candidate_piece = piece
                '''
        return (candidate_piece.location[0]*10 + candidate_piece.location[1], best_move)





