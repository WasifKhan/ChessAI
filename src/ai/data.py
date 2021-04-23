# Architecture for ChessAI

# Model: Q-Learning

'''
Pieces = 
{0: None, 1: Pawn, 2: Bishop, 3: Knight, 4: Rook, 5: Queen, 6: King}

State Space:
8x8 integers representing pieces on board
ie. starting board = [
[4, 3, 2, 6, 5, 2, 3, 4],
[1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1],
[4, 3, 2, 6, 5, 2, 3, 4]
]

'''
