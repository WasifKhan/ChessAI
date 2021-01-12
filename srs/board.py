class Board:
    def __init__(self, square):
        self.square = square

    def board(self, square):
        alpha_lst = ['A','B','C','D','E','F','G','H']
        num_lst    = [1,2,3,4,5,6,7,8]
        #board_lbl = {alpha_lst[x]+str(num_lst[y]): square}
        board_label = {'A1':square, 'A2':square, 'A3':square, 'A4':square, 'A5':square, 
                    'A6':square, 'A7':square, 'A8':square, 'B1':square, 'B2':square, 
                    'B3':square, 'B4':square, 'B5':square, 'B6':square, 'B7':square, 
                    'B8':square, 'C1':square, 'C2':square, 'C3':square, 'C4':square, 
                    'C5':square, 'C6':square, 'C7':square, 'C8':square, 'D1':square, 
                    'D2':square, 'D3':square, 'D4':square, 'D5':square, 'D6':square, 
                    'D7':square, 'D8':square, 'E1':square, 'E2':square, 'E3':square, 
                    'E4':square, 'E5':square, 'E6':square, 'E7':square, 'E8':square, 
                    'F1':square, 'F2':square, 'F3':square, 'F4':square, 'F5':square, 
                    'F6':square, 'F7':square, 'F8':square, 'G1':square, 'G2':square, 
                    'G3':square, 'G4':square, 'G5':square, 'G6':square, 'G7':square, 
                    'G8':square, 'H1':square, 'H2':square, 'H3':square, 'H4':square, 
                    'H5':square, 'H6':square, 'H7':square, 'H8':square}