from src.backend.pieces.piece import Square
from src.backend.pieces.pawn import Pawn


moves = [
    ('black/white pawn move two',
        ['A2 A4', 'A7 A5', 'A4 A5'],
        [Pawn(is_white=True, location=(0,3)),
         Pawn(is_white=False, location=(0,4))]),
    ('white pawn capture black pawn',
        ['B2 B4', 'C7 C5', 'B4 C5'],
        [Pawn(is_white=True, location=(2,4)),
         Square(location=(1,3))]),
    ('black pawn capture white pawn',
        ['B2 B4', 'C7 C5', 'A2 A4', 'C5 B4'],
        [Pawn(is_white=False, location=(1,3)),
         Square(location=(2,4))]),
    ('white pawn invalid move',
        ['B2 B5'],
        [Pawn(is_white=True, location=(1,1)),
         Square(location=(1,4))]),
]

