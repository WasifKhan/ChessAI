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
# IE.
# ('bishop upper right diagonal white movement',
#        ['D2 D4', 'D7 D5', 'C1 E3', 'C8 E6'],
#        [Bishop(is_white=True, location=(4,2)),
#         Bishop(is_white=False, location=(4, 5))])

moves = pawn_moves + bishop_moves + rook_moves + knight_moves + queen_moves + king_moves
