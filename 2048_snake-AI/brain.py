"""Recursive ranking functions"""
from __future__ import division
from board_functions import successors
from board_functions import num_empty


def rank_branch(state, max_depth, prob=1, curr_depth=0):
    """Takes a single game-state as input and returns the total
    score of the input state + the score of all successors states
    within the search depth"""
    if curr_depth == max_depth or prob < .0001:
        return rank_state(state)*prob
    children = successors(state)
    if not children:
        return rank_state(state)*prob

    total = (rank_state(state)*prob)
    weights = {0:.9, 1:.1}
    for section in weights:
        for board in children[section]:
            total += rank_branch(board, max_depth,
                                 prob*(weights[section]*(1/(num_empty(board)+1))), curr_depth+1)
    return total


def get_dir(state, max_depth):
    """Takes a single game-state and and a maximum
    search depth as input and outputs the AI's preferred move('W', 'A', 'S', 'D')"""
    paths = {'w':1, 'a':1, 's':1, 'd':1}
    for direction in paths:
        children = successors(state, direction)
        if children:
            prob = {0:9/(len(children[0])*9)+len(children[1]),
                    1:1/(len(children[0])*9)+len(children[1])}
            children = [children[0][:10], children[1][:10]]
            for section in prob:
                for board in children[section]:
                    paths[direction] += rank_branch(board, max_depth,
					                                prob[section]*(1/(num_empty(board)+1)))
        else:
            paths[direction] = False


    max_score = False
    best_direction = False
    for direction in paths:
        curr_score = paths[direction]
        if curr_score:
            if curr_score > max_score or max_score == False:
                max_score = curr_score
                best_direction = direction
    return best_direction


def rank_state(state):
    """Takes a single game-state as input
    and returns a heuristic rank for that state"""
    tile_spots = [[10, 8, 7, 6.5],
                  [.5, .7, 1, 3],
                  [-.5, -1.5, -1.8, -2],
                  [-3.8, -3.7, -3.5, -3]]
    score = 0
    for row_idx in range(4):
        for tile_idx in range(4):
            tile = state[row_idx][tile_idx]
            score += tile * tile_spots[row_idx][tile_idx]
            if tile == 2048:
                score += 10000
    empty = num_empty(state)


    return score + (empty*empty)
