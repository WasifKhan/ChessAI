class Square:
    def __init__(self, location):
        self.location = location
        self.is_white = None

    def __str__(self):
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

    def __str__(self):
        return 'K' if self.is_white else 'k'
        
    def is_valid_move(self, board, destination):
        return True
    

class King(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
    
    def __str__(self):
        return '$' if self.is_white else '-'

    def is_valid_move(self, board, destination):
        return True

    
class Queen(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def __str__(self):
        return 'Q' if self.is_white else 'q'    
    
    def is_valid_move(self, board, destination):
        return True
    

class Rook(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def __str__(self):
        return 'R' if self.is_white else 'r'

    def is_valid_move(self, board, destination):
        if self.is_white:
            # Check for vertical + movement
            if destination[1] > self.location[1]:
                for i in range(1, destination[1]):
                    if (self.location[1] + i == destination[1] and
                        self.location[0] == destination[0]):
                        if board[destination].is_white == None:
                            return True
            # Check for horizontal + movement
            if destination[0] > self.location[0]:
                for i in range(1, destination[0]):
                    if (self.location[0] + i == destination[0] and
                        self.location[1] == destination[1]):
                        if board[destination].is_white == None:
                            return True
            # Check for vertical - movement
            if destination[1] < self.location[1]:
                for i in range(1, destination[1]):
                    if (self.location[1] - i == destination[1] and
                        self.location[0] == destination[0]):
                        if board[destination].is_white == None:
                            return True
            # Check for horizontal - movement
            if destination[0] > self.location[0]:
                for i in range(1, destination[0]):
                    if (self.location[0] - i == destination[0] and
                        self.location[1] == destination[1]):
                        if board[destination].is_white == None:
                            return True
            if not(isinstance(board[destination], Piece)):
                return True

            if board[destination].is_white == False:
                return True
        
        # Black Rook
        if not self.is_white:
            # Check for vertical + movement
            if destination[1] > self.location[1]:
                for i in range(1, destination[1]):
                    if (self.location[1] + i == destination[1] and
                        self.location[0] == destination[0]):
                        if board[destination].is_white == None:
                            return True
            # Check for horizontal + movement
            if destination[0] > self.location[0]:
                for i in range(1, destination[0]):
                    if (self.location[0] + i == destination[0] and
                        self.location[1] == destination[1]):
                        if board[destination].is_white == None:
                            return True
            # Check for vertical - movement
            if destination[1] < self.location[1]:
                for i in range(1, destination[1]):
                    if (self.location[1] - i == destination[1] and
                        self.location[0] == destination[0]):
                        if board[destination].is_white == None:
                            return True
            # Check for horizontal - movement
            if destination[0] > self.location[0]:
                for i in range(1, destination[0]):
                    if (self.location[0] - i == destination[0] and
                        self.location[1] == destination[1]):
                        if board[destination].is_white == None:
                            return True
            if not(isinstance(board[destination], Piece)):
                return True

            if board[destination].is_white == False:
                return True
               
class Bishop(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def __str__(self):
        return 'B' if self.is_white else 'b'

    def is_valid_move(self, board, destination):
        if self.is_white:
            
                x_direction = destination[0] - self.location[0]
                y_direction = destination[1] - self.location[1]
                
                if x_direction == y_direction:
                    # Check X + and Y + plane
                    if (x_direction > 0 and y_direction > 0):
                        for i in range(1, x_direction):
                            if board[destination[0] + i, destination[1] + i].is_white == None:
                                return True

                    if (0 > x_direction and 0 > y_direction):
                        # Check X- and Y -
                        for i in range(1, x_direction):
                            if board[destination[0] - i, destination[1] - i].is_white == None:
                                return True
                
                if x_direction == abs(y_direction):
                    # Check X + and Y -
                    if (x_direction > 0 and 0 > y_direction):
                        for i in range(x_direction):
                            if board[destination[0] + i, destination[1] - i].is_white == None:
                                return True

                if abs(x_direction) == y_direction:
                    # Check X- and Y +
                    if (0 > x_direction and y_direction > 0):
                        for i in range(x_direction):
                            if board[destination[0] - i, destination[1] + i].is_white == None:
                                return True
        
                if not(isinstance(board[destination], Piece)):
                    return True

                if board[destination].is_white == False:
                    return True

        # Black Bishop
        if self.is_white == False:
                x_direction = destination[0] - self.location[0]
                y_direction = destination[1] - self.location[1]

                if x_direction == y_direction:
                    # Check X + and Y + plane
                    if (x_direction > 0 and y_direction > 0):
                        for i in range(1, x_direction):
                            if board[destination[0] + i, destination[1] + i].is_white == None:
                                return True

                    if (0 > x_direction and 0 > y_direction):
                        # Check X- and Y -
                        for i in range(1, x_direction):
                            if board[destination[0] - i, destination[1] - i].is_white == None:
                                return True
                
                if x_direction == abs(y_direction):
                    # Check X + and Y -
                    if (x_direction > 0 and 0 > y_direction):
                        for i in range(x_direction):
                            if board[destination[0] + i, destination[1] - i].is_white == None:
                                return True

                if abs(x_direction) == y_direction:
                    # Check X- and Y +
                    if (0 > x_direction and y_direction > 0):
                        for i in range(x_direction):
                            if board[destination[0] - i, destination[1] + i].is_white == None:
                                return True
                if not(isinstance(board[destination], Piece)):
                        return True
                if board[destination].is_white:
                    return True

class Pawn(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def __str__(self):
        return 'P' if self.is_white else 'p'

    def is_valid_move(self, board, destination):
        if self.is_white:
            # Check for diagonal movement
            if (self.location[1] + 1 == destination[1] and
               (self.location[0] + 1 == destination[0] or
                self.location[0] - 1 == destination[0])):
                if board[destination].is_white == False:
                    return True
                # Check for en passant movement
                elif board[destination].is_white == None:                    
                    previous_move = board.history[-1]
                    if (isinstance(previous_move[0], Pawn) and                        
                    previous_move[1][1] - previous_move[2][1] == 2 and
                    previous_move[2][0] == destination[0] and self.location[1] == 4):
                        return True
                                 

            # Check for vertical movement - 1 square
            if (self.location[1] + 1 == destination[1] and
                self.location[0] == destination[0]):
                if board[destination].is_white == None:
                    return True
            # Check for vertical movement - 2 squares
            elif (self.location[1] + 2 == destination[1] and 
                  self.location[0] == destination[0] and 
                  self.location[1] == 1):
                if (board[destination].is_white == None and
                    board[(destination[0], destination[1] - 1)].is_white == None):
                    return True
            
        else:
            # Check for diagonal movement
            if (self.location[1] - 1 == destination[1] and
               (self.location[0] + 1 == destination[0] or
                self.location[0] - 1 == destination[0])):
                if board[destination].is_white:
                    return True
                # Check for en passant movement    
                elif board[destination].is_white == None:                    
                    previous_move = board.history[-1]
                    if (isinstance(previous_move[0], Pawn) and
                    previous_move[1][1] - previous_move[2][1] == -2 and
                    previous_move[2][0] == destination[0] and self.location[1] == 3):
                        return True
            # Check for vertical movement - 1 square
            if (self.location[1] - 1 == destination[1] and
                self.location[0] == destination[0]):
                if board[destination].is_white == None:
                    return True
            # Check for vertical movement - 2 squares
            elif (self.location[1] - 2 == destination[1] and 
                  self.location[0] == destination[0] and 
                  self.location[1] == 6):
                if (board[destination].is_white == None and
                    board[(destination[0], destination[1] + 1)].is_white == None):
                    return True
            
        return False

 
