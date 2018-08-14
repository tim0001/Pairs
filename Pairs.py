from tkinter import *
from collections import defaultdict
from threading import Timer
import random


# generates list of 1-n number pairs
def genPairs(n):
    n = int(n)
    pairs = []

    for i in range(1, n+1):
        pairs.append(i)
        pairs.append(i)
    return pairs


# scrambles list of pairs
def scramble(pairs):
    scrambled = []

    while len(pairs) > 0:
        i = random.randint(0, len(pairs) - 1)
        scrambled.append(pairs.pop(i))
    return scrambled


# reveals selected tiles and resets if numbers don't match
def match(row, col, number):
    global first
    global firstNum
    global firstRow
    global firstCol

    buttons[row][col].config(text=number, relief='flat', command=lambda:None)
    if not first:
        firstNum = number
        firstRow = row
        firstCol = col
        first = True
    elif number == firstNum:
        first = False
    else:
        t = Timer(0.5, reset, [firstRow, firstCol, firstNum, row, col, number])
        t.start()
        first = False


# resets tiles and increases tries by 1
def reset(firstRow, firstCol, firstNum, row, col, number):
    global score

    buttons[firstRow][firstCol].config(text='', relief='raised', command=
                                        lambda i=firstRow, j=firstCol, n=firstNum: match(i, j, n))
    buttons[row][col].config(text='', relief='raised', command=
                                        lambda i=row, j=col, n=number: match(i, j, n))
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
    numList = scramble(genPairs(size*size/2))
    c = 0
    for i in range(size):
        for j in range(size):
            btn = Button(main, command=lambda row=i, col=j, number=numList[c]: match(row, col, number),
                         height=1, width=1)
            buttons[i].append(btn)
            btn.grid(row=i, column=j, sticky="wens")
            main.rowconfigure(i, weight=1)
            main.columnconfigure(j, weight=1)
            c += 1
    return main


# change size to one selected in menu
def callback(selection):
    global size

    size = selection


# resets tiles to selected size, clears score
def resetTiles():
    global size
    global main
    global score
    global first

    first = False
    main.destroy()
    genTiles()
    score =0
    tries.config(text=['Tries:', score])


# Global variables
firstNum = 0
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
root.geometry('300x350')

# create menu for selecting tile size and reseting tiles
options = [2, 4, 6, 8, 10, 12]
menu = Frame(root, height=30)
menu.pack(side='top', fill=X)
selected = StringVar(menu)
selected.set(options[4])
optionList = OptionMenu(menu, selected, *options, command=callback)
optionList.config(width=10, bg='white', activebackground='white')
optionList['menu'].config(bg='white')
optionList.grid(row=0, column=1)
resetButton = Button(menu, text='Reset', command=lambda: resetTiles())
resetButton.grid(row=0, column=2, sticky=W)
menuLabel = Label(menu, text='Size :')
menuLabel.grid(row=0, column=0)

# creates tiles
genTiles()

# score board showing number of unsuccessful pairings
board = Frame(root, height=30)
board.pack(side='bottom', fill=X)
tries = Label(board, text=['Tries:', score], font='arial')
tries.pack()

root.mainloop()
