'''
File to extract chess games data from the web
'''

from bz2 import BZ2File
from urllib.request import urlopen
from ai.data.files import destination as DESTINATION, files as FILES
from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game, location, logger):
        super().__init__(game, location, logger)
        #self._download_raw_data()


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

    def populate_data(self, num_games):
        from time import time
        data = self.get_data()
        self.logger.info('Populating data...')
        for i, moves in enumerate(self._stream_raw_data(num_games)):
            if i % 1000 == 0:
                if i != 0:
                    self.logger.debug(f'took {str(time()-start)[0:5]}s to process')
                start = time()
                self.logger.debug(f'{i/10000}% done')
            if i % 10000 == 0 and i != 0:
                self.set_data(data)
                self.logger.debug('Saving state...')
            datapoints = self._generate_datapoint(moves)
            for i, board in enumerate(datapoints[0]):
                if board.pself.logger.log() not in data[i]:
                    data[i][board.pprint()] = 1
                else:
                    data[i][board.pprint()] += 1
        self.set_data(data)
        self.logger.info('Done populating...')

    def get_data(self):
        self.logger.info(f'Begin extacting intelligence.')
        location = f'./ai/data/dataset/intelligence.py'
        self.logger.info('Extracting Intelligence...')
        data = []
        with open(location, 'r') as fp:
            for i, line in enumerate(fp):
                data.append(eval(line[0:-1]))
        self.logger.info(f'Done extacting intelligence.')
        return data

    def set_data(self, data):
        location = f'./ai/data/intelligence.py'
        with open(location, 'w') as fp:
            for moves in data:
                fp.write(str(moves) + '\n')

    def _download_raw_data(self):
        from time import time
        num_games = 0
        start = None
        for ID in range(1,3):
            for cur_ID in range(100):
                try:
                    lines = BZ2File(urlopen(FILES[ID]), 'r')
                    it = iter(lines)
                    filename = f'{DESTINATION}data_{ID}_{cur_ID}.txt'
                    output = f'Processing...{ID*10 + cur_ID}% done\n'
                    if start:
                        end = time()
                        minutes, seconds = int((end-start)//60), int((end-start)%60)
                        output += f'Previous 100,000 games took {minutes}m{seconds}s to process\n'
                    start = time()
                    self.logger.info(output)
                    with open(filename, 'w') as fp:
                        while (line := next(it)) and num_games < 100000:
                            if (move := str(line))[2] == '1':
                                num_games += 1
                                datapoint = self._raw_data_to_datapoint(move)
                                fp.write(datapoint)
                        num_games = 0
                except Exception:
                    continue
        self.logger.info('Done downloading dataset')


    def _stream_raw_data(self, num_games):
        train_state = self.location + '/train_state.txt'
        with open(train_state) as fp:
            file_ID = int(fp.readline()[0])
        while num_games != 0:
            lines = BZ2File(urlopen(FILES[file_ID]), 'r')
            it = iter(lines)
            try:
                while num_games != 0 and (line := str(next(it))):
                    if line[2] == '1':
                        num_games -= 1
                        yield self._raw_data_to_datapoint(line)
            except Exception:
                file_ID += 1
                continue
        with open(train_state, 'w') as fp:
            fp.write(str(file_ID+1))
        return StopIteration


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


