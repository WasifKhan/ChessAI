class Square:
    def __init__(self, location):
        self.location = location
        self.is_white = None

    def display(self):
        return '_'
        
class Piece(Square):
    def __init__(self, is_white, location):
        super().__init__(location)
        self.is_white = is_white

    def move(self, location):
        self.location = location

class Knight(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'K' if self.is_white else 'k'
        
    def is_valid_move(self, board, destination):
        return True
    

class King(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
    
    def display(self):
        return '$' if self.is_white else '-'

    def is_valid_move(self, board, destination):
        return True

    
class Queen(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'Q' if self.is_white else 'q'    
    
    def is_valid_move(self, board, destination):
        return True
    

class Rook(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'R' if self.is_white else 'r'

    def is_valid_move(self, board, destination):
        return True


class Bishop(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'B' if self.is_white else 'b'

    def is_valid_move(self, board, destination):
        return True


class Pawn(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'P' if self.is_white else 'p'

    def is_valid_move(self, board, destination):
        # Check for diagonal movement
        if self.is_white:
            if (self.location[1] + 1 == destination[1] and
               (self.location[0] + 1 == destination[0] or
                self.location[0] - 1 == destination[0])):
                if board[destination].is_white == False:
                    return True
        else:
            if (self.location[1] - 1 == destination[1] and
               (self.location[0] + 1 == destination[0] or
                self.location[0] - 1 == destination[0])):
                if board[destination].is_white:
                    return True

        # Check for vertical movement
        if self.is_white:
            if (self.location[1] + 1 == destination[1] and
                self.location[0] == destination[0]):
                if board[destination].is_white == None:
                    return True
            elif (self.location[1] + 2 == destination[1] and 
                  self.location[0] == destination[0] and 
                  self.location[1] == 1):
                if (board[destination].is_white == None and
                    board[(destination[0], destination[1] - 1)].is_white == None):
                    return True
        else:
            if (self.location[1] - 1 == destination[1] and
                self.location[0] == destination[0]):
                if board[destination].is_white == None:
                    return True
            elif (self.location[1] - 2 == destination[1] and 
                  self.location[0] == destination[0] and 
                  self.location[1] == 1):
                if (board[destination].is_white == None and
                    board[(destination[0], destination[1] + 1)].is_white == None):
                    return True
        return False

 
