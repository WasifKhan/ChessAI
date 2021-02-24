from src.backend.piece import Bishop, Square

moves = [
    ('bishop upper right diagonal white movement',
        ['D2 D4', 'D7 D5', 'C1 E3', 'C8 E6'],
        [Bishop(is_white=True, location=(4,2)),
         Bishop(is_white=False, location=(4, 5))]),
       
]