from tkinter import *
from collections import defaultdict
from threading import Timer
import random


# generates list of 1-n number pairs
def genPairs(n):
    global mode
    n = int(n)
    pairs = []
    if mode == 'number':
        pairs = [i for i in range(1, n + 1) for j in (0, 1)]
        return pairs
    elif mode == 'color':
        for i in range(1, n + 1):
            c = '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pairs.append(c)
            pairs.append(c)
        return pairs


# scrambles list of pairs
def scramble(pairs):
    scrambled = []

    while len(pairs) > 0:
        i = random.randint(0, len(pairs) - 1)
        scrambled.append(pairs.pop(i))
    return scrambled


# reveals selected tiles and resets if numbers don't match
def match(row, col, x):
    global mode
    global first
    global firstVal
    global firstRow
    global firstCol

    if mode == 'number':
        buttons[row][col].config(text=x, relief='flat', command=lambda: None)
    elif mode == 'color':
        buttons[row][col].config(bg=x, relief='flat', command=lambda: None)
    if not first:
        firstVal = x
        firstRow = row
        firstCol = col
        first = True
    elif x == firstVal:
        first = False
    else:
        t = Timer(0.5, reset, [firstRow, firstCol, firstVal, row, col, x])
        t.start()
        first = False


# resets tiles and increases tries by 1
def reset(firstRow, firstCol, firstVal, row, col, x):
    global score
    global mode

    if mode == 'number':
        buttons[firstRow][firstCol].config(text='', relief='raised', command=
                                            lambda i=firstRow, j=firstCol, n=firstVal: match(i, j, n))
        buttons[row][col].config(text='', relief='raised', command=
                                            lambda i=row, j=col, n=x: match(i, j, n))
    elif mode == 'color':
        buttons[firstRow][firstCol].config(bg='SystemButtonFace', relief='raised', command=
                                            lambda i=firstRow, j=firstCol, n=firstVal: match(i, j, n))
        buttons[row][col].config(bg='SystemButtonFace', relief='raised', command=
                                            lambda i=row, j=col, n=x: match(i, j, n))
    score += 1
    tries.config(text=['Tries:', score])


# generates square array of tiles and returns its container
def genTiles():
    global size
    global main
    global buttons
    buttons = defaultdict(list)
    main = Frame(root)
    main.pack(side='top', expand=True, fill=BOTH)
    value = scramble(genPairs(size*size/2))
    c = 0
    for i in range(size):
        for j in range(size):
            btn = Button(main, command=lambda row=i, col=j, x=value[c]: match(row, col, x),
                         height=1, width=1)
            buttons[i].append(btn)
            btn.grid(row=i, column=j, sticky="wens")
            main.rowconfigure(i, weight=1)
            main.columnconfigure(j, weight=1)
            c += 1
    return main


# change size to selected
def callback(selection):
    global size

    size = selection


# resets tiles to selected size, clears score
def resetTiles():
    global main
    global score
    global first
    global mode

    first = False
    main.destroy()
    mode = choice.get()
    genTiles()
    score = 0
    tries.config(text=['Tries:', score])


# Global variables
mode = 'number'
firstVal = 0
firstRow = 0
firstCol = 0
first = False
score = 0
size = 10
main = None
buttons = defaultdict(list)


# creating window
root = Tk()
root.title('Pairs')
root.geometry('450x450')

# create menu for selecting tile size and reseting tiles
menu = Frame(root, height=30)
menu.pack(side='top', fill=X)

sizeLabel = Label(menu, text='Size :')
sizeLabel.grid(row=0, column=0)

options = [2, 4, 6, 8, 10, 12]
number = StringVar(menu)
number.set(options[4])
sizeList = OptionMenu(menu, number, *options, command=callback)
sizeList.config(width=10, bg='white', activebackground='white')
sizeList['menu'].config(bg='white')
sizeList.grid(row=0, column=1, sticky='w')
menu.columnconfigure(1, weight=2)

modeLabel = Label(menu, text='Mode :')
modeLabel.grid(row=0, column=2)


tileMode = ['number', 'color']
choice = StringVar(menu)
choice.set(tileMode[0])
ModeList = OptionMenu(menu, choice, *tileMode)
ModeList.config(width=10, bg='white', activebackground='white')
ModeList['menu'].config(bg='white')
ModeList.grid(row=0, column=3, sticky='w')
menu.columnconfigure(3, weight=2)

resetButton = Button(menu, text='Reset', command=lambda: resetTiles())
resetButton.grid(row=0, column=4, sticky='wens')
menu.columnconfigure(4, weight=1)


# creates tiles
genTiles()

# score board showing number of unsuccessful pairings
board = Frame(root, height=30)
board.pack(side='bottom', fill=X)
tries = Label(board, text=['Tries:', score], font='arial')
tries.pack()

root.mainloop()
