'''
View to host chess engine
'''

import tkinter as tk

class View:
    def __init__(self):
        window = tk.Tk()
        greeting = tk.Label(text='Welcome to Ali and Wasif Chess Engine',
                            foreground='white',
                            background='black',
                            width='40',
                            height=5)

        start = tk.Button(text='Start',
                          foreground='red',
                          background='green',
                          width=50,
                          height=50)
        greeting.pack()
        start.pack()
        window.mainloop()


