'''
View to host chess engine
'''


import tkinter as tk
from PIL import Image, ImageTk
from interface import Interface

CURRENT_AI = 2


class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        load = Image.open('./frontend/images/chess_board.png')
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


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

        root = tk.Tk()
        self.root = root
        app = Window(root)
        root.wm_title('Chess')
        root.geometry('840x770')
        white_king_photo = ImageTk.PhotoImage(file = \
                './frontend/images/pieces_image/king_white.png')
        black_king_photo = ImageTk.PhotoImage(file = \
                './frontend/images/pieces_image/king_black.png')
        white_queen_photo = ImageTk.PhotoImage(file = \
                './frontend/images/pieces_image/queen_white.png')
        black_queen_photo = ImageTk.PhotoImage(file = \
                './frontend/images/pieces_image/queen_black.png')


        for row in range(8):
            root.columnconfigure(row, weight=1, minsize=50)
            root.rowconfigure(row, weight=1, minsize=50)
            for column in range(8):
                frame = tk.Frame(master=app,
                            relief=tk.RAISED,
                            borderwidth=3)
                frame.grid(row=7-row, column=column, padx=9, pady=9)
                piece = tk.Button(master=frame, image=white_king_photo, width=50, height=50)
                piece['command'] = lambda r=piece: self.piece(r)
                piece.pack(padx=0, pady=0)
                self.squares[piece] = column * 10 + row

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


