class Square:
    def __init__(self, location):
        self.location = location

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
        
    def move(self, location):
        pass


class King(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
    
    def display(self):
        return '$' if self.is_white else '-'

    def move(self, location):
        pass
    
class Queen(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'Q' if self.is_white else 'q'    
    
    def move(self, location):
        pass

class Rook(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'R' if self.is_white else 'r'

    def move(self, location):
        pass

class Bishop(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'B' if self.is_white else 'b'

    def move(self, location):
        pass

class Pawn(Piece):
    def __init__(self, is_white, location):
        super().__init__(is_white, location)

    def display(self):
        return 'P' if self.is_white else 'p'

    def move(self, location):
        pass  
