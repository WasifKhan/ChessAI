from ai.models.base_model import BaseModel


class WasifAI(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def train(self):
        return True

    def _resign(self, board, is_white):
        if len(board.history) >= 5:
            value = sum([value[3] for value in board.history[-5:]])
            if (value <= -10 and is_white) or (value >= 10 and not is_white):
                return True
        return False

    def _predict(self, board, is_white):
        from copy import copy
        if not hasattr(self, 'turn'):
            self.turn = 1 if is_white else 2
        my_pieces = board.white_pieces if is_white else board.black_pieces
        votes = dict()
        for piece in my_pieces:
            for key in piece.move_IDs:
                temp_board = copy(board)
                move = piece.move_IDs[key](piece.location)
                move_t = (move//10, move%10)
                if move_t[0] >= 0 and move_t[0] <= 7 \
                        and move_t[1] >= 0 and move_t[1] <= 7 \
                        and temp_board.is_valid_move(temp_board[piece.location], move_t):
                    temp_board.move(temp_board[piece.location], move_t)
                    if temp_board.plogger.log() in self.data[self.turn]:
                        source = piece.location[0]*10 + piece.location[1]
                        destination = move
                        votes[(source, destination)] = self.data[self.turn][temp_board.plogger.log()]
        self.turn += 2
        best_move = None
        best_vote = None
        total_votes = 0
        for key in votes:
            if not best_move or votes[key] > best_vote:
                best_move = key
                best_vote = votes[key]
            total_votes += votes[key]
        if not votes:
            logger.log('too stupid to make a move')
        else:
            logger.log(f'{best_vote*100/total_votes}% confident on this move')
        return best_move
