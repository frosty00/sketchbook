"""
Modeled after https://github.com/fewf/curtsies_2048
"""

import random

import sturm

def main():
    board = make_board()
    with sturm.cbreak_mode():
        while True:
            if is_full(board):  message = "You lose!"
            elif is_won(board): message = "You win!"
            else:               message = ""
            sturm.render("Use the arrow keys or 'q' to quit.\n\n"
                         + view(board) + "\n\n"
                         + message + "\n")
            if message: break
            key = sturm.get_key()
            if key == 'q': break
            elif key in globals(): # Hacky hacky, sorry. :P
                board2 = globals()[key](board)
                if board2 != board:
                    board = plop(board2, 2 if random.random() < .9 else 4)

# A board is a tuple of rows;
# a row is a tuple of values;
# a value is 0 for empty, or a positive number.

def make_board(): return plop(plop(empty_board, 2), 2)

empty_board = ((0,)*4,)*4

# Pre: not is_full(board)
def plop(board, v):
    while True:
        r, c = random.randint(0, 3), random.randint(0, 3)
        if board[r][c] == 0:
            return update(board, r, c, v)

def update(board, nr, nc, nv):
    return tuple(tuple(nv if (r,c) == (nr,nc) else v
                       for c, v in enumerate(row))
                 for r, row in enumerate(board))

def view(board):
    return '\n\n'.join(' '.join(('%d' % v if v else '.').center(4)
                                for v in row)
                       for row in board)

## print(view(update(empty_board, 3, 2, 4)))
#.  .    .    .    .  
#. 
#.  .    .    .    .  
#. 
#.  .    .    .    .  
#. 
#.  .    .    4    .  

def is_full(board): return all(all(row) for row in board)
def is_won(board): return any(any(v == 2048 for v in row) for row in board)

# Arrow-key actions:
def left(board):  return tuple(map(collapse, board))
def right(board): return fliph(left(fliph(board)))
def up(board):    return flipd(left(flipd(board)))
def down(board):  return flipd(right(flipd(board)))

def flipv(board): return board[::-1]                # vertical flip
def flipd(board): return tuple(zip(*board))         # diagonal
def fliph(board): return flipd(flipv(flipd(board))) # horizontal

def collapse(row):
    xs, ys = [], []
    for v in filter(None, row):
        if ys == [v]:
            xs.append(2*v)
            ys = []
        else:
            xs.extend(ys)
            ys = [v]
    xs.extend(ys)
    return tuple(xs) + (0,) * (4 - len(xs))

## collapse((0, 0, 0, 0))
#. (0, 0, 0, 0)
## collapse((0, 0, 0, 2))
#. (2, 0, 0, 0)
## collapse((0, 2, 0, 2))
#. (4, 0, 0, 0)
## collapse((0, 2, 4, 4))
#. (2, 8, 0, 0)
## collapse((0, 2, 2, 4))
#. (4, 4, 0, 0)
## collapse((2, 2, 2, 4))
#. (4, 2, 4, 0)
## collapse((2, 2, 4, 4))
#. (4, 8, 0, 0)

if __name__ == '__main__':
    main()
