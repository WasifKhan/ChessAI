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
        my_pieces = board.white_pieces if is_white else board.black_pieces
        best_move = None
        board_value = None
        candidate_piece = None
        for my_piece in my_pieces:
            for move in my_piece.moves(board):
                print('thinking....')
                temp_board = copy(board)
                temp_board.move(temp_board[my_piece.location], ((move//10),(move%10)))
                their_pieces = temp_board.black_pieces if is_white else temp_board.white_pieces
                enemy_move_values = []
                for their_piece in their_pieces:
                    for their_move in their_piece.moves(temp_board):
                        second_temp_board = copy(temp_board)
                        second_temp_board.move(second_temp_board[their_piece.location], ((their_move//10),(their_move%10)))
                        my_pieces = second_temp_board.white_pieces if is_white else second_temp_board.black_pieces
                        cur_value = board.value() - second_temp_board.value()
                        if (cur_value <= 0 and is_white) or (cur_value >= 0 and not is_white):
                            print('Skipping branch')
                            (board_value, best_move, candidate_piece) = (cur_value, move, my_piece) \
                                if board_value is None or ((cur_value > board_value and is_white) or (cur_value < board_value and not is_white)) \
                                else (board_value, best_move, candidate_piece)
                            continue
                        for my_piece_2 in my_pieces:
                            for move_2 in my_piece_2.moves(second_temp_board):
                                third_temp_board = copy(second_temp_board)
                                third_temp_board.move(third_temp_board[my_piece_2.location], ((move_2//10), (move_2%10)))
                                their_pieces = third_temp_board.black_pieces if is_white else third_temp_board.white_pieces
                                for their_piece2 in their_pieces:
                                    for their_move2 in their_piece2.moves(third_temp_board):
                                        fourth_temp_board = copy(third_temp_board)
                                        fourth_temp_board.move(fourth_temp_board[their_piece2.location], ((their_move2//10),(their_move2%10)))
                                        enemy_move_values.append(fourth_temp_board.value())
                                    cur_value = min(enemy_move_values) if is_white else max(enemy_move_values)
                                    (board_value, best_move, candidate_piece) = (cur_value, move, my_piece) if board_value is None \
                                        or ((cur_value > board_value and is_white) or (cur_value < board_value and not is_white)) \
                                        else (board_value, best_move, candidate_piece)
                    
        return (candidate_piece.location[0]*10 + candidate_piece.location[1], best_move)