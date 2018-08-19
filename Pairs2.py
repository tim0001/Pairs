import tkinter as tk
import random
from collections import defaultdict
from threading import Timer


class Tiles:

    def __init__(self, root, size=10):
        self.root = root
        self.size = size
        self.firstNum = 0
        self.firstRow = 0
        self.firstCol = 0
        self.first = False
        self.score = 0
        self.buttons = defaultdict(list)
        self.main = self.genTiles()

    # generates square array of tiles and returns its container
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
        tries.config(text=['Tries:', self.score])


# change size to one selected in menu
def callback(selection):
    tiles.size = selection


# resets tiles to selected size, clears score
def reset():
    tiles.first = False
    tiles.main.destroy()
    tiles.main = tiles.genTiles()
    tiles.score = 0
    tries.config(text=['Tries:', tiles.score])


# create window
root = tk.Tk()
root.title('Pairs')
root.geometry('300x350')

# create menu for selecting tile size and reseting tiles
options = [2, 4, 6, 8, 10, 12]
menu = tk.Frame(root, height=30)
menu.pack(side='top', fill=tk.X)
selected = tk.StringVar(menu)
selected.set(options[4])
optionList = tk.OptionMenu(menu, selected, *options, command=callback)
optionList.config(width=10, bg='white', activebackground='white')
optionList['menu'].config(bg='white')
optionList.grid(row=0, column=1)
resetButton = tk.Button(menu, text='Reset', command=lambda: reset())
resetButton.grid(row=0, column=2, sticky=tk.W)
menuLabel = tk.Label(menu, text='Size :')
menuLabel.grid(row=0, column=0)

tiles = Tiles(root, 10)

# score board showing number of unsuccessful pairings
board = tk.Frame(root, height=30)
board.pack(side='bottom', fill=tk.X)
tries = tk.Label(board, text=['Tries:', tiles.score], font='arial')
tries.pack()

root.mainloop()
