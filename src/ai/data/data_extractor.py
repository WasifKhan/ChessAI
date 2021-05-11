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
    def __init__(self, game):
        self.game = game

    def _extract_moves(self, line):
        game = split('[\d]+\.\s', line)
        datapoint = '['
        for it in range (1, len(game) - 1):
            move = game[it].split('{')
            if len(move) > 1:
                white_move = split('[\?!#\+=]', move[0][0:-1])[0]
                black_move = split('[\?!#\+=]', move[-2].split()[-1])[0]
            else:
                white_move = split('[\?!#\+=]', move[0].split()[0])[0]
                black_move = split('[\?!#\+=]', move[0].split()[1])[0]
            datapoint += f"('{white_move}', '{black_move}'), "
        move = game[-1].split('{')
        if len(move) > 1:
            white_move = split('[\?!#\+=]', move[0][0:-1])[0]
            black_move = split('[\?!#\+=]', move[-2].split()[-1])[0]
        else:
            white_move = split('[\?!#\+=]', move[0].split()[0])[0]
            black_move = split('[\?!#\+=]', move[0].split()[1])[0]
        if white_move == black_move:
            black_move = 'None'
        elif '*' in black_move:
            black_move = 'None'
        elif '1-0' in black_move:
            black_move = 'None'
        elif '1/2' in black_move:
            black_move = 'Draw'
        elif '0-1' in black_move:
            white_move = 'None'
            black_move = 'None'
        if not white_move == 'None':
            datapoint += f"('{white_move}', '{black_move}'), "
        return datapoint[0:-2] + ']\n'
    
    def _convert_move(self, move):
        return move

    def _raw_data_to_datapoint(self, line):
        datapoint = '['
        moves = eval(self._extract_moves(line))
        for move in moves:
            white_move, black_move = move
            white_move = self._convert_move(white_move)
            #self.game.move(white_move)
            black_move = self._convert_move(black_move)
            #self.game.move(black_move)
            datapoint += f"('{white_move}', '{black_move}'), "
        datapoint = datapoint[0:-2] + ']\n'
        return datapoint 

    def raw_data_to_dataset(self):
        if len(listdir(DESTINATION)) > 2:
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
