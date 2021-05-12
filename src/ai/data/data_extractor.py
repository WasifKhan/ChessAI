'''
File to extract chess games data from the web
'''

from os import listdir
from bz2 import BZ2File
from urllib.request import urlopen
from ai.data.files import destination as DESTINATION, files as FILES
from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game):
        super().__init__(game)

    def download_raw_data(self):
        if len(listdir(DESTINATION)) > 3:
            return
        for ID in range(5):#len(FILES)):
            try:
                lines = BZ2File(urlopen(FILES[ID]), 'r')
                it = iter(lines)
                '''
                Can remove notion of index once ready to use
                Also change this loop to be len(FILES) and change the
                inner loop to be 'for _ in range(ten_million)'
                '''
                index = 0
                while line := next(it):
                    if index == 8:
                        raise StopIteration
                    filename = f'{DESTINATION}data_{str(ID)}_{index}.txt'
                    print(f'Processing: {ID}.({index}/30) / 100 ')
                    with open(filename, 'w') as fp:
                        for _ in range(100000):#00):
                            if (move := str(next(it)))[2] == '1':
                                datapoint = self._raw_data_to_datapoint(move)
                                fp.write(datapoint)
                    index += 1
            except StopIteration:
                continue
        print('Done downloading dataset')

    def get_datapoint(self):
        dataset_path = './ai/data/dataset/'
        for data in listdir(dataset_path):
            if data[0] == 'd':
                with open(dataset_path + data) as fp:
                    for moves in fp:
                        yield self._generate_datapoint(moves)


