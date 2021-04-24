class Square:
    def __init__(self, location):
        self.location = location
        self.is_white = None

    def __str__(self):
        return '.'
        
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
        vertical_move = abs(destination[0] - self.location[0])
        horizontal_move = abs(destination[1] - self.location[1])

        if not(vertical_move == 1 and horizontal_move == 2) and not(vertical_move == 2 and horizontal_move == 1):
            print(vertical_move)
            print(horizontal_move)
            return False
        elif not(isinstance(board[destination], Piece)):
            return True        
        elif self.is_white and board[destination].is_white:
            return False
        elif not(self.is_white) and not(board[destination].is_white):
            return False
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
        x_direction = destination[0] - self.location[0]
        y_direction = destination[1] - self.location[1]
        x_plane = 1 if x_direction > 0 else -1
        y_plane = 1 if y_direction > 0 else -1

        # Horizontal movement
        if (x_direction != 0 and y_direction == 0):
            for i in range(1, abs(x_direction)):
                if not(board[self.location[0] + (i * x_plane), self.location[1]].is_white == None):
                    return False
        # Vertical movement
        elif (y_direction != 0 and x_direction == 0):
            for i in range(1, abs(y_direction)):
                if not(board[self.location[0], self.location[1] + (i * y_plane)].is_white == None):
                    return False
        # Diagonal movement            
        elif abs(x_direction) != abs(y_direction):
            return False
        else:
            for i in range(1, x_direction):
                if not(board[self.location[0] + (i * x_plane), self.location[1] + (i*y_plane)].is_white == None):
                    return False
        if not(isinstance(board[destination], Piece)):
            return True        
        elif self.is_white and board[destination].is_white:
            return False
        elif not(self.is_white) and not(board[destination].is_white):
            return False
        return True

class Rook(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def __str__(self):
        return 'R' if self.is_white else 'r'

    def is_valid_move(self, board, destination):
        x_direction = destination[0] - self.location[0]
        y_direction = destination[1] - self.location[1]
        x_plane = 1 if x_direction > 0 else -1
        y_plane = 1 if y_direction > 0 else -1
        
        # Horizontal movement
        if (x_direction != 0 and y_direction == 0):
            for i in range(1, abs(x_direction)):
                if not(board[self.location[0] + (i * x_plane), self.location[1]].is_white == None):
                    return False
        # Vertical movement
        elif (y_direction != 0 and x_direction == 0):
            for i in range(1, abs(y_direction)):
                if not(board[self.location[0], self.location[1] + (i * y_plane)].is_white == None):
                    return False
        else:
            return False
        if not(isinstance(board[destination], Piece)):
            return True        
        elif self.is_white and board[destination].is_white:
            return False
        elif not(self.is_white) and not(board[destination].is_white):
            return False
        return True

class Bishop(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def __str__(self):
        return 'B' if self.is_white else 'b'

    def is_valid_move(self, board, destination):
        x_direction = destination[0] - self.location[0]
        y_direction = destination[1] - self.location[1]
        x_plane = 1 if x_direction > 0 else -1
        y_plane = 1 if y_direction > 0 else -1
        if abs(x_direction) != abs(y_direction):
            return False
        for i in range(1, x_direction):
            if not(board[self.location[0] + (i * x_plane), self.location[1] + (i*y_plane)].is_white == None):
                return False
        if not(isinstance(board[destination], Piece)):
            return True        
        elif self.is_white and board[destination].is_white:
            return False
        elif not(self.is_white) and not(board[destination].is_white):
            return False
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

 
