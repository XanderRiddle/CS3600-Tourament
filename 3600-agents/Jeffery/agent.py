from collections.abc import Callable
from time import sleep
from typing import List, Set, Tuple

import numpy as np
from game import *

"""
Jeffery is hopefully not quite the dumbest and may just be smart enough to beat Henry.
"""

class PlayerAgent:
    """
    /you may add functions, however, __init__ and play are the entry points for
    your program and should not be changed.
    """

    def __init__(self, board: board.Board, time_left: Callable):
        pass

    def play(
        self,
        board: board.Board,
        sensor_data: List[Tuple[bool, bool]],
        time_left: Callable,
    ):
        location = board.chicken_player.get_location()
        print(f"I'm at {location}.")
        print(f"Trapdoor A: heard? {sensor_data[0][0]}, felt? {sensor_data[0][1]}")
        print(f"Trapdoor B: heard? {sensor_data[1][0]}, felt? {sensor_data[1][1]}")
        print(f"Starting to think with {time_left()} seconds left.")
        moves = board.get_valid_moves()
        minimax()
        result = moves[np.random.randint(len(moves))]
        print(f"I have {time_left()} seconds left. Playing {result}.")
        return result
    
    def minimax():
        moves = board.get_valid_moves()
        if move_terminates_game():
            return best_move
        elif number_of_recursions == 3:
            return best_move
        
        if maximizing_player:
        best_value = -infinity
        for move in moves:
            new_state = apply_move(move)
            value = minimax(new_state, depth + 1, False)
            best_value = max(best_value, value)
        return best_value
    
        else:
        best_value = +infinity
        for move in get_moves(state):
            new_state = apply_move(state, move)
            value = minimax(new_state, depth + 1, True)
            best_value = min(best_value, value)
        return best_value
    
    def apply_move(move):
       

