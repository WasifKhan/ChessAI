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
        return True if 'weights.h5' in listdir(self.location) else False

    def _train(self):
        self._build_model()
        self._train_model()
        self._evaluate_model()

    def _predict_move(self, board, is_white):
        model = self._load_model()
        prediction = model.predict(self._board_to_datapoint(board, is_white))
        return self._prediction_to_board(prediction)

    def _board_to_datapoint(self, board, is_white):
        datapoint = [[board[column,row].value \
                    if board[column,row].is_white == is_white \
                    else board[column,row].value * -1 \
                for column in range(8)] \
                for row in range(7, -1, -1)]
        return datapoint

    def _generate_datapoint(self, moves):
        '''
        Map list of moves into:
        np.array(board), np.array([{0,1}] * 124)
        '''
        return moves

    def _get_data_points(self):
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
