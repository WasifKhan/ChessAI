from typing import MutableSequence
from src.backend.pieces.piece import Square
from src.backend.pieces.pawn import Pawn
from src.backend.pieces.king import King
from src.backend.pieces.rook import Rook
from src.backend.pieces.queen import Queen


moves = [
    ('white king invalid move', 
        ['E1 E2'], 
        [Pawn(is_white=True, location=(4,1)),
         King(is_white=True, location=(4,0))]),
    ('white king valid move',
        ['E2 E4', 'E7 E5', 'E1 E2'],
        [Pawn(is_white=True, location=(4,3)),
         King(is_white=True, location=(4,1)),
         Square(location=(4,0))]),
    ('White King Queen Side Caslte',
        ['D2 D4', 'A7 A6', 'C2 C4', 'H7 H6', 'D1 B3', 'D7 D6', 'C1 E3', 'G7 G6', 'B1 A3', 'G6 G5', 'E1 C1'],
        [King(is_white=True, location=(2,0)),
         Rook(is_white=True, location=(3,0)),
         Square(location=(0,0)),
         Square(location=(4,0))]),
    ('White King and Black King -King side caslte',
        ['G2 G4', 'G7 G5', 'F1 H3', 'F8 H6', 'G1 F3', 'G8 F6', 'E1 G1', 'E8 G8'],
        [King(is_white=True, location=(6,0)),
         Rook(is_white=True, location=(5,0)),
         Square(location=(7,0)),
         Square(location=(4,0)),
         King(is_white=False, location=(6,7)),
         Rook(is_white=False, location=(5,7)),
         Square(location=(4,7)),
         Square(location=(7,7))]),
    ('Black King Queen Side Castle',
        ['A2 A3', 'D7 D5', 'B2 B3', 'C7 C5', 'C2 C3', 'D8 B6', 'D2 D3', 'C8 E6', 'E2 E3', 'B8 A6', 'F2 F3', 'E8 C8'],
        [King(is_white=False, location=(2,7)),
         Rook(is_white=False, location=(3,7)),
         Square(location=(0,7)),
         Square(location=(3,7))]),
    ('White King move check',
        ['A2 A3', 'C7 C6', 'H2 H3', 'D8 A5', 'C2 C4'],
        [Pawn(is_white=True, location=(2,1)),
         Queen(is_white=False, location=(0,4)),
         King(is_white=True, location=(4,0))]),
    ('Black King move check',
        ['E2 E3', 'A7 A6', 'D1 H5', 'F7 F6'],
        [Pawn(is_white=False, location=(5,6)),
         Queen(is_white=True, location=(7,4)),
         King(is_white=False, location=(4,7))]),
    ('White King Caslte king Side Blocked',
        ['G1 H3', 'E7 E5', 'G2 G4', 'F8 C5', 'F2 F4', 'A7 A6', 'F1 G2', 'B7 B6', 'E1 G1'],
        [King(is_white=True, location=(4,0)),
         Rook(is_white=True, location=(7,0))]),
    ('White King Castle King Side Unblock',
        ['G1 H3', 'E7 E5', 'G2 G4', 'F8 C5', 'F2 F4', 'A7 A6', 'F1 G2', 'B7 B6', 'E2 E3', 'H7 H6', 'E1 G1'],
        [King(is_white=True, location=(6,0)),
         Rook(is_white=True, location=(5,0)),
         Square(location=(7,0)),
         Square(location=(4,0))])



]

