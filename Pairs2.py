import tkinter as tk
import random
from collections import defaultdict
from threading import Timer


class Menu:   # creates menu for selecting tile size and reseting tiles

    def __init__(self, root):
        self.tiles = None
        self.root = root
        self.options = [2, 4, 6, 8, 10, 12]
        self.menu = tk.Frame(self.root, height=30)
        self.menu.pack(side='top', fill=tk.X)
        # creates option list
        self.selected = tk.StringVar(self.menu)
        self.selected.set(self.options[4])
        self.optionList = tk.OptionMenu(self.menu, self.selected, *self.options, command=self.callback)
        self.optionList.config(width=10, bg='white', activebackground='white')
        self.optionList['menu'].config(bg='white')
        self.optionList.grid(row=0, column=1)
        # creates reset button
        self.resetButton = tk.Button(self.menu, text='Reset', command=lambda: self.reset())
        self.resetButton.grid(row=0, column=2, sticky=tk.W)
        # creates option list text
        self.menuLabel = tk.Label(self.menu, text='Size :')
        self.menuLabel.grid(row=0, column=0)

    # changes size to selected size
    def callback(self, selection):
        if self.tiles is not None:
            self.tiles.size = selection

    # resets tiles to selected size, clears score
    def reset(self):
        if self.tiles is not None:
            self.tiles.first = False
            self.tiles.main.destroy()
            self.tiles.main = self.tiles.genTiles()
            self.tiles.score = 0
            self.tiles.tries.config(text=['Tries:', self.tiles.score])


class Tiles:  # creates pair tiles and score board

    def __init__(self, root, size=10):
        self.root = root
        self.size = size
        self.firstNum = 0
        self.firstRow = 0
        self.firstCol = 0
        self.first = False
        self.score = 0
        self.buttons = defaultdict(list)
        # tiles
        self.main = self.genTiles()
        # score board
        self.board = tk.Frame(root, height=30)
        self.board.pack(side='bottom', fill=tk.X)
        self.tries = tk.Label(self.board, text=['Tries:', self.score], font='arial')
        self.tries.pack()

    # generates size by size array of tiles, returns its frame
    def genTiles(self):
        self.buttons = defaultdict(list)
        main = tk.Frame(self.root)
        main.pack(side='top', expand=True, fill=tk.BOTH)
        numList = self.scramble(self.genPairs(self.size * self.size / 2))
        c = 0
        for i in range(self.size):
            for j in range(self.size):
                btn = tk.Button(main, command=lambda row=i, col=j, number=numList[c]: self.match(row, col, number),
                                height=1, width=1)
                self.buttons[i].append(btn)
                btn.grid(row=i, column=j, sticky="wens")
                main.rowconfigure(i, weight=1)
                main.columnconfigure(j, weight=1)
                c += 1
        return main

    # generates list of 1-n number pairs
    @staticmethod
    def genPairs(n):
        n = int(n)
        pairs = []

        for i in range(1, n + 1):
            pairs.append(i)
            pairs.append(i)
        return pairs

    # scrambles list of pairs
    @staticmethod
    def scramble(pairs):
        scrambled = []

        while len(pairs) > 0:
            i = random.randint(0, len(pairs) - 1)
            scrambled.append(pairs.pop(i))
        return scrambled

    # reveals selected tiles and resets if numbers don't match
    def match(self, row, col, number):

        self.buttons[row][col].config(text=number, relief='flat', command=lambda: None)
        if not self.first:
            self.firstNum = number
            self.firstRow = row
            self.firstCol = col
            self.first = True
        elif number == self.firstNum:
            self.first = False
        else:
            t = Timer(0.5, self.resetTiles, [self.firstRow, self.firstCol, self.firstNum, row, col, number])
            t.start()
            self.first = False

    # resets tiles and increases tries by 1
    def resetTiles(self, firstRow, firstCol, firstNum, row, col, number):

        self.buttons[firstRow][firstCol].config(text='', relief='raised', command=
                                                lambda i=firstRow, j=firstCol, n=firstNum: self.match(i, j, n))
        self.buttons[row][col].config(text='', relief='raised', command=
                                        lambda i=row, j=col, n=number: self.match(i, j, n))
        self.score += 1
        self.tries.config(text=['Tries:', self.score])


# creates window
root = tk.Tk()
root.title('Pairs')
root.geometry('300x350')

menu = Menu(root)
menu.tiles = Tiles(root, 10)

root.mainloop()
