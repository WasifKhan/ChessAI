'''
View to host chess engine
'''


import tkinter as tk
from PIL import Image, ImageTk
from interface import Interface

CURRENT_AI = 2





class View:
    def __init__(self):
        self.interface = Interface()
        '''
        The following code should be in buttons initiated by the user.
        Currently store here until calls are done
        '''
        self.interface.set_player_names('Player 1', 'Player 2')
        scoreboard = self.interface.get_scoreboard()
        score = self.interface.get_score('Player 1', 'Player 2')
        '''
        End of code that should be inside buttons.
        The code below belongs in init
        '''
        self.squares = {}
        self.current_click = None

        def create_chessboard(canvas):
            squares = [("white" if (row + col) % 2 == 0 else "grey") \
                    for row in range(8) for col in range(8)]
            for i, color in enumerate(squares):
                x1 = (i % 8) * 75
                y1 = (i // 8) * 75
                x2 = x1 + 75
                y2 = y1 + 75
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

        def place_piece(canvas, root, image_file, x, y, piece_id):
            photo = ImageTk.PhotoImage(file = image_file)
            image_id = canvas.create_image(x, y, anchor="nw", image=photo, tags=piece_id)
            canvas.tag_bind(image_id, '<Button-1>', lambda event, id=image_id: on_piece_click(event, id))
            return photo  # return to keep a reference


        def on_piece_click(event, piece_id):
            nonlocal source 
            if source is None:
                source = ((525-event.x)//75)*10 + ((525-event.y)//75)

                print(f"Selected {piece_id}")
            else:
                destination = ((event.x-525)//75)*10 + ((525-event.y)//75)
                if self.interface.add_move(source, destination):
                    canvas.coords(selected_piece, move_x, move_y)
                    print(f"Moved {selected_piece} to ({move_x}, {move_y})")
                else:
                    print("Illegal move")
                source = None  # Reset for the next selection

        def get_legal_moves(piece_id):
            # Dummy function, replace with actual backend call
            # This should return a list of tuples (x, y) representing legal move coordinates
            return [(120, 120), (180, 180)]  # Example legal moves

        def make_move(piece_id, new_x, new_y):
            # Dummy function, replace with actual backend call
            print(f"Moved {piece_id} to ({new_x}, {new_y})")

        root = tk.Tk()
        self.root = root
        root.wm_title('Chess')
        root.geometry('840x770')
        canvas = tk.Canvas(root, width=700, height=700)
        canvas.pack()
        create_chessboard(canvas)
        source = None
        images = []
        
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/rook_black.png', 0, 0, 1))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/knight_black.png', 75, 0, 2))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/bishop_black.png', 150, 0, 3))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/queen_black.png', 225, 0, 4))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/king_black.png', 300, 0, 5))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/bishop_black.png', 375, 0, 6))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/knight_black.png', 450, 0, 7))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/rook_black.png', 525, 0, 8))

        images.append(place_piece(canvas, root, './frontend/images/pieces_image/rook_white.png', 0, 525, 9))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/knight_white.png', 75, 525, 10))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/bishop_white.png', 150, 525, 11))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/queen_white.png', 225, 525, 12))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/king_white.png', 300, 525, 13))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/bishop_white.png', 375, 525, 14))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/knight_white.png', 450, 525, 15))
        images.append(place_piece(canvas, root, './frontend/images/pieces_image/rook_white.png', 525, 525, 16))

        [images.append(place_piece(canvas, root, './frontend/images/pieces_image/pawn_black.png', i * 75, 75, 17+i)) for i in range(8)]
        [images.append(place_piece(canvas, root, './frontend/images/pieces_image/pawn_white.png', i * 75, 450, 25+i)) for i in range(8)]


        btm_frame = tk.Frame(master=root, relief=tk.RAISED, borderwidth=6)
        btm_frame.pack(side=tk.BOTTOM)
        resign_button = tk.Button(master=btm_frame, text='Resign', fg='red')
        resign_button['command'] = lambda: self.resign()
        resign_button.pack(side=tk.LEFT)

        sim_games_button = tk.Button(master=btm_frame, text='Simulate Games', fg='blue')
        sim_games_button['command'] = lambda: self.simulate_games()
        sim_games_button.pack(side=tk.LEFT)

        play_again_button = tk.Button(master=btm_frame, text='Play Again', fg='orange')
        play_again_button['command'] = lambda: self.play_again()
        play_again_button.pack(side=tk.LEFT)

        train_ai_button = tk.Button(master=btm_frame, text='Train AI', fg='green')
        train_ai_button['command'] = lambda: self.train_AI()
        train_ai_button.pack(side=tk.LEFT)

        versus_random_ai_button = tk.Button(master=btm_frame, text='Load Easy AI', fg='green')
        versus_random_ai_button['command'] = lambda: self.versus_random_AI()
        versus_random_ai_button.pack(side=tk.LEFT)

        versus_current_ai_button = tk.Button(master=btm_frame, text='Load Hard AI', fg='green')
        versus_current_ai_button['command'] = lambda: self.versus_current_AI()
        versus_current_ai_button.pack(side=tk.LEFT)

        root.mainloop()

    def train_AI(self):
        self.interface.train_AI()

    def simulate_games(self):
        self.interface.simulate_games(10)

    def play_again(self):
        self.interface.play_again()

    def resign(self):
        self.interface.game_over()

    def piece(self, piece):
        if self.current_click:
            if (result := self.interface.add_move(self.current_click, self.squares[piece])):
                if self.interface.versus_ai and not self.interface.ai_move(False):
                    self.resign()
                    return
                print(self.interface)
            self.current_click = None
        else:
            self.current_click = self.squares[piece]

    def versus_random_AI(self):
        self.interface.versus_AI(0)
        print('\nDone Loading\nClick Play Again.\n')

    def versus_current_AI(self):
        self.interface.versus_AI(CURRENT_AI)
        print('\nDone Loading\nClick Play Again.\n')

    def action(self, piece):
        self.interface.add_action(self.squares[piece])


