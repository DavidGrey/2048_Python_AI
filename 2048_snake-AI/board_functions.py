"""General board mechanics for 2048"""
from __future__ import division
from random import randint, choice
from copy import deepcopy


class move(object):
    """Class for shifting 2048 states"""
    def __init__(self, state, direction):
        self.state = state
        self.direction = direction

    def right(self):
        """Shifts the argument state to the right"""
        start = self.state
        new = []
        for row in self.state:
            new_row = []
            new_row.append([tile for tile in row if tile != 0])
            new.append([0]*(4-len(new_row[0]))+new_row[0])
        self.state = []
        for row in new:
            for i in range(2, -1, -1):
                if row[i] == row[i+1]:
                    row[i+1] = row[i]*2
                    row[i] = 0
            self.state.append(row)
        new = []
        for row in self.state:
            new_row = []
            new_row.append([tile for tile in row if tile != 0])
            new.append([0]*(4-len(new_row[0]))+new_row[0])
        if start == new:
            return False
        return new


    def left(self):
        """Shifts the argument state to the left"""
        new_state = move([row[::-1] for row in self.state], 'd').right()
        if new_state and (new_state != self.state):
            return [row[::-1] for row in new_state]
        else:
            return False


    def up(self):
        """Shifts the argument state up"""
        new_state = []
        for i in range(4):
            new_row = []
            for row in self.state:
                new_row.append(row[i])
            new_state.append(new_row[::-1])

        new_state = move(new_state, 'd').right()
        if not new_state:
            return False
        self.state = []
        for i in range(3, -1, -1):
            new_row = []
            for row in new_state:
                new_row.append(row[i])
            self.state.append(new_row)
        return self.state


    def down(self):
        """Shifts the argument state down"""
        new_state = []
        for i in range(4):
            new_state.append([row[i] for row in self.state][::-1])

        new_state = move(new_state, 'a').left()

        if not new_state:
            return False
        self.state = []
        for i in range(3, -1, -1):
            self.state.append([row[i] for row in new_state])
        return self.state

    def shift(self):
        """Format move(state, dir).shift()"""
        if self.direction == 'w':
            return move(self.state, self.direction).up()
        elif self.direction == 'a':
            return move(self.state, self.direction).left()
        elif self.direction == 's':
            return move(self.state, self.direction).down()
        elif self.direction == 'd':
            return move(self.state, self.direction).right()


def make_board():
    """Returns a random starting board"""
    board = [[0 for i in range(4)] for x in range(4)]
    board[randint(0, 3)][randint(0, 3)] = choice([2]*9+[4])
    while True:
        row = randint(0, 3)
        col = randint(0, 3)
        if board[row][col] == 0:
            board[row][col] = choice([2]*9+[4])
            return board


def rand_tile(state):
    """Takes a single state as input, places a tile
    (2 90% of the time and a 4 the rest) on it at random,
     and returns the state"""
    zeros = []
    for row in range(4):
        for tile in range(4):
            try:
                if state[row][tile] == 0:
                    zeros.append((row, tile))
            except:
                return state
    if not zeros:
        return False
    spawn = choice(zeros)
    state[spawn[0]][spawn[1]] = choice([2]*9+[4])
    return state


def pp(board):
    """Prints a formated version of the argment state"""
    for row in board:
        nrow = '|'
        for i in row:
            if i != 0:
                nrow += str(i) + ' |'
            else:
                nrow += '__|'
        print nrow
    print '\n'*2


def all_rand_tiles(state):
    """Takes a single state as argument and returns a list
     of all the states the could result from the rand_tile function
      being run on the arugment state"""
    states = [[], []]
    changed = list()
    old_states = [None]
    while old_states != states:
        old_states = states
        new_state = deepcopy(state)
        for row in range(4):
            for tile in range(4):
                if state[row][tile] == 0:
                    if [row, tile] not in changed:
                        new_state[row][tile] = 2
                        states[0].append(new_state)
                        new_state = deepcopy(state)
                        new_state[row][tile] = 4
                        states[1].append(new_state)
                        new_state = deepcopy(state)
                        changed.append([row, tile])
    return states


def successors(state, dirs=['w', 'a', 's', 'd']):
    """Returns a dictionary with directions as key
     and possible game states as values"""
    #Should make the "if moved" part of the if statements nested
    states = [[], []]
    for direction in dirs:
        moved = move(state, direction).shift()
        if moved:
            states[0] += all_rand_tiles(moved)[0]
            states[1] += all_rand_tiles(moved)[1]

    if states != [[], []]:
        return states


def num_empty(state):
    """Takes a game-state as input
    and returns the number of empty cells in that state"""
    return sum([row.count(0) for row in state])
