'''
File to extract chess games data from the web
'''

from os import listdir
from bz2 import BZ2File
from urllib.request import urlopen
from ai.data.files import files as FILES
from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game):
        super().__init__(game)

    def datapoints(self, location):
        train_state = location + '/train_state.txt'
        file_id = None
        with open(train_state) as fp:
            file_ID = int(fp.readline()[0])
        for moves in self._download_raw_data(file_ID):
            yield self._generate_datapoint(moves)
        with open(train_state, 'w') as fp:
            fp.write(str(file_ID+1))

    def _download_raw_data(self, ID):
        lines = BZ2File(urlopen(FILES[ID]), 'r')
        it = iter(lines)
        index = 0
        print(f'{ID*2}% Processing.')
        try:
            while line := str(next(it)):
                if index % 1000 == 0:
                    print(f'{ID*2}%: Processing... {index//1000}% done')
                if index == 100000:
                    return StopIteration
                if line[2] == '1':
                    datapoint = self._raw_data_to_datapoint(line)
                    yield datapoint
                index += 1
        except Exception:
            return StopIteration
        print(f'{ID*2}% Done processing.')

    def _generate_datapoint(self, moves):
        datapoint = ()
        moves = eval(moves)
        self.game.__init__()
        x_vector = []
        y_vector = []
        from copy import deepcopy
        for source, destination in moves:
            x = deepcopy(self.game.board)
            if self.game.move(source, destination):
                y = (source, destination)
                x_vector.append(x)
                y_vector.append(y)
            else:
                break
        return (x_vector, y_vector)


