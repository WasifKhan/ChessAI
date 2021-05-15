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

    def _download_raw_data(self, ID):
        lines = BZ2File(urlopen(FILES[ID]), 'r')
        it = iter(lines)
        '''
        Can remove notion of index once ready to use
        Also change this loop to be len(FILES) and change the
        inner loop to be 'for _ in range(ten_million)'
        '''
        index = 0
        print(f'Processing File: {ID}')
        while line := next(it):
            if index == 1000:
                return StopIteration
            if (move := str(next(it)))[2] == '1':
                datapoint = self._raw_data_to_datapoint(move)
                yield move
                index += 1
        print(f'Done processing file: {ID}')

    def datapoints(self, location):
        train_state = location + '/train_state.txt'
        with open(train_state) as fp:
            file_ID = int(fp.readline()[0])
        for i, moves in enumerate(self._download_raw_data(file_ID)):
            yield self._generate_datapoint(moves)
        with open(train_state, 'w') as fp:
            fp.write(str(file_index+1))

