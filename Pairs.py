from tkinter import *
from collections import defaultdict
from threading import Timer
import random


# generates list of 1-n number pairs
def genPairs(n):
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

    buttons[row][col].config(text=number, state='disabled', relief='flat')
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

    buttons[firstRow][firstCol].config(text='', state='normal', relief='raised')
    buttons[row][col].config(text='', state='normal', relief='raised')
    score += 1
    tries.config(text=['Tries:', score])


# Global variables
firstNum = 0
firstRow = 0
firstCol = 0
first = False
score = 0


root = Tk()
root.title('Pairs')

main = Frame(root)
main.pack(side='top', expand=True, fill=BOTH)

# creates 10x10 tiles in main frame
size = 10
buttons = defaultdict(list)
numList = scramble(genPairs(50))
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

# score board showing number of unsuccessful matches(tries)
board = Frame(root, height=30)
board.pack(side='bottom', fill=X)
tries = Label(board, text=['Tries:', score], font='arial')
tries.pack()

root.mainloop()
