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
            if index % 10 == 0:
                print(f'Processing... {index//15}% done')
            if index == 150:
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
            temp_board = self.game.copy_board()
            print(f'temp_board is: {temp_board}')
            print(f'our board is: {self.game.board}')
            if temp_board[source].is_white is not None and temp_board.move(temp_board[source], (destination//10, destination%10)):
                is_white = self.game.board[source].is_white
                y = self._move_to_datapoint(self.game.board, is_white, temp_board.move_ID)
                self.game.move(source, destination)
                y_vector.append(y)
        return (x_vector, y_vector)

    def datapoints(self, location):
        from os import listdir
        train_state = location + '/train_state.txt'
        data_sample = location + '/sample_data.txt'
        if 'sample_data.txt' in listdir(location):
            with open(data_sample, 'r') as fp:
                for line in fp:
                    print(line)
            return

        file_id = None
        with open(train_state) as fp:
            file_ID = int(fp.readline()[0])
        with open(data_sample, 'w') as fp:
            for moves in self._download_raw_data(file_ID):
                x,y = self._generate_datapoint(moves)
                for i in range(len(x)):
                    print(f'input: \n{x[i]}\noutput: \n{y[i]}')
                    fp.write('[' + str(x[i]) + ', ' + str(y[i]) + ']\n')
        '''
                yield self._generate_datapoint(moves)
        with open(train_state, 'w') as fp:
            # CHANGE TO str(file_ID)+1) when done
            fp.write(str(file_ID))
        '''
