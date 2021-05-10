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
from ai.data.files import destination as DESTINATION, files as FILES



class DataExtractor:
    def __init__(self, files, destination):
        self.files = files
        self.destination = destination

    def _convert_to_datapoint(self, line):
        return line

    def _extract_moves(self, line):
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
        return self._convert_to_datapoint(datapoint[0:-2] + ']\n')

    def raw_data_to_dataset(self):
        if len(listdir(self.destination)) > 1:
            return
        for ID in range(5):#len(self.files)):
            try:
                lines = BZ2File(urlopen(self.files[ID]), 'r')
                it = iter(lines)
                '''
                Can remove notion of index once ready to use
                Also change this loop to be len(self.files) and change the
                inner loop to be 'for _ in range(ten_million)'
                '''
                index = 0
                while line := next(it):
                    if index == 8:
                        raise StopIteration
                    filename = f'{self.destination}data_{str(ID)}_{index}.txt'
                    print(f'Processing: {ID}.({index}/30) / 100 ')
                    with open(filename, 'w') as fp:
                        for _ in range(100000):#00):
                            if (move := str(next(it)))[2] == '1':
                                moves = self._extract_moves(move)
                                fp.write(moves)
                    index += 1
            except StopIteration:
                continue
        print('Done downloading dataset')

data_extractor = DataExtractor(FILES, DESTINATION)
