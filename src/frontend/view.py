'''
View to host chess engine
'''

import tkinter as tk
from PIL import Image, ImageTk



class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        load = Image.open('./frontend/images/bg_chessboard.png')
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


class View:
    def __init__(self, interface):
        '''
        The following code should be in buttons initiated by the user.
        Currently store here until calls are done
        '''
        interface.versus_AI()
        interface.set_player_names('Player 1', 'Black AI')
        scoreboard = interface.get_scoreboard()
        score = interface.get_score('Player 1', 'Black AI')
        '''
        End of code that should be inside buttons.
        The code below belongs in init
        '''
        self.interface = interface
        self.squares = {}
        self.current_click = None

        root = tk.Tk()
        self.root = root
        app = Window(root)
        root.wm_title('Beth Harmon')
        root.geometry('640x470')

        for row in range(8):
            root.columnconfigure(row, weight=1, minsize=75)
            root.rowconfigure(row, weight=1, minsize=50)
            for column in range(8):
                frame = tk.Frame(master=app,
                            relief=tk.RAISED,
                            borderwidth=4)
                frame.grid(row=7-row, column=column, padx=5, pady=5)
                piece = tk.Button(master=frame, text=f'({column}, {row})')
                piece['command'] = lambda r=piece: self.piece(r)
                piece.pack(padx=5, pady=5)
                self.squares[piece] = column * 10 + row
        btm_frame = tk.Frame(master=root, relief=tk.RAISED, borderwidth=6)
        btm_frame.pack(side=tk.BOTTOM)
        resign_button = tk.Button(master=btm_frame, text='Resign', fg='red')
        resign_button['command'] = lambda: self.resign()
        resign_button.pack(side=tk.LEFT)

        sim_games_button = tk.Button(master=btm_frame, text='Simulate Games', fg='blue')
        sim_games_button['command'] = lambda: self.simulate_games()
        sim_games_button.pack(side=tk.LEFT)

        play_again_button = tk.Button(master=btm_frame, text='Play Again', fg='green')
        play_again_button['command'] = lambda: self.play_again()
        play_again_button.pack(side=tk.LEFT)

        root.mainloop()

    def simulate_games(self):
        self.interface.simulate_games(100)

    def play_again(self):
        self.interface.play_again()

    def resign(self):
        self.interface.game_over()

    def piece(self, piece):
        if self.current_click:
            if (result := self.interface.add_move(self.current_click, self.squares[piece])):
                if self.interface.versus_ai and self.interface.ai_move(False) is None:
                    self.resign()
                    return
                print(self.interface)
            self.current_click = None
        else:
            self.current_click = self.squares[piece]

    def versus_AI(self):
        self.interface.versus_AI()

    def action(self, piece):
        self.interface.add_action(self.squares[piece])


