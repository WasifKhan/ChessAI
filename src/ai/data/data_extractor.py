'''
File to extract chess games data from the web
'''

from ai.data.parser import Parser
from ai.data.dataset.files import destination as DESTINATION, files as RAW_DATA



class DataExtractor(Parser):
    def __init__(self, game, location, logger):
        super().__init__(game, location, logger)
        # self.download_raw_data()


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


    def download_raw_data(self):
        from bz2 import BZ2File
        from urllib.request import urlopen
        self.logger.info(f'\nBegin processing dataset\n')
        for ID in range(0,5):
            data = self._get_data()
            self.logger.info(f'Processing dataset...{ID*20}% done')
            filename = f'{DESTINATION}data_{ID}.txt'
            try:
                lines = BZ2File(urlopen(RAW_DATA[ID]), 'r')
                self._process_data(filename, iter(lines), data, 100)
            except Exception as e:
                if e.value != 'Finished':
                    self.logger.error(f'Exception raised in download:\n{e}')
                self._set_data(data)
                continue
        self.logger.info('Finish processing dataset')


    def _get_data(self):
        self.logger.info(f'Loading prior data')
        location = f'./ai/data/dataset/intelligence.py'
        data = []
        with open(location, 'r') as fp:
            for i, line in enumerate(fp):
                data.append(eval(line[0:-1]))
        return data


    def _set_data(self, data):
        self.logger.info(f'Saving processed data')
        location = DESTINATION + 'intelligence.py'
        with open(location, 'w') as fp:
            for moves in data:
                fp.write(str(moves) + '\n')


    def _process_data(self, filename, dataset, data, num_games):
        from re import split
        games_processed = 0
        with open(filename, 'w') as fp:
            white_elo, black_elo = None, None
            while (line := next(dataset)) and games_processed < num_games:
                if games_processed % num_games//100 == 0:
                    self.logger.debug(f'Current data {games_processed*100//num_games}% processed')
                move = str(line)
                if 'WhiteElo' in move:
                    white_elo = int(split('"', move)[1])
                elif 'BlackElo' in move:
                    black_elo = int(split('"', move)[1])
                elif move[2] == '1' and min(white_elo, black_elo) >= 2000:
                    games_processed += 1
                    datapoint = self._raw_data_to_datapoint(move)
                    boards = self._generate_datapoint(datapoint)
                    for i, board in enumerate(boards[0]):
                        if board.pprint() not in data[i]:
                            data[i][board.pprint()] = 1
                        else:
                            data[i][board.pprint()] += 1
                    white_elo, black_elo = None, None
                    fp.write(datapoint)
        raise StopIteration('Finished')


    def _generate_datapoint(self, moves):
        from copy import copy
        self.logger.debug('Generating datapoint')
        self.game.__init__()
        x_vector, y_vector = [], []
        moves = eval(moves)
        for source, destination in moves:
            x = copy(self.game.board)
            if not self.game.move(source, destination):
                self.logger.warning(\
                        f'Game was invalid.\n{x}\nMove: {source} -> {destination}')
                break
            y = (source, destination)
            x_vector.append(x)
            y_vector.append(y)
        return (x_vector, y_vector)

