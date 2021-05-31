'''
Initialization of pieces on board
'''

from .rook import Rook
from .bishop import Bishop
from .knight import Knight
from .pawn import Pawn
from .queen import Queen
from .king import King

PIECES = \
{
    Rook(1, is_white=True, location=(0,0)),
    Rook(2, is_white=True, location=(7,0)),
    Knight(1, is_white=True, location=(1,0)),
    Knight(2, is_white=True, location=(6,0)),
    Bishop(1, is_white=True, location=(2,0)),
    Bishop(2, is_white=True, location=(5,0)),
    Queen(1, is_white=True, location=(3,0)),
    King(1, is_white=True, location=(4,0)),
    Pawn(1, is_white=True, location=(0,1)),
    Pawn(2, is_white=True, location=(1,1)),
    Pawn(3, is_white=True, location=(2,1)),
    Pawn(4, is_white=True, location=(3,1)),
    Pawn(5, is_white=True, location=(4,1)),
    Pawn(6, is_white=True, location=(5,1)),
    Pawn(7, is_white=True, location=(6,1)),
    Pawn(8, is_white=True, location=(7,1)),
    Rook(1, is_white=False, location=(0,7)),
    Rook(2, is_white=False, location=(7,7)),
    Knight(1, is_white=False, location=(1,7)),
    Knight(2, is_white=False, location=(6,7)),
    Bishop(1, is_white=False, location=(2,7)),
    Bishop(2, is_white=False, location=(5,7)),
    Queen(1, is_white=False, location=(3,7)),
    King(1, is_white=False, location=(4,7)),
    Pawn(1, is_white=False, location=(0,6)),
    Pawn(2, is_white=False, location=(1,6)),
    Pawn(3, is_white=False, location=(2,6)),
    Pawn(4, is_white=False, location=(3,6)),
    Pawn(5, is_white=False, location=(4,6)),
    Pawn(6, is_white=False, location=(5,6)),
    Pawn(7, is_white=False, location=(6,6)),
    Pawn(8, is_white=False, location=(7,6)),
}
