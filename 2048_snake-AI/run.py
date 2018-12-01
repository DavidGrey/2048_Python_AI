"""Contains main loop for the AI"""
from board_functions import pp
from board_functions import make_board
from board_functions import num_empty
from board_functions import rand_tile
from board_functions import move

from brain import get_dir

BOARD = make_board()

#Main loop
while True:
    pp(BOARD)

    EMPTY = num_empty(BOARD)

    MAX_DEPTH = 1

    if EMPTY > 3:
        MAX_DEPTH = 1
    elif EMPTY > 1:
        MAX_DEPTH = 2



    if not dir:
        print "Game Over"
        break

    BOARD = rand_tile(move(BOARD, get_dir(BOARD, MAX_DEPTH)).shift())

    print '\n'
