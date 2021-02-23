from src.backend.piece import Pawn, Square
'''
result = 1 of:
{'state': list[Piece]}
{'status': {1, 0}}
'''

moves = {'vertical_double':(['A2 A4', 'A7 A5', 'A4 A5'], {'status':1}),
         #'vertical_single':['A2 A3', 'D7 D6', 'B2 B3', 'E7 E6'],
         'capture':(['B2 B4', 'C7 C5', 'B4 C5'], {'state': [Pawn(is_white=True, location=(2,4)), Square(location=(1,3))]}),
         #'en passant white':['C2 C4', 'H7 H6','C4 C5', 'D7 D5', 'C5 D6'],
         #'en passant black':['A2 A3', 'C7 C5', 'A3 A4', 'C5 C4', 'D2 D4', 'C4 D3'],
         #'bishop capture':['D2 D4', 'A7 A5', 'C1 D2', 'B7 B6', 'D2 E3', 'C7 C6', 'E3 F4', 'G7 G5', 'F4 G5'],
}
 
