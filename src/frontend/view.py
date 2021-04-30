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
        #load = Image.open('./frontend/images/bg_chessboard.png')
        #render = ImageTk.PhotoImage(load)
        #img = tk.Label(self, image=render)
        #img.image = render
        #img.place(x=0, y=0)


class View:
    def print_piece(self):
        print('test')

    def __init__(self):
        window = tk.Tk()
        app = Window(window)
        window.wm_title('Beth Harmon')
        window.geometry('1080x720')

        for row in range(7, -1, -1):
            window.columnconfigure(row, weight=1, minsize=75)
            window.rowconfigure(row, weight=1, minsize=50)
            for column in range(8):
                frame = tk.Frame(master=app,
                            relief=tk.RAISED,
                            borderwidth=4)
                frame.grid(row=7-row, column=column, padx=5, pady=5)
                piece = tk.Button(master=frame, text=f'({row}, {column})',
                        command=self.print_piece)
                piece.pack(padx=5, pady=5)
        window.mainloop()
