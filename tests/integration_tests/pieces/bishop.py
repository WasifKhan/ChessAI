from src.backend.pieces.piece import Square
from src.backend.pieces.bishop import Bishop


moves = [
    ('bishop upper right diagonal white movement',
        ['D2 D4', 'D7 D5', 'C1 E3', 'C8 E6'],
        [Bishop(is_white=True, location=(4,2)),
         Bishop(is_white=False, location=(4, 5))]),
    ('Bishop white capture',
        ['E2 E4', 'E7 E6', 'F1 A6', 'F8 A3', 'A6 B7'],
        [Bishop(is_white=True, location=(1,6))]),
    ('Bishop black capture',
        ['E2 E4', 'E7 E6', 'F1 A6', 'F8 A3', 'A6 B7', 'A3 B2'],
        [Bishop(is_white=False, location=(1,1)),
         Square(location=(5,7))]),
]

