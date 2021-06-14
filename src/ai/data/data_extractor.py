'''
File to extract chess games data from the web
'''

from ai.data.parser import Parser



class DataExtractor(Parser):
    def __init__(self, game, location, logger):
        super().__init__(game, location, logger)
        from time import localtime
        self.destination = 'ai/data/dataset/'
        self.raw_data = {
                'link_start': 'https://database.lichess.org/standard/lichess_db_standard_rated_',
                'link_end': '.pgn.bz2',
                'start_year': 2013,
                'cur_year': localtime()[0] + 1,
                'cur_month': localtime()[1],
                'total': (localtime()[0] - 2013)*12 + localtime()[1] - 1
                }


    @property
    def memory(self):
        location = self.destination + 'memory.py'
        data = []
        with open(location, 'r') as fp:
            for i, line in enumerate(fp):
                data.append(eval(line[0:-1]))
        return data


    @memory.setter
    def memory(self, data):
        location = self.destination + 'memory.py'
        with open(location, 'w') as fp:
            for moves in data:
                fp.write(str(moves) + '\n')


    def clean_memory(self):
        old_data = self.memory
        data = []
        for i, dp in enumerate(old_data[0:25]):
            cur_dict = dict()
            for board in dp:
                if (i < 8 and dp[board] >= 9)\
                        or (i < 16 and dp[board] >= 8)\
                        or (i < 21 and dp[board] >= 6)\
                        or (i < 25 and dp[board] >= 4):
                    cur_dict[board] = dp[board]
            data.append(cur_dict)
        self.memory = data

    def datapoints(self, num_games):
        from os import listdir
        data = open(self.location + '/train_state.txt').readlines()
        datafile, line = int(data[0][0:-1]), int(data[1])
        skip_lines = line
        while num_games != 0:
            with open(self.destination + f'data_{datafile}.txt') as fp:
                for moves in fp:
                    if num_games == 0:
                        break
                    if skip_lines != 0:
                        skip_lines -= 1
                        continue
                    num_games -= 1
                    line += 1
                    yield self._generate_datapoint(moves)
            if num_games != 0:
                datafile += 1
                line = 0
        open(self.location + '/train_state.txt','w')\
                .write(f'{datafile}\n{line}')
        return StopIteration


    def download_raw_data(self):
        from bz2 import BZ2File
        from urllib.request import urlopen
        self.logger.info(f'\nBegin processing dataset\n')
        for year in range(2018, self.raw_data['cur_year']):
            for month in range(2, 12):
                if year == self.raw_data['cur_year'] - 1 \
                        and month == self.raw_data['cur_month'] - 1:
                    break
                link_ID = str(year) + '-'
                link_ID += str(month) if month >= 10 else '0' + str(month)
                link = self.raw_data['link_start'] \
                        + link_ID \
                        + self.raw_data['link_end']
                self.logger.info(f'Processing data: {year}:{month}...{((year-2013)*12+(month-1))*100//self.raw_data["total"]}% done')
                filename = f'{self.destination}data_{year}_{month}'
                lines = BZ2File(urlopen(link), 'r')
                memory = self.memory
                try:
                    self._process_data(filename, iter(lines), memory)
                except (StopIteration, EOFError):
                    self.logger.info('File Complete')
                except Exception as e:
                    import traceback
                    self.logger.error(\
                            f'Exception occured!\n{traceback.format_exc(3)}')
                self.memory = memory
        self.logger.info('Finish processing dataset')


    def _process_data(self, filename, dataset, memory):
        from re import split
        file_ID = 0
        while True:
            games_processed = 0
            state = open(f'{filename}_{file_ID}.txt', 'w')
            white_elo, black_elo = 0, 0
            while games_processed < 100000 and (line := next(dataset)):
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
                elif move[2] == '1' and min(white_elo, black_elo) >= 2400:
                    games_processed += 1
                    datapoint = self._raw_data_to_datapoint(move)
                    boards = self._generate_datapoint(datapoint)
                    for i, board in enumerate(boards[0]):
                        try:
                            memory[i][repr(board)] += 1
                        except KeyError:
                            memory[i][repr(board)] = 1
                        except IndexError:
                            break
                    white_elo, black_elo = 0, 0
                    state.write(datapoint)
            file_ID += 1
        raise EOFError
