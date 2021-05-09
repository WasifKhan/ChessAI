'''
File to extract chess games data from the web
'''

from bz2 import BZ2Decompressor
from urllib.request import urlopen
from ai.data.raw_data.files import files as FILES
from os import listdir
from re import split



SOURCE = 'ai/data/raw_data/data_files/'
DESTINATION = 'ai/data/data.txt'


class DataExtractor:
    def __init__(self, files, source, destination):
        self.files = files
        self.source = source
        self.destination = destination
        self.filename = 'data'
        self.chunk = 16 * 1024
        self.data = []

    def _extract_file(self, file, ID):
        decompressor = BZ2Decompressor()
        filename = self.source + self.filename + str(ID) + '.txt'
        with open(filename, 'wb') as fp:
            req = urlopen(file)
            while chunk := req.read(self.chunk):
                decomp = decompressor.decompress(chunk)
                if decomp:
                    fp.write(decomp)

    def download_raw_data(self):
        if len(listdir(self.source)) > 1:
            return
        for ID in range(len(self.files)):
            try:
                self._extract_file(self.files[ID], ID)
            except EOFError:
                continue

    def _extract_moves(self, lines):
        for line in lines[:-1]:
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
                self.data.append(datapoint)

    def raw_data_to_dataset(self):
        if 'data.txt' in listdir('ai/data/'):
            return
        for filename in listdir(self.source):
            with open(self.source + filename) as fp:
                lines = fp.readlines()
                self._extract_moves(lines)
        with open(self.destination, 'w') as fp:
            for datapoint in self.data:
                fp.write(datapoint)


data_extractor = DataExtractor(FILES, SOURCE, DESTINATION)
