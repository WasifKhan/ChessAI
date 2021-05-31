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
        my_pieces = copy(board.white_pieces) if is_white else copy(board.black_pieces)
        best_move_per_piece = []
        for my_piece in my_pieces:
            for move in my_piece.moves(board):
                print('thinking.')
                break_move = False
                temp_board = copy(board)
                print(f'piece is: {str(my_piece)}, location is: {my_piece.location}')
                print(f'move is {move}\nboard is:\n{board}')
                temp_board.move(temp_board[my_piece.location], ((move//10),(move%10)))
                print('got here')
                their_pieces = temp_board.black_pieces if is_white else temp_board.white_pieces
                enemy_move_values = []
                for their_piece in their_pieces:
                    for their_move in their_piece.moves(temp_board):
                        second_temp_board = copy(temp_board)
                        second_temp_board.move(second_temp_board[their_piece.location], ((their_move//10),(their_move%10)))
                        board_value = board.value() - second_temp_board.value()
                        if (board_value > 0 and is_white) or (board_value < 0 and not is_white):
                            break_move = True
                            break
                        enemy_move_values.append((second_temp_board.value(), (their_piece.location[0]*10 + their_piece.location[1], their_move)))
                    if break_move:
                        break
                if break_move:
                    print('broke out of move')
                    continue
                else:
                    best_board = []
                    best_move = []
                    for board_val in enemy_move_values:
                        if best_move == []:
                            best_move = [board_val[0]]
                            best_board = [board_val[1]]
                        elif (best_move[0] > board_val[0] and is_white) and (best_move[0] < board_val[0] and not is_white):
                            best_move = [board_val[0]]
                            best_board = [board_val[1]]
                        elif best_move[0] == board_val[0]:
                            best_move.append(board_val[0])
                            best_board.append(board_val[1])
                    for i, board in enumerate(best_board):
                        best_move_per_piece.append((best_move[i], (my_piece.location[0]*10 + my_piece.location[1], best_board[i])))
        if len(best_move_per_piece) == 1:
            return best_move_per_piece[2][0]*10 + best_move_per_piece[2][1], best_move_per_piece[3]
        best_move = None
        board_value = None
        candidate_piece = None
        for state in best_move_per_piece:
            print('thinking...')
            cur_board = copy(state[1])
            my_pieces = state[1].white_pieces if is_white else state[1].black_pieces
            for my_piece_2 in my_pieces:
                for move_2 in my_piece_2.moves(cur_board):
                    third_temp_board = copy(cur_board)
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