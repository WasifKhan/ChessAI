'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta
from os import listdir



class AI(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location
        if not self._trained():
            self._train()

    def _trained(self):
        return True if 'brain.h5' in listdir(self.location) else False

    def _train(self):
        self._build_model()
        self._train_model()
        self._evaluate_model()

    def _predict_move(self, board, is_white):
        model = self._load_model()
        prediction = model.predict(self._board_to_datapoint(board, is_white))
        return self._prediction_to_board(prediction)

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
        return datapoint

    def _generate_datapoint(self, moves, iter=[0]):
        '''
        THIS FUNCTION SHOULD DO THE load_dataset() in the cNN tutorial
        Map list of moves into: (np.array(shape=(X,8,8,1), np.array(X, 124,1))
        '''
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
        # SPLIT INTO 2 games!
        ret_val = ([test_data_x_0, test_data_x_1], [test_data_y_0,
            test_data_y_1])
        if iter[0] % 2 == 0:
            ret_val = ([test_data_x_2, test_data_x_3], [test_data_y_2, test_data_y_3])
        iter[0] += 1
        return ret_val

    def _get_datapoint(self):
        dataset_path = './ai/data/dataset/'
        for data in listdir(dataset_path):
            if data[0] == 'd':
                with open(dataset_path + data) as fp:
                    for moves in fp:
                        yield self._generate_datapoint(moves)

    def _resign(self, board, is_white):
        if len(board.history) < 3:
            return False
        prior_turns = [board.history[i][3] for i in range(-3, 0, 1)]
        if is_white and max(prior_turns) <= -2 \
            or (not is_white and min(prior_turns) >= 2):
                return True
        return False

    def get_move(self, board, is_white):
        return False if self._resign(board, is_white) else self._predict_move(board, is_white)
