'''
File to extract chess games data from the web
'''

import bz2
from urllib.request import urlopen
from files import files as FILES
import os
import re

LOCATION = 'raw_data/'
DATASET_LOCATION = 'dataset/data.txt'

class ExtractData:
    def __init__(self, location, files):
        self.location = location
        self.files = files
        self.filename = 'data'
        self.chunk = 16 * 1024

    def extract_file(self, file, ID):
        decompressor = bz2.BZ2Decompressor()
        filename = self.location + self.filename + str(ID) + '.txt'
        try:
            with open(filename, 'wb') as fp:
                req = urlopen(file)
                while chunk := req.read(self.chunk):
                    decomp = decompressor.decompress(chunk)
                    if decomp:
                        fp.write(decomp)
        except EOFError:
            fp.close()
            return

    def extract_data(self):
        for ID in range(len(self.files)):
            self.extract_file(self.files[ID], ID)

class DataConverter:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.data = []

    def extract_moves(self, lines):
        for line in lines[:-1]:
            if line[0] == '1':
                game = re.split('[\d]+\.\s', line)
                datapoint = '['
                for it in range (1, len(game)):
                    move = game[it].split('{')
                    if len(move) > 1:
                        white_move = re.split('[\?!#\+=]', move[0][0:-1])[0]
                        black_move = re.split('[\?!#\+=]', move[-2].split()[-1])[0]
                    else:
                        white_move = re.split('[\?!#\+=]', move[0].split()[0])[0]
                        black_move = re.split('[\?!#\+=]', move[0].split()[1])[0]
                    if it + 1 == len(game) and white_move == black_move:
                        black_move = 'None'
                    datapoint += f"('{white_move}', '{black_move}'), "
                datapoint = datapoint[0:-2] + ']\n'
                self.data.append(datapoint)

    def raw_data_to_dataset(self):
        for filename in os.listdir(self.source):
            with open(self.source + filename) as fp:
                lines = fp.readlines()
                self.extract_moves(lines)
        with open(self.destination, 'w') as fp:
            for datapoint in self.data:
                fp.write(datapoint)
'''
data_extractor = ExtractData(LOCATION, FILES)
data_extractor.extract_data()
'''
converter = DataConverter(LOCATION, DATASET_LOCATION)
converter.raw_data_to_dataset()
