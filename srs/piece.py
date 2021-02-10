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

class Knight(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'K' if self.is_white else 'k'
        
    def is_valid_move(self, board, destination):
        return True
    
    def move(self, location):
        pass


class King(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
    
    def display(self):
        return '$' if self.is_white else '-'

    def is_valid_move(self, board, destination):
        return True

    def move(self, location):
        pass
    
class Queen(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'Q' if self.is_white else 'q'    
    
    def is_valid_move(self, board, destination):
        return True
    
    def move(self, location):
        pass

class Rook(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'R' if self.is_white else 'r'

    def is_valid_move(self, board, destination):
        return True

    def move(self, location):
        pass

class Bishop(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'B' if self.is_white else 'b'

    def is_valid_move(self, board, destination):
        return True

    def move(self, location):
        pass

class Pawn(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'P' if self.is_white else 'p'

    def is_valid_move(self, board, destination):
        # TODO: Implement correct movement
        current_location = self.location
        if current_location[0] != destination[0]:
            print(f'current_location: {current_location}')
            return False
        if abs(current_location[1] - destination[1]) > 1:
            print(f'current_location[1]: {current_location[1]}')
            print(f'destination[1]: {destination[1]}')
            return False
        return True

    def move(self, location):
        pass  
