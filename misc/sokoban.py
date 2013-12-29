"""
Play Sokoban on the tty. (Use the arrow keys.)
"""

def parse(board_pic):
    lines = [line.strip() for line in board_pic.splitlines()]
    assert lines and all(len(line) == len(lines[0]) for line in lines)
    return len(lines[0]), list(''.join(lines))

def unparse((width, grid)):
    return '\r\n'.join(''.join(grid[i:i+width])
                       for i in range(0, len(grid), width))

def play(board):
    write(ansi_hide_cursor)
    while True:
        write(ansi_clear_screen + unparse(board))
        if won(board): break
        move = read_key()
        if move in 'qQxX': break
        if move in commands: push(board, commands[move])
    write(ansi_show_cursor)

def won((width, grid)): return 'o' not in grid

commands = dict(up   = lambda (width, grid): -width,
                down = lambda (width, grid):  width,
                left = lambda (width, grid): -2,
                right= lambda (width, grid):  2)

def push((width, grid), direction):
    "Update board, trying to move the player in the direction."
    i = grid.index('i' if 'i' in grid else 'I')
    d = direction((width, grid))
    move(grid, 'o@', i+d, i+d+d) # First push any neighboring box.
    move(grid, 'iI', i, i+d)

def move(grid, thing, src, dst):
    "Move thing from src to dst if possible."
    # N.B. dst is always in bounds when grid[src] in thing because our
    # boards have '#'-borders.
    if grid[src] in thing and grid[dst] in ' .':
        clear(grid, src)
        drop(grid, dst, thing)

def clear(grid, i):
    "Remove any thing (box or player) from position i."
    grid[i] = ' .'[grid[i] in '.@I']

def drop(grid, i, thing):
    "At a clear position, put thing."
    grid[i] = thing['.' == grid[i]]


# Terminal stuff

import os, sys

ansi_clear_screen = '\x1b[2J\x1b[H'
ansi_hide_cursor  = '\x1b[?25l'
ansi_show_cursor  = '\x1b[?25h'
write = sys.stdout.write

def with_raw(reacting):
    os.system('stty raw -echo')
    try:
        reacting()
    finally:
        os.system('stty sane')

esc = chr(27)
keys = {esc+'[A': 'up',   esc+'[C': 'right',
        esc+'[B': 'down', esc+'[D': 'left'}
key_prefixes = set(k[:i] for k in keys for i in range(1, len(k)))

def read_key():
    k = sys.stdin.read(1)
    while k in key_prefixes:
        k1 = sys.stdin.read(1)
        if not k1: break
        k += k1
    return keys.get(k, k)


if __name__ == '__main__':
    puzzle = """\
# # # # # # #
# . i   #   #
# o @   o   #
#       o   #
#   . .     #
#     @     #
# # # # # # #"""
    board = parse(puzzle)
    with_raw(lambda: play(board))