'''
File to extract chess games data from the web
'''

import bz2
from urllib.request import urlopen
from files import files as FILES

LOCATION = 'raw_data/'

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


data_extractor = ExtractData(LOCATION, FILES)
data_extractor.extract_data()
