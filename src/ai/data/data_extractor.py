'''
File to extract chess games data from the web
'''

from bz2 import BZ2File
from urllib.request import urlopen
from ai.data.files import destination as DESTINATION, files as FILES
from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game, location, download=False):
        super().__init__(game, location)
        self.download = download
        # self._download_raw_data()


    def datapoints(self, num_games):
        if self.download:
            from os import listdir
            for data in listdir(DESTINATION):
                if data[0] == 'd':
                    with open(DESTINATION + data) as fp:
                        for moves in fp:
                            if num_games == 0:
                                return StopIteration
                            num_games -= 1
                            yield self._generate_datapoint(moves)
        else:
            for moves in self._stream_raw_data(num_games):
                yield self._generate_datapoint(moves)
        return StopIteration


    def _download_raw_data(self):
        from time import time
        num_games = 0
        start = None
        for ID in range(10):
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
                    print(output)
                    with open(filename, 'w') as fp:
                        while (line := next(it)) and num_games < 100000:
                            if (move := str(line))[2] == '1':
                                num_games += 1
                                datapoint = self._raw_data_to_datapoint(move)
                                fp.write(datapoint)
                        num_games = 0
                except Exception:
                    continue
        print('Done downloading dataset')


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


