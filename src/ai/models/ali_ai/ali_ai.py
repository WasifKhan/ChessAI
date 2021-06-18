from ai.data.model_info import ModelInfo


class AliAI(ModelInfo):
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
        '''
        self.memory: list(X)
            X: dict(repr(board): int)
        -----------------------------
        Contains 1M games of data. Each index in list represents all boards for
        a given turn.
        Boards are represented as keys in a dictionary with the value being the
        frequency of how much the board occurred
        Ie. list[0] contains a dictionary of size 1 containing the starting
        board.
        list[1] contains a dictionary with keys reprenting the board state
        after white made their first move. Values being the frequency of how
        many games white made that move.
        '''
        if self._resign(board, is_white):
            return False
        if x := self.edge_cases(board, is_white):
            return x
        from copy import copy
        my_pieces = board.white_pieces if is_white else board.black_pieces
        best_moves = []
        for my_piece in my_pieces:
            for move in my_piece.moves(board):
                source = my_piece.location[0]*10 + my_piece.location[1]
                temp_board = copy(board)
                temp_board.move(temp_board[my_piece.location], ((move//10),(move%10)))
                their_pieces = temp_board.black_pieces if is_white else temp_board.white_pieces
                enemy_move_values = []
                for their_piece in their_pieces:
                    for their_move in their_piece.moves(temp_board):
                        if not temp_board.is_valid_move(their_piece,
                                (their_move//10, their_move%10)):
                            continue
                        second_temp_board = copy(temp_board)
                        second_temp_board.move(second_temp_board[their_piece.location], ((their_move//10),(their_move%10)))
                        my_pieces = second_temp_board.white_pieces if is_white else second_temp_board.black_pieces
                        cur_value = board.value() - second_temp_board.value()
                        if enemy_move_values == []:
                            enemy_move_values = [(cur_value, second_temp_board)]
                        elif (cur_value == enemy_move_values[0][0] and is_white) or (cur_value == enemy_move_values[0][0] and not is_white):
                            enemy_move_values.append((cur_value,second_temp_board))
                        else:
                            if (cur_value > enemy_move_values[0][0] and is_white) or (cur_value < enemy_move_values[0][0] and not is_white):
                                enemy_move_values = [(cur_value, second_temp_board)]
                cur_value = enemy_move_values[0][0]
                if best_moves == []:
                    best_moves = [(cur_value, enemy_move_values[0][1], source, move)]
                elif (best_moves[0][0] == cur_value and is_white) or (best_moves[0][0] == cur_value and not is_white):
                    best_moves.append((cur_value, enemy_move_values[0][1], source, move))
                else:
                    if (best_moves[0][0] > cur_value and is_white) or (best_moves[0][0] < cur_value and not is_white):
                        best_moves = [(cur_value, enemy_move_values[0][1], source, move)]
        # Omit next line to continue search
        return best_moves[0][2], best_moves[0][3]
        real_best_move = []

        for state in best_moves:
            third_temp_board = state[1]
            my_pieces = third_temp_board.white_pieces if is_white else third_temp_board.black_pieces
            for my_piece in my_pieces:
                for move in my_piece.moves(third_temp_board):
                    source = my_piece.location[0]*10 + my_piece.location[1]
                    fourth_temp_board = copy(third_temp_board)
                    their_pieces = fourth_temp_board.black_pieces if is_white else fourth_temp_board.white_pieces
                    enemy_move_values = []
                    for their_piece in their_pieces:
                        for their_move in their_piece.moves(fourth_temp_board):
                            fifth_temp_board = copy(fourth_temp_board)
                            fifth_temp_board.move(fifth_temp_board[their_piece.location], ((their_move//10),(their_move%10)))
                            my_pieces = fifth_temp_board.white_pieces if is_white else fifth_temp_board.black_pieces
                            cur_value = third_temp_board.value() - fifth_temp_board.value()
                            if enemy_move_values == []:
                                enemy_move_values = [(cur_value, fifth_temp_board)]
                            elif (cur_value == enemy_move_values[0][0] and is_white) or (cur_value == enemy_move_values[0][0] and not is_white):
                                enemy_move_values.append((cur_value,fifth_temp_board))
                            else:
                                if (cur_value > enemy_move_values[0][0] and is_white) or (cur_value < enemy_move_values[0][0] and not is_white):
                                    enemy_move_values = [(cur_value, fifth_temp_board)]
                    cur_value = enemy_move_values[0][0]
                    if real_best_move == []:
                        real_best_move = [(cur_value, enemy_move_values[0][1], state[2], state[3])]
                    elif (real_best_move[0][0] == cur_value and is_white) or (real_best_move[0][0] == cur_value and not is_white):
                            real_best_move.append((cur_value, enemy_move_values[0][1], state[2], state[3]))
                    else:
                        if (real_best_move[0][0] > cur_value and is_white) or (real_best_move[0][0] < cur_value and not is_white):
                            real_best_move = [(cur_value, enemy_move_values[0][1], state[2], state[3])]
        
        return (real_best_move[0][2], real_best_move[0][3])
