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
                try:
                    y = self._move_to_datapoint(self.game.board[destination].get_move())
                    y_vector.append(y)
                except Exception:
                    x_vector.pop()
                    return (x_vector, y_vector)
           # NO ELSE NEEDED ONCE WORKING PROPERLY
            else:
                return ([], [])
        return (x_vector, y_vector)

    def datapoints(self, location):
        train_state = location + '/train_state.txt'
        file_id = None
        with open(train_state) as fp:
            file_ID = int(fp.readline()[0])
        for i, moves in enumerate(self._download_raw_data(file_ID)):
            yield self._generate_datapoint(moves)
        with open(train_state, 'w') as fp:
            fp.write(str(file_ID+1))

