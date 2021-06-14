'''
AI Implemented Using Basic Convolutional Neural Network

self._predict(board, is_white)
self._build_model()
self._train_model()
self._evaluate_model()
self._board_to_datapoint(board, is_white)
'''

from ai.data.model_info import ModelInfo
from ai.models.advanced_cnn.architecture import Architecture



class AdvancedCnn(ModelInfo):
    def __init__(self, game, location):
        super().__init__(game, location)
        self.model = Architecture(location)

    def _predict(self, board, is_white):
        from numpy import set_printoptions
        self.logger.debug(f'board is:\n{str(board)}')
        set_printoptions(suppress=True)
        piece_map = {0:'P', 1:'B', 2:'N', 3:'R', 4:'Q', 5:'K'}
        dp = self._boards_to_datapoints(board, is_white)
        model = self.model.get_model('S')
        selector = model.predict(dp)[0].round(3)
        self.logger.debug(f'Piece probabilities: [P, B, N, R, Q, K]: {selector}')
        best_pred, best_val, best_piece = [None]*3
        true_max_pred = None
        for ID in piece_map:
            model = self.model.get_model(piece_map[ID])
            move_pred = model.predict(dp)[0].round(3)
            max_pred = max(move_pred.reshape((-1,)))
            cur_val = max_pred * selector[ID]
            if best_val is None or best_val < cur_val:
                best_pred, best_val, best_piece = move_pred, cur_val, ID
                true_max_pred = max_pred

        board_move = best_pred.reshape((8,8))
        piece_dp = dp[:,:,:,best_piece:best_piece+1].reshape((8,8))
        self.logger.debug(f'prediction:\n{board_move}')
        self.logger.debug(f'true:\n{piece_dp}')
        source = None
        board_direction = range(8) if is_white else range(7, -1, -1)
        for row in board_direction:
            for column in range(8):
                if board_move[row][column] == true_max_pred:
                    destination = column*10 + 7-row
                    self.logger.debug(f'destination is: {destination}')
        for piece in board.white_pieces if is_white else board.black_pieces:
            if str(piece).upper() == piece_map[best_piece] \
                    and board.is_valid_move(piece, (destination//10, destination%10)):
                source = piece.location[0]*10 + piece.location[1]
                self.logger.debug(f'source is: {source}')
                break
        self.logger.debug(f'Predicted {source} -> {destination}')
        if not source:
            return False
        return (source, destination)


    def _train_model(self):
        self.logger.info('Building models')
        self.model.build_model((8, 8, 6), [(64, 'softmax'), (6, 'softmax')])
        iterations = 20
        for it in range(iterations):
            self.logger.info(f'Training models... {it*(100//iterations)}% done')
            num_datapoints = 8000
            self.model.clear_data()
            for data in self.datapoints(num_datapoints):
                self._boards_to_datapoints(*data, True)
            self.model.train(batch_size=128, epochs=10)
        self.model.save_model()


    def _evaluate_model(self):
        from matplotlib import pyplot
        from matplotlib.colors import CSS4_COLORS
        for ID in self.model.data:
            colors = iter(CSS4_COLORS)
            fig, axs = pyplot.subplots()
            fig.suptitle(f'{ID} Network')
            for model in self.model.performances:
                train_color, test_color = next(colors), next(colors)
                performance = self.model.performances[model][ID][-3:-1]
                color_pair = next(colors)
                axs.plot(performance[-1].history['loss'], color=train_color,
                        label=f'{model} - Train Loss')
                axs.plot(performance[-1].history['val_loss'], color=test_color,
                        label=f'{model} - Test Loss')
            pyplot.legend()
            pyplot.show()


    def _boards_to_datapoints(self, boards, moves=None, is_white=True):
        from numpy import array
        piece_map = {'P':0, 'B':1, 'N':2, 'R':3, 'Q':4, 'K':5}
        if not moves:
            self.logger.debug('Begin prediction')
            board_direction = range(8) if is_white else range(7, -1, -1)
            x_data = []
            for row in board_direction:
                cur_row = []
                for column in range(8):
                    dp = [0]*6
                    if (piece := boards[column,row]).value != 0:
                        value = 1 if piece.is_white == is_white else -1
                        dp[piece_map[str(piece).upper()]] = value
                    cur_row.append(array(dp))
                x_data.append(array(cur_row))
            x_data = array(x_data)
            x_data = x_data.reshape((1,8,8,6))
            return x_data

        for i in range(len(boards)):
            board = boards[i]
            piece = boards[i][moves[i][0]]
            index = piece_map[str(piece).upper()]
            source = moves[i][0] if i % 2 == 0 else (moves[i][0]//10)*10 + (7-moves[i][0]%10)
            destination = moves[i][1] if i % 2 == 0 else (moves[i][1]//10)*10 + (7-moves[i][1]%10)
            move = (source, destination)
            board_direction = range(8) if i % 2 == 0 else range(7, -1, -1)
            x_data = []
            for row in board_direction:
                cur_row = []
                for column in range(8):
                    cur_piece = board[column,row]
                    dp = [0]*6
                    if str(cur_piece) != '.':
                        value = 1 if not(cur_piece.is_white) == i % 2 else -1
                        dp[piece_map[str(cur_piece).upper()]] = value
                    cur_row.append(dp)
                x_data.append(array(cur_row))
            x_data = array(x_data)
            y_selector = array([0]*6)
            y_selector[index] = 1
            y_piece = array([[0]*8]*8).reshape(8,8)
            y_piece[move[1]%10][move[1]//10] = 1
            y_piece = y_piece.reshape((-1, ))
            self.model.add_data('S', x_data, y_selector)
            self.model.add_data(str(piece).upper(), x_data, y_piece)
            is_white = not(is_white)

