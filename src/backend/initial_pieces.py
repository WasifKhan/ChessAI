'''
Initialization of pieces on board
'''

from .pieces.rook import Rook
from .pieces.bishop import Bishop
from .pieces.knight import Knight
from .pieces.pawn import Pawn
from .pieces.queen import Queen
from .pieces.king import King

PIECES = \
{
    Rook(is_white=True, location=(0,0)),
    Rook(is_white=True, location=(7,0)),
    Knight(is_white=True, location=(1,0)),
    Knight(is_white=True, location=(6,0)),
    Bishop(is_white=True, location=(2,0)),
    Bishop(is_white=True, location=(5,0)),
    Queen(is_white=True, location=(3,0)),
    King(is_white=True, location=(4,0)),
    Pawn(is_white=True, location=(0,1)),
    Pawn(is_white=True, location=(1,1)),
    Pawn(is_white=True, location=(2,1)),
    Pawn(is_white=True, location=(3,1)),
    Pawn(is_white=True, location=(4,1)),
    Pawn(is_white=True, location=(5,1)),
    Pawn(is_white=True, location=(6,1)),
    Pawn(is_white=True, location=(7,1)),
    Rook(is_white=False, location=(0,7)),
    Rook(is_white=False, location=(7,7)),
    Knight(is_white=False, location=(1,7)),
    Knight(is_white=False, location=(6,7)),
    Bishop(is_white=False, location=(2,7)),
    Bishop(is_white=False, location=(5,7)),
    Queen(is_white=False, location=(3,7)),
    King(is_white=False, location=(4,7)),
    Pawn(is_white=False, location=(0,6)),
    Pawn(is_white=False, location=(1,6)),
    Pawn(is_white=False, location=(2,6)),
    Pawn(is_white=False, location=(3,6)),
    Pawn(is_white=False, location=(4,6)),
    Pawn(is_white=False, location=(5,6)),
    Pawn(is_white=False, location=(6,6)),
    Pawn(is_white=False, location=(7,6)),
}
