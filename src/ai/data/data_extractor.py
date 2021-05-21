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
        '''
        index = 0
        print(f'Processing File: {ID}')
        while line := str(next(it)):
            if index % 100 == 0:
                print(f'Processing... {index//100}% done')
            if index == 300:
                break
            if line[2] == '1':
                datapoint = self._raw_data_to_datapoint(line)
                yield datapoint
            index += 1
        print(f'Done processing file: {ID}')

    def _generate_datapoint(self, moves):
        datapoint = ()
        moves = eval(moves)
        self.game.__init__()
        x_vector = []
        y_vector = []
        for source, destination in moves:
            x = self._board_to_datapoint(self.game.board, self.game.white_turn)
            x_vector.append(x)
            if self.game.move(source, destination):
                y = self._move_to_datapoint(self.game.board.move_ID)
                y_vector.append(y)
        return (x_vector, y_vector)

    def datapoints(self, location):
        train_state = location + '/train_state.txt'
        file_id = None
        with open(train_state) as fp:
            file_ID = int(fp.readline()[0])
        for i, moves in enumerate(self._download_raw_data(file_ID)):
            yield self._generate_datapoint(moves)
        with open(train_state, 'w') as fp:
            # CHANGE TO str(file_ID)+1) when done
            fp.write(str(file_ID))

