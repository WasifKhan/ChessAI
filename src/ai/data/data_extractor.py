'''
File to extract chess games data from the web
'''

from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game, location, logger):
        super().__init__(game, location, logger)
        from time import localtime
        self.num_games = 10000000
        self.destination = 'ai/data/dataset/'
        self.link_start =\
        'https://database.lichess.org/standard/lichess_db_standard_rated_'
        self.link_end = '.pgn.bz2'
        self.cur_year = localtime()[0] + 1
        self.cur_month = localtime()[1]


    @property
    def memory(self):
        location = self.destination + 'intelligence.py'
        data = []
        with open(location, 'r') as fp:
            for i, line in enumerate(fp):
                data.append(eval(line[0:-1]))
        return data

    @memory.setter
    def memory(self, data):
        location = self.destination + 'intelligence.py'
        with open(location, 'w') as fp:
            for moves in data:
                fp.write(str(moves) + '\n')


    def datapoints(self, num_games):
        state = int(open(self.location + '/train_state.txt').readlines()[0])
        skip_lines = state
        with open(self.destination + 'data.txt') as fp:
            for moves in fp:
                if num_games == 0:
                    break
                if skip_lines != 0:
                    skip_lines -= 1
                    continue
                num_games -= 1
                state += 1
                yield self._generate_datapoint(moves)
        open(self.location + '/train_state.txt', 'w').write(str(state))
        return StopIteration


    def download_raw_data(self):
        from bz2 import BZ2File
        from urllib.request import urlopen
        self.logger.info(f'\nBegin processing dataset\n')
        total = (self.cur_year - 2015 - 1)*12 + self.cur_month-1
        for year in range(2013, self.cur_year):
            for month in range(1, 13):
                if year == self.cur_year - 1 and month == self.cur_month - 1:
                    break
                link_ID = str(year) + '-'
                link_ID += str(month) if month >= 10 else '0' + str(month)
                link = self.link_start + link_ID + self.link_end
                self.logger.info(f'Processing dataset...{((year-2015)*12+month-1)*100//total}% done')
                filename = f'{self.destination}data_{year}_{month}.txt'
                lines = BZ2File(urlopen(link), 'r')
                memory = self.memory
                try:
                    state = open(filename, 'w')
                    self._process_data(state, iter(lines), memory)
                except StopIteration:
                    state.close()
                    self.logger.info('File Complete')
                self.memory = memory
        self.logger.info('Finish processing dataset')


    def _process_data(self, state, dataset, memory):
        from re import split
        games_processed = 0
        num_games = self.num_games//100
        white_elo, black_elo = 0, 0
        while (line := next(dataset)) and games_processed < num_games:
            move = str(line)
            if 'WhiteElo' in move:
                white_elo = split('"', move)[1]
                if white_elo[0] != '2':
                    white_elo = 0
                    continue
                white_elo = int(white_elo)
            elif 'BlackElo' in move:
                black_elo = split('"', move)[1]
                if black_elo[0] != '2':
                    black_elo = 0
                    continue
                black_elo = int(black_elo)
            elif move[2] == '1' and min(white_elo, black_elo) >= 2000:
                games_processed += 1
                datapoint = self._raw_data_to_datapoint(move)
                boards = self._generate_datapoint(datapoint)
                for i, board in enumerate(boards[0]):
                    try:
                        memory[i][board.pprint()] += 1
                    except KeyError:
                        memory[i][board.pprint()] = 1
                white_elo, black_elo = 0, 0
                state.write(datapoint)


    def _generate_datapoint(self, moves):
        from copy import copy
        self.logger.debug('Generating datapoint')
        self.game.__init__()
        x_vector, y_vector = [], []
        moves = eval(moves)
        for source, destination in moves:
            x = copy(self.game.board)
            if not self.game.move(source, destination):
                self.logger.warning(\
                        f'Game was invalid.\n{x}\nMove: {source} -> {destination}')
                break
            y = (source, destination)
            x_vector.append(x)
            y_vector.append(y)
        return (x_vector, y_vector)

