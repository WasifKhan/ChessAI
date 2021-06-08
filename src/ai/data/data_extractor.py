'''
File to extract chess games data from the web
'''

from ai.data.files import destination as DESTINATION, files as FILES
from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game, location, logger):
        super().__init__(game, location, logger)
        self._download_raw_data()

    def datapoints(self, num_games):
        state = int(open(self.location + '/train_state.txt').readlines()[0])
        skip_lines = state
        with open(DESTINATION + 'data.txt') as fp:
            for moves in fp:
                if num_games == 0:
                    break
                if skip_lines != 0:
                    skip_lines -= 1
                    continue
                num_games -= 1
                state += 1
                yield self._generate_datapoint(moves)
        open(self.location + '/train_state.txt', 'w').write(str(state))
        return StopIteration

    def get_data(self):
        self.logger.info(f'Begin extacting intelligence')
        location = f'./ai/data/dataset/intelligence.py'
        data = []
        with open(location, 'r') as fp:
            for i, line in enumerate(fp):
                data.append(eval(line[0:-1]))
        return data

    def set_data(self, data):
        self.logger.info(f'Begin saving intelligence')
        location = f'./ai/data/intelligence.py'
        with open(location, 'w') as fp:
            for moves in data:
                fp.write(str(moves) + '\n')

    def _download_raw_data(self):
        '''
        Downloads 15M Games = ID(10) * cur_ID(15) * num_games(100,000)
        '''
        from re import split
        from bz2 import BZ2File
        from urllib.request import urlopen
        num_games = 0
        for ID in range(0,10):
            for cur_ID in range(0, 15):
                try:
                    self.logger.info(f'Processing...{ID*10 + cur_ID}% done\n')
                    lines = BZ2File(urlopen(FILES[ID]), 'r')
                    data = self.get_data()
                    it = iter(lines)
                    filename = f'{DESTINATION}data_{ID}_{cur_ID}.txt'
                    with open(filename, 'w') as fp:
                        while (line := next(it)) and num_games < 100000:
                            move = str(line)
                            if 'WhiteElo' in move:
                                white_elo = int(split('"', move)[1])
                            elif 'BlackElo' in move:
                                black_elo = int(split('\"', move)[1])
                            elif move[2] == '1' and min(white_elo, black_elo) >= 2000:
                                num_games += 1
                                datapoint = self._raw_data_to_datapoint(move)
                                boards = self._generate_datapoint(datapoint)
                                for i, board in enumerate(boards[0]):
                                    if board.pprint() not in data[i]:
                                        data[i][board.pprint()] = 1
                                    else:
                                        data[i][board.pprint()] += 1
                                white_elo, black_elo = None, None
                                fp.write(datapoint)
                        num_games = 0
                except Exception as e:
                    self.set_data(data)
                    self.logger.error(f'Exception raised in download:\n{e}')
                    continue
        self.set_data(data)
        self.logger.info('Done downloading dataset')


    def _generate_datapoint(self, moves):
        from copy import copy
        self.game.__init__()
        x_vector, y_vector = [], []
        moves = eval(moves)
        for source, destination in moves:
            x = copy(self.game.board)
            if not self.game.move(source, destination):
                break
            y = (source, destination)
            x_vector.append(x)
            y_vector.append(y)
        return (x_vector, y_vector)


