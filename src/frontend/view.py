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
        self.interface = interface
        self.versus_AI()
        self.squares = {}
        self.current_click = None

        window = tk.Tk()
        app = Window(window)
        window.wm_title('Beth Harmon')
        window.geometry('640x430')

        for row in range(8):
            window.columnconfigure(row, weight=1, minsize=75)
            window.rowconfigure(row, weight=1, minsize=50)
            for column in range(8):
                frame = tk.Frame(master=app,
                            relief=tk.RAISED,
                            borderwidth=4)
                frame.grid(row=7-row, column=column, padx=5, pady=5)
                piece = tk.Button(master=frame, text=f'({column}, {row})')
                piece['command'] = lambda r=piece: self.click_piece(r)
                piece.pack(padx=5, pady=5)
                self.squares[piece] = column * 10 + row
        window.mainloop()

    def click_piece(self, piece):
        if not self.current_click:
            self.current_click = self.squares[piece]
        else:
            self.interface.add_move(self.current_click, self.squares[piece])
            self.current_click = None

    def versus_AI(self):
        self.interface.versus_AI()

    def action(self, piece):
        self.interface.add_action(self.squares[piece])


