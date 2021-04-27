'''
File to convert raw online data to dataset for learning purposes
'''

import os
import re

RAW_DATA_LOCATION = 'raw_data/'
DATASET_LOCATION = 'dataset/data.txt'

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
                        white_move = re.split('\W', move[0][0:-1])[0]
                        black_move = re.split('\W', move[-2].split()[-1])[0]
                    else:
                        white_move = re.split('\W', move[0].split()[0])[0]
                        black_move = re.split('\W', move[0].split()[1])[0]
                    if it + 1 == len(game) and white_move == black_move:
                        black_move = 'None'
                    datapoint += f'({white_move}, {black_move}), '
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



converter = DataConverter(RAW_DATA_LOCATION, DATASET_LOCATION)
converter.raw_data_to_dataset()

