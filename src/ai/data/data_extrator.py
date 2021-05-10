'''
File to extract chess games data from the web

*****************
*****WARNING*****
Running this file takes approximately 15 hours
*****************
'''

from os import listdir
from re import split
from bz2 import BZ2File
from urllib.request import urlopen
from ai.data.raw_data.files import files as FILES



SOURCE = 'ai/data/raw_data/data_files/'
DESTINATION = 'ai/data/dataset/'


class DataExtractor:
    def __init__(self, files, source, destination):
        self.files = files
        self.source = source
        self.destination = destination
        self.filename = 'data'
        self.data = []

    def download_raw_data(self):
        if len(listdir(self.source)) > 1:
            return
        for ID in range(len(self.files)):
            try:
                index = 0
                lines = BZ2File(urlopen(self.files[ID]), 'r')
                it = iter(lines)
                while True:
                    filename = self.source + self.filename + str(ID) + f'_{index}.txt'
                    print(f'processing {filename}')
                    with open(filename, 'wb') as fp:
                        for _ in range(10000000):
                            line = next(it)
                            fp.write(line)
                    index += 1
            except EOFError:
                continue

    def _extract_moves(self, raw_data, filename):
        with open(self.destination + filename, 'w') as fp:
            for line in raw_data:
                if line[0] == '1':
                    game = split('[\d]+\.\s', line)
                    datapoint = '['
                    for it in range (1, len(game)):
                        move = game[it].split('{')
                        if len(move) > 1:
                            white_move = split('[\?!#\+=]', move[0][0:-1])[0]
                            black_move = split('[\?!#\+=]', move[-2].split()[-1])[0]
                        else:
                            white_move = split('[\?!#\+=]', move[0].split()[0])[0]
                            black_move = split('[\?!#\+=]', move[0].split()[1])[0]
                        if it + 1 == len(game) and white_move == black_move:
                            black_move = 'None'
                        datapoint += f"('{white_move}', '{black_move}'), "
                    datapoint = datapoint[0:-2] + ']\n'
                    fp.write(datapoint)

    def clean_raw_data(self):
        if len(listdir(self.destination)) > 1:
            print('in here')
            return
        for filename in listdir(self.source):
            with open(self.source + filename) as fp:
                if filename[0] == '.':
                    print(f'git ignore: {filename}')
                    continue
                print(f'processing {filename}')
                self._extract_moves(fp, filename)

    def raw_data_to_dataset(self):
        pass

data_extractor = DataExtractor(FILES, SOURCE, DESTINATION)
