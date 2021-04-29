from src.backend.pieces.piece import Square
from src.backend.pieces.knight import Knight


moves = [
    ('White Knight opener', 
        ['B1 C3'], 
        [Knight(is_white=True, location=(2,2)), 
         Square(location=(1,0))]),
    ('Black Knight capture', 
        ['D2 D4', 'A7 A6', 'C1 H6', 'G8 H6'],
        [Knight(is_white=False, location=(7,5)),
         Square(location=(6,7))]),
    ('White Knight invaild move',
        ['B1 D3'],
        [Knight(is_white=True, location=(1,0))]),
    ('White Knight capture',
        ['A2 A3', 'B8 C6', 'G1 F3', 'C6 D4', 'F3 D4'],
        [Knight(is_white=True, location=(3,3))]),
]

