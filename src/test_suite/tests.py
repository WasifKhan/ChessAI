from .pieces_test_cases.pawn_tests import moves as pawn_moves
from .pieces_test_cases.bishop_tests import moves as bishop_moves
from .pieces_test_cases.rook_tests import moves as rook_moves
from .pieces_test_cases.knight_tests import moves as knight_moves
from .pieces_test_cases.queen_tests import moves as queen_moves
from .pieces_test_cases.king_tests import moves as king_moves

# (a,b,c)
# a = str 
# the name of the test
# b = list
# list of the moves for the game
# c = list
# list of Pieces (where you expect them to be after)


moves = pawn_moves + bishop_moves + rook_moves + knight_moves + queen_moves + king_moves
    #'vertical_single':['A2 A3', 'D7 D6', 'B2 B3', 'E7 E6'],
    #'en passant white':['C2 C4', 'H7 H6','C4 C5', 'D7 D5', 'C5 D6'],
    #'en passant black':['A2 A3', 'C7 C5', 'A3 A4', 'C5 C4', 'D2 D4', 'C4 D3'],
    #'bishop capture':['D2 D4', 'A7 A5', 'C1 D2', 'B7 B6', 'D2 E3', 'C7 C6', 'E3 F4', 'G7 G5', 'F4 G5'],
