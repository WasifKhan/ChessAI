'''
File to extract chess games data from the web
'''

from bz2 import BZ2File
from urllib.request import urlopen
from ai.data.files import files as FILES
from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game, location):
        super().__init__(game, location)


    def datapoints(self, num_games):
        for moves in self._download_raw_data(num_games):
            yield self._generate_datapoint(moves)


    def _download_raw_data(self, num_games):
        train_state = self.location + '/train_state.txt'
        file_id = None
        with open(train_state) as fp:
            file_ID = int(fp.readline()[0])
        while num_games != 0:
            lines = BZ2File(urlopen(FILES[file_ID]), 'r')
            it = iter(lines)
            try:
                while num_games != 0 and (line := str(next(it))):
                    if line[2] == '1':
                        num_games -= 1
                        yield self._raw_data_to_datapoint(line)
            except Exception:
                file_ID += 1
                continue
        with open(train_state, 'w') as fp:
            fp.write(str(file_ID+1))
        return StopIteration


    def _generate_datapoint(self, moves):
        moves = eval(moves)
        self.game.__init__()
        x_vector = []
        y_vector = []
        from copy import deepcopy
        for source, destination in moves:
            x = deepcopy(self.game.board)
            if self.game.move(source, destination):
                y = (source, destination)
                x_vector.append(x)
                y_vector.append(y)
            else:
                break
        return (x_vector, y_vector)


