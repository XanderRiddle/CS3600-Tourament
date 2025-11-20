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

    def apply_move(self, board_state: board.Board, move):
        return None

    def board_state_is_terminating_state(self, board_state: board.Board):
        return None
    
    def evaluation (self, board_state: board.Board):
        score = 0
        player_eggs_laid = board_state.chicken_player.get_eggs_laid()
        enemy_eggs_laid = board_state.chicken_enemy.get_eggs_laid()
        score = player_eggs_laid - enemy_eggs_laid
        return score
        
    def minimax(self, board_state: board.Board, depth, is_maximizing_player):
        if self.board_state_is_terminating_state(board_state):
            return -np.inf if is_maximizing_player else np.inf
        elif depth == 3:
            return self.evaluation(board_state)
        
        moves = board_state.get_valid_moves()
        if is_maximizing_player:
            best_value = -np.inf
            for move in moves:
                new_state = self.apply_move(board_state, move)
                value = self.minimax(new_state, depth + 1, False)
                best_value = max(best_value, value)
            return best_value
    
        else:
            best_value = np.inf
            for move in moves:
                new_state = self.apply_move(board_state, move)
                value = self.minimax(new_state, depth + 1, True)
                best_value = min(best_value, value)
            return best_value

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
        self.minimax()
        result = moves[np.random.randint(len(moves))]
        print(f"I have {time_left()} seconds left. Playing {result}.")
        return result
       

