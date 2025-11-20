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
        self.known_traps = set()

    def apply_move(self, board_state: board.Board, move):
            direction, move_type = move
            new_state = board_state.forecast_move(direction, move_type)
            return new_state

    def board_state_is_terminating_state(self, board_state: board.Board):
        if board_state.is_game_over():
            return True
        if not board_state.get_valid_moves():
            return True
        return False
    
    def evaluation (self, board_state: board.Board):
        score = 0
        player_location = board_state.chicken_player.get_location() * 2
        enemy_location = board_state.chicken_enemy.get_location()
        player_eggs_laid = board_state.chicken_player.get_eggs_laid() * 2
        enemy_eggs_laid = board_state.chicken_enemy.get_eggs_laid()
        score = player_eggs_laid - enemy_eggs_laid
        score += board_state.chicken_player.can_lay_egg(player_location)
        score -= board_state.chicken_enemy.can_lay_egg(enemy_location)
        score += len(board_state.get_valid_moves()) * 0.1
        score -= self.distance_to_next_egg_tile(board_state)
        if (player_location) in board_state.found_trapdoors:
            score -= 9999
        score += self.distance_to_center(board_state) * 0.1
        return score
        
    def distance_to_next_egg_tile(self, board_state: board.Board):
        px, py = board_state.chicken_player.get_location()
        min_dist = 999

        for x in range(board_state.game_map.MAP_SIZE):
            for y in range(board_state.game_map.MAP_SIZE):
                if board_state.chicken_player.can_lay_egg((x,y)):
                    dist = abs(px - x) + abs(py - y)
                    min_dist = min(min_dist, dist)

        return min_dist
    
    def distance_to_center(self, board_state: board.Board):
        px, py = board_state.chicken_player.get_location()
        center = board_state.game_map.MAP_SIZE // 2
        cx, cy = center, center
        return abs(px - cx) + abs(py - cy)

    def minimax(self, board_state: board.Board, depth, is_maximizing_player, MAX_DEPTH = 5):
        if self.board_state_is_terminating_state(board_state):
            return -np.inf if is_maximizing_player else np.inf
        elif depth == MAX_DEPTH:
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
        best_value = -np.inf
        best_move = None
        for move in moves:
            new_state = self.apply_move(board, move)
            value = self.minimax(new_state, depth=1, is_maximizing_player=True)
            if value > best_value:
                best_value = value
                best_move = move
        result = best_move
        print(f"I have {time_left()} seconds left. Playing {result}.")
        return result
       

