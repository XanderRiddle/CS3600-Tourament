from typing import Callable, List, Tuple
from game.enums import Direction, MoveType
from game.chicken import Chicken

class PlayerAgent:
    def __init__(self, board, time_left: Callable):
        # Track visited cells to encourage exploration
        loc = board.chicken_player.get_location()
        self.visited = {loc}
        # Remember our chicken's color (even sum squares vs odd)
        self.even_color = board.chicken_player.even_chicken

    def play(self, board, sensor_data: List[Tuple[bool,bool]], time_left: Callable):
        # Update visited with current location
        my_loc = board.chicken_player.get_location()
        self.visited.add(my_loc)

        def evaluate(bd):
            # Evaluation from bd.chicken_player’s perspective
            my_chicken = bd.chicken_player
            enemy = bd.chicken_enemy
            my_loc = my_chicken.get_location()
            opp_loc = enemy.get_location()
            # Egg count difference
            score = (my_chicken.get_eggs_laid() - enemy.get_eggs_laid()) * 10.0
            # Bonus if can drop an egg here
            x,y = my_loc
            if (x+y) % 2 == (0 if bd.chicken_player.even_chicken else 1):
                # square is our color
                if (x,y) not in bd.eggs_player and (x,y) not in bd.turds_player:
                    score += 5.0
            # Turd resource advantage (small)
            score += (my_chicken.turds_left - enemy.turds_left)
            # Prefer being near edges (avoid trap in center)
            dx = min(x, 7-x); dy = min(y, 7-y)
            score += 0.2 * (dx + dy)  # encourage larger distance from center
            # Avoid repeats
            if my_loc in self.visited:
                score -= 1.0
            return score

        # Minimax with alpha-beta
        def minimax(bd, depth, alpha, beta):
            # Time check (optional cut-off)
            if time_left() < 0.1:
                return evaluate(bd)
            moves = bd.get_valid_moves(enemy=False)
            if depth == 0 or not moves:
                # Terminal or depth limit
                return evaluate(bd)
            best = float('-inf')
            for (dir, move_type) in moves:
                new_bd = bd.forecast_move(dir, move_type)
                if new_bd is None:
                    continue
                new_bd.reverse_perspective()
                score = minimax(new_bd, depth-1, alpha, beta)
                if score > best:
                    best = score
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # prune
            return best

        # Root search: maximize
        best_score = float('-inf')
        best_move = None
        for (dir, move_type) in board.get_valid_moves():
            new_board = board.forecast_move(dir, move_type)
            if new_board is None:
                continue
            new_board.reverse_perspective()
            score = minimax(new_board, 6, best_score, float('inf'))
            if score > best_score:
                best_score = score
                best_move = (dir, move_type)
        # If no move found (shouldn't happen if any moves exist), pick a fallback
        if best_move is None and board.get_valid_moves():
            best_move = board.get_valid_moves()[0]
        return best_move
