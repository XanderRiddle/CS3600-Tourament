# Heuristic PlayerAgent implementation
import numpy as np
from game.enums import Direction, MoveType

class PlayerAgent:
    def __init__(self, board, time_left):
        # Track suspected trapdoor danger maps (optional for heuristic)
        self.board_init = board
        self.time_left = time_left

    def play(self, board, sensor_data, time_left):
        moves = board.get_valid_moves()
        if not moves:
            return None

        # Basic heuristic scoring for each move
        best_score = -1e9
        best_move = moves[0]
        my_loc = board.chicken_player.get_location()
        enemy_loc = board.chicken_enemy.get_location()

        for move in moves:
            direction, mtype = move
            score = 0

            # Encourage egg laying when valid
            if mtype == MoveType.EGG:
                score += 50
                # Bonus for corner eggs
                x, y = my_loc
                if (x in (0, board.game_map.MAP_SIZE-1) and 
                    y in (0, board.game_map.MAP_SIZE-1)):
                    score += 30

            # Turd defensive use: only useful if near enemy
            if mtype == MoveType.TURD:
                dist = abs(my_loc[0] - enemy_loc[0]) + abs(my_loc[1] - enemy_loc[1])
                if dist <= 3:
                    score += 20
                else:
                    score -= 10

            # Prefer moving toward center
            next_loc = board.chicken_player.get_next_loc(direction, loc=my_loc)
            center = (3.5, 3.5)
            dist_center = abs(next_loc[0]-center[0]) + abs(next_loc[1]-center[1])
            score += (10 - dist_center)

            # Avoid squares adjacent to enemy turds
            if board.is_cell_in_enemy_turd_zone(next_loc):
                score -= 200

            # Avoid likely trapdoor squares if strong signal
            # Simple rule: if felt=True, avoid moving
            heard_w, felt_w = sensor_data[0]
            heard_b, felt_b = sensor_data[1]
            if felt_w or felt_b:
                score -= 100

            if score > best_score:
                best_score = score
                best_move = move

        return best_move