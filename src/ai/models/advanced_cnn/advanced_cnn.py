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


    def _board_to_datapoint(self, board, is_white):
        from numpy import array
        piece_map = {'P':0, 'B':1, 'N':2, 'R':3, 'Q':4, 'K':5}
        board_direction = range(8) if is_white else range(7, -1, -1)
        x_data = []
        for row in board_direction:
            cur_row = []
            for column in range(8):
                dp = [0]*6
                if (piece := board[column,row]).value != 0:
                    value = 1 if piece.is_white == is_white else -1
                    dp[piece_map[str(piece).upper()]] = value
                cur_row.append(array(dp))
            x_data.append(array(cur_row))
        x_data = array(x_data)
        return x_data


    def _prediction_to_move(self, predictions, board, is_white):
        piece_map = {0:'P', 1:'B', 2:'N', 3:'R', 4:'Q', 5:'K'}
        board_direction = range(8) if is_white else range(7, -1, -1)
        moves = []
        for prediction in predictions:
            best_pred, best_val, true_val, best_piece = prediction
            board_move = best_pred.reshape((8,8))
            for row in board_direction:
                for column in range(8):
                    board_val = round(float(board_move[row][column]), 3)
                    if board_val == true_val:
                        destination = column*10 + (row if is_white else 7-row)
                        moves.append([piece_map[best_piece], None, destination, round(best_val, 3)])
        for piece in board.white_pieces if is_white else board.black_pieces:
            for move in moves:
                best_piece, _, destination, best_val = move
                if str(piece).upper() == best_piece \
                        and board.is_valid_move(piece, (destination//10, destination%10)):
                    source = piece.location[0]*10 + piece.location[1]
                    move[1] = source
                    break
        self.logger.debug(f'Current board:\n{board}')
        message = 'Possible moves:\n'
        output = None
        for move in moves:
            piece, source, destination, best_val = move
            if source:
                if not output:
                    output = move
                message += f'{best_val}: {piece}. {source} -> {destination}\n'
        self.logger.debug(f'{message}')
        confidence = f'Piece-CNN: {output[0]}. {output[1]} -> {output[2]}'
        confidence += 'Very' if moves[0][3] >= 0.7 \
                else 'Somewhat' if moves[0][3] >= 0.5 \
                else 'Not very' if moves[0][3] >= 0.3 \
                else 'Not at all'
        confidence += ' confident about this move.'
        self.logger.info(confidence)
        return output[1:3]



    def _generate_datapoints(self, boards, moves, is_white=True):
        from numpy import array
        piece_map = {'P':0, 'B':1, 'N':2, 'R':3, 'Q':4, 'K':5}
        for i in range(len(boards)):
            board = boards[i]
            piece = boards[i][moves[i][0]]
            index = piece_map[str(piece).upper()]
            source = moves[i][0] if is_white else (moves[i][0]//10)*10 + (7-moves[i][0]%10)
            destination = moves[i][1] if is_white else (moves[i][1]//10)*10 + (7-moves[i][1]%10)
            move = (source, destination)
            x_data = self._board_to_datapoint(board, is_white)
            y_selector = array([0]*6)
            y_selector[index] = 1
            y_piece = array([[0]*8]*8).reshape(8,8)
            y_piece[move[1]%10][move[1]//10] = 1
            y_piece = y_piece.reshape((-1, ))
            self.model.add_data('S', x_data, y_selector)
            self.model.add_data(str(piece).upper(), x_data, y_piece)
            is_white = not(is_white)


    def _predict(self, board, is_white):
        from numpy import set_printoptions
        self.logger.debug('Begin prediction')
        piece_map = {0:'P', 1:'B', 2:'N', 3:'R', 4:'Q', 5:'K'}
        set_printoptions(suppress=True)
        dp = self._board_to_datapoint(board, is_white).reshape((1, 8, 8, 6))
        selector = self.model.get_model('S').predict(dp)[0].round(3)
        self.logger.debug(f'Piece probabilities: [P, B, N, R, Q, K]: {selector}')
        candidate_moves = []
        for ID in piece_map:
            model = self.model.get_model(piece_map[ID])
            move_pred = model.predict(dp)[0].round(3)
            max_pred = round(float(max(move_pred.reshape((-1,)))), 3)
            cur_val = max_pred * selector[ID]
            candidate_moves.append((move_pred, cur_val, max_pred, ID))
        candidate_moves = sorted(candidate_moves, key=lambda x: -x[1])
        return self._prediction_to_move(candidate_moves, board, is_white)


    def _train_model(self):
        self.logger.info('Building models')
        self.model.build_model((8, 8, 6), [(64, 'softmax'), (6, 'softmax')])
        iterations = 20
        num_datapoints = 1000
        for it in range(iterations):
            self.logger.info(f'Training models... {it*(100//iterations)}% done')
            self.model.clear_data()
            for data in self.datapoints(num_datapoints):
                self._generate_datapoints(*data, True)
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
                axs.plot(performance[-1].history['categorical_accuracy'], color=train_color,
                        label=f'{model} - Train Loss')
                axs.plot(performance[-1].history['val_categorical_accuracy'], color=test_color,
                        label=f'{model} - Test Loss')
            pyplot.legend()
            pyplot.show()

