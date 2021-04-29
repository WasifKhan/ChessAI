from src.backend.pieces.piece import Square
from src.backend.pieces.pawn import Pawn
from src.backend.pieces.king import King


moves = [
    ('white king invalid move', 
        ['E1 E2'], 
        [Pawn(is_white=True, location=(1,4)),
         King(is_white=True, location=(0,4))]),
    ('white king valid move',
        ['E2 E4', 'E7 E5', 'E1 E2'],
        [Pawn(is_white=True, location=(3,4)),
         King(is_white=True, location=(1,4))]),
]

