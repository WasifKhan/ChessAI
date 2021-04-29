from .piece import Piece


class Pawn(Piece):
    ID = 1
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
        self.ID = Pawn.ID
        Pawn.ID += 1

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

    def moves(self, board):
        result = set()
        
        
        y_direction = 1 if self.is_white else -1
        # Single vertical movement
        if (piece:= board[self.location[0], self.location[1] + y_direction]).is_white is None:
            result.add(piece.location[0] * 10 + piece.location[1])
        # Double vertical movement
        if (self.location[1] == 1 and self.is_white) or (self.location[1] == 6 and not(self.is_white)):
            if (piece:= board[self.location[0], self.location[1] + y_direction * 2]).is_white is None:
                result.add(piece.location[0] * 10 + piece.location[1])
        
        # Capture
        if (self.location[0] == 0):
            if (piece:= board[self.location[0] + 1, self.location[1] + y_direction]).is_white is not self.is_white and piece.is_white is not None:
                result.add(piece.location[0] * 10 + piece.location[1]) 
        elif (self.location[0] == 7):
            if (piece:= board[self.location[0] - 1, self.location[1] + y_direction]).is_white is not self.is_white and piece.is_white is not None:
                result.add(piece.location[0] * 10 + piece.location[1])
        else:
            if (piece:= board[self.location[0] + 1, self.location[1] + y_direction]).is_white is not self.is_white and piece.is_white is not None:
                result.add(piece.location[0] * 10 + piece.location[1])
            if (piece:= board[self.location[0] - 1, self.location[1] + y_direction]).is_white is not self.is_white and piece.is_white is not None:
                result.add(piece.location[0] * 10 + piece.location[1])
        # En passant
        '''
        NEED TO IMPLEMENT EN PASSANT MOVEMENT
        '''
        return result
