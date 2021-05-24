'''
File to extract chess games data from the web
'''

from bz2 import BZ2File
from urllib.request import urlopen
from ai.data.files import destination as DESTINATION, files as FILES
from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game, location):
        super().__init__(game, location)
        # self._download_raw_data()


    def datapoints(self, num_games):
        '''
        Online version
        for moves in self._stream_raw_data(num_games):
            yield self._generate_datapoint(moves)
        return StopIteration
        ------------------------
        Offline Version
        for data in listdir(dataset_path):
            if data[0] == 'd':
                with open(DESTINATION + data) as fp:
                    for moves in fp:
                        if num_games == 0:
                            return StopIteration
                        num_games -= 1
                        yield self._generate_datapoint(moves)
        return StopIteration
        '''
        dataset_path = './ai/data/data.txt'
        with open(dataset_path) as fp:
            for moves in fp:
                if num_games == 0:
                    return StopIteration
                num_games -= 1
                yield self._generate_datapoint(moves)

    def _download_raw_data(self):
        DESTINATION = 'ai/data/dataset/'
        num_games = 0
        # Each file contains 10M games
        for ID in range(10):
            # Save 1M games per file
            for cur_ID in range(10):
                try:
                    lines = BZ2File(urlopen(FILES[ID]), 'r')
                    it = iter(lines)
                    filename = f'{DESTINATION}data_{ID}_{cur_ID}.txt'
                    print(f'Processing...{ID*10 + cur_ID}% done')
                    with open(filename, 'w') as fp:
                        while (line := next(it)) and num_games < 1000000:
                            if (move := str(line))[2] == '1':
                                num_games += 1
                                datapoint = self._raw_data_to_datapoint(move)
                                fp.write(datapoint)
                        num_games = 0
                except Exception as e:
                    continue
        print('Done downloading dataset')


    def _stream_raw_data(self, num_games):
        train_state = self.location + '/train_state.txt'
        file_id = None
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
        moves = eval(moves)
        self.game.__init__()
        x_vector = []
        y_vector = []
        from copy import copy
        for source, destination in moves:
            x = copy(self.game.board)
            if self.game.move(source, destination):
                y = (source, destination)
                x_vector.append(x)
                y_vector.append(y)
            else:
                break
        return (x_vector, y_vector)


