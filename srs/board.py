class Board:
    def __init__(self, square):
        self.square = square

    def board(self, square):
        alpha_lst = ['A','B','C','D','E','F','G','H']
        num_lst    = [1,2,3,4,5,6,7,8]
        board_lbl = {alpha_lst[x]+str(num_lst[y]): square}
