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
        interface.set_player_names('Player 1', 'AI')
        scoreboard = interface.get_scoreboard()
        score = interface.get_score('Player 1', 'AI')
        play_again = interface.play_again(True)
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
                piece['command'] = lambda r=piece: self.click_piece(r)
                piece.pack(padx=5, pady=5)
                self.squares[piece] = column * 10 + row
        resign = tk.Frame(master=root, relief=tk.RAISED, borderwidth=6)
        resign.pack(side=tk.BOTTOM)
        resign_button = tk.Button(master=resign, text='Resign', fg='red')
        resign_button['command'] = lambda: self.click_resign()
        resign_button.pack(side=tk.BOTTOM)
        root.mainloop()

    def click_resign(self):
        self.interface.game_over(self.root)

    def click_piece(self, piece):
        if self.current_click:
            result = self.interface.add_move(self.current_click, self.squares[piece])
            self.current_click = None
            if self.interface.AI and self.interface.ai_move() is None:
                self.click_resign()
        else:
            self.current_click = self.squares[piece]


    def versus_AI(self):
        self.interface.versus_AI()

    def action(self, piece):
        self.interface.add_action(self.squares[piece])


