from collections.abc import Callable
from time import sleep
from typing import List, Set, Tuple

import numpy as np
from game import *

class PlayerAgent:
    """
    /you may add functions, however, __init__ and play are the entry points for
    your program and should not be changed.
    """

    def __init__(self, board: board.Board, time_left: Callable):
        self.known_traps = set()
        self.visited = set()   # REAL game visited

    def apply_move(self, board_state: board.Board, move):
        direction, move_type = move
        return board_state.forecast_move(direction, move_type)

    def board_state_is_terminating_state(self, board_state: board.Board):
        if board_state.is_game_over():
            return True
        if not board_state.get_valid_moves():
            return True
        return False
    
    def manhattan_distance_to_center(self, board_state: board.Board):
        x, y = board_state.chicken_player.get_location()
        width, height = 8, 8
        center_x, center_y = width // 2, height // 2
        return abs(x - center_x) + abs(y - center_y)

    def evaluation(self, board_state: board.Board, visited):
        player_location = board_state.chicken_player.get_location()
        player_eggs = board_state.chicken_player.get_eggs_laid()
        enemy_eggs = board_state.chicken_enemy.get_eggs_laid()

        # Score diff in eggs
        score = player_eggs - enemy_eggs

        # Prefer being closer to the center of the board
        score -= self.manhattan_distance_to_center(board_state) * 10

        # Penalize revisiting tiles (in search)
        if player_location in visited:
            score -= 9999

        # Penalize stepping on a known trapdoor
        if player_location in board_state.found_trapdoors:
            score -= 9999

        return score

    def minimax(
        self,
        board_state: board.Board,
        depth,
        is_maximizing_player,
        visited,
        MAX_DEPTH = 5
    ):
        # If game is over or maximum depth reached, evaluate
        if self.board_state_is_terminating_state(board_state):
            return -np.inf if is_maximizing_player else np.inf
        elif depth == MAX_DEPTH:
            return self.evaluation(board_state, visited)

        # Current position for future visited checks
        current_loc = board_state.chicken_player.get_location()

        # Add current tile to visited for future recursive calls
        visited = visited | {current_loc}

        moves = board_state.get_valid_moves()

        if is_maximizing_player:
            best_value = -np.inf
            for move in moves:
                new_state = self.apply_move(board_state, move)

                value = self.minimax(
                    new_state,
                    depth + 1,
                    False,
                    visited,
                )
                best_value = max(best_value, value)
            return best_value

        else:
            best_value = np.inf
            for move in moves:
                new_state = self.apply_move(board_state, move)

                value = self.minimax(
                    new_state,
                    depth + 1,
                    True,
                    visited,
                )
                best_value = min(best_value, value)
            return best_value

    def play(
        self,
        board: board.Board,
        sensor_data: List[Tuple[bool, bool]],
        time_left: Callable,
    ):
        # Mark current location as visited in the real game
        location = board.chicken_player.get_location()
        self.visited.add(location)

        print(f"I'm at {location}.")
        print(f"Trapdoor A: heard? {sensor_data[0][0]}, felt? {sensor_data[0][1]}")
        print(f"Trapdoor B: heard? {sensor_data[1][0]}, felt? {sensor_data[1][1]}")
        print(f"Starting to think with {time_left()} seconds left.")

        moves = board.get_valid_moves()
        best_value = -np.inf
        best_move = None

        for move in moves:
            new_state = self.apply_move(board, move)

            # Pass a copy of real visited into minimax
            value = self.minimax(
                new_state,
                depth=1,
                is_maximizing_player=False,
                visited=set(self.visited)
            )

            if value > best_value:
                best_value = value
                best_move = move

        result = best_move
        print(f"I have {time_left()} seconds left. Playing {result}.")
        return result
