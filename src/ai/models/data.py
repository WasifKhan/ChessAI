# Architecture for ChessAI

# Model: Q-Learning

'''
Pieces = 
{0: None, 1: Pawn, 2: Bishop, 3: Knight, 4: Rook, 5: Queen, 6: King}

Value = {Pawn: 1, Bishop: 3, Knight: 3, Rook: 5, Queen: 9, King: 100}

State Space:
8x8 integers representing pieces on board
ie. starting board = S_0 = [
[K, R, B, Q, K, B, R, K],
[P, P, P, P, P, P, P, P],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[P, P, P, P, P, P, P, P],
[K, R, B, Q, K, B, R, K],
]

Input Layer: 64 Neurons = S0 = [
[5, 3, 3, 9, 100, 3, 3, 5] * -1,
[1, 1, 1, 1, 1, 1, 1, 1] * -1,
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1],
[5, 3, 3, 9, 100, 3, 3, 5]
]

Output Layer = 124 Neurons = (16 Pawn Actions
                              + 28 Bishop Actions
                              + 16 Knight Actions
                              + 28 Rook Actions
                              + 28 Queen Actions
                              + 8 King Actions) =
PAWN
1 - P1 - Up 1
2 - P1 - Up 2
3 - P2 - Up 1
4 - P2 - Up 2
5 - P3 - Up 1
6 - P3 - Up 2
7 - P4 - Up 1
8 - P4 - Up 2
9 - P5 - Up 1
10 - P5 - Up 2
11 - P6 - Up 1
12 - P6 - Up 2
13 - P7 - Up 1
14 - P7 - Up 2
15 - P8 - Up 1
16 - P8 - Up 2

BISHOP
1 - B1 - +Slope to Index0
2 - B1 - +Slope to Index1
3 - B1 - +Slope to Index2
4 - B1 - +Slope to Index3
5 - B1 - +Slope to Index4
6 - B1 - +Slope to Index5
7 - B1 - +Slope to Index6
8 - B1 - -Slope to Index0
9 - B1 - -Slope to Index1
10 - B1 - -Slope to Index2
11 - B1 - -Slope to Index3
12 - B1 - -Slope to Index4
13 - B1 - -Slope to Index5
14 - B1 - -Slope to Index6

15 - B2 - +Slope to Index0
16 - B2 - +Slope to Index1
17 - B2 - +Slope to Index2
18 - B2 - +Slope to Index3
19 - B2 - +Slope to Index4
20 - B2 - +Slope to Index5
21 - B2 - +Slope to Index6
22 - B2 - +Slope to Index0
23 - B2 - -Slope to Index1
24 - B2 - -Slope to Index2
25 - B2 - -Slope to Index3
26 - B2 - -Slope to Index4
27 - B2 - -Slope to Index5
28 - B2 - -Slope to Index6

KNIGHT
1 - K1 - Up Right
2 - K1 - Right Up
3 - K1 - Right Down
4 - K1 - Down Right
5 - K1 - Down Left
6 - K1 - Left Down
7 - K1 - Left Up
8 - K1 - Up Left

9 - K2 - Up Right
10 - K2 - Right Up
11 - K2 - Right Down
12 - K2 - Down Right
13 - K2 - Down Left
14 - K2 - Left Down
15 - K2 - Left Up
16 - K2 - Up Left

ROOK
1 - R1 - Horizontal to Index0
2 - R1 - Horizontal to Index1
3 - R1 - Horizontal to Index2
4 - R1 - Horizontal to Index3
5 - R1 - Horizontal to Index4
6 - R1 - Horizontal to Index5
7 - R1 - Horizontal to Index6
8 - R1 - Vertical to Index0
9 - R1 - Vertical to Index1
10 - R1 - Vertical to Index2
11 - R1 - Vertical to Index3
12 - R1 - Vertical to Index4
13 - R1 - Vertical to Index5
14 - R1 - Vertical to Index6

15 - R2 - Horizontal to Index0
16 - R2 - Horizontal to Index1
17 - R2 - Horizontal to Index2
18 - R2 - Horizontal to Index3
19 - R2 - Horizontal to Index4
20 - R2 - Horizontal to Index5
21 - R2 - Horizontal to Index6
22 - R2 - Vertical to Index0
23 - R2 - Vertical to Index1
24 - R2 - Vertical to Index2
25 - R2 - Vertical to Index3
26 - R2 - Vertical to Index4
27 - R2 - Vertical to Index5
28 - R2 - Vertical to Index6

QUEEN
1 - Q - +Slope to Index0
2 - Q - +Slope to Index1
3 - Q - +Slope to Index2
4 - Q - +Slope to Index3
5 - Q - +Slope to Index4
6 - Q - +Slope to Index5
7 - Q - +Slope to Index6
8 - Q - -Slope to Index0
9 - Q - -Slope to Index1
10 - Q - -Slope to Index2
11 - Q - -Slope to Index3
12 - Q - -Slope to Index4
13 - Q - -Slope to Index5
14 - Q - -Slope to Index6

15 - Q - Horizontal to Index0
16 - Q - Horizontal to Index1
17 - Q - Horizontal to Index2
18 - Q - Horizontal to Index3
19 - Q - Horizontal to Index4
20 - Q - Horizontal to Index5
21 - Q - Horizontal to Index6
22 - Q - Vertical to Index0
23 - Q - Vertical to Index1
24 - Q - Vertical to Index2
25 - Q - Vertical to Index3
26 - Q - Vertical to Index4
27 - Q - Vertical to Index5
28 - Q - Vertical to Index6

KING
1 - K - Up Right
2 - K - Up
3 - K - Up Left
4 - K - Left
5 - K - Down Left
6 - K - Down
7 - K - Down Right
8 - K - Right
'''
