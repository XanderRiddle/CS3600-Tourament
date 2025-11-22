from game.enums import Direction, MoveType, Result

class PlayerAgent:
    def __init__(self, board, time_left):
        # Initialization parameters
        self.board = board
        self.time_left = time_left
        self.max_depth = 8        # maximum search depth
        self.debug = False
        self.EGG_WEIGHT = 10      # weight for egg-count advantage
        self.EDGE_WEIGHT = 1      # penalty weight for distance from edge
        self.INF = float('inf')

    def play(self, board, sensor_data, time_left):
        # Return (Direction, MoveType) for our move.
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None  # no move possible (should rarely happen if rules followed)

        # Iterative deepening: search depth 1,2,... until time runs low:contentReference[oaicite:3]{index=3}.
        best_move = valid_moves[0]
        for depth in range(1, self.max_depth+1):
            if self.time_left() < 0.1:  # leave small time margin
                break
            alpha = -self.INF
            beta  =  self.INF
            best_val = -self.INF
            current_best = best_move
            # Evaluate each move at this depth
            for move in valid_moves:
                if self.time_left() < 0.05:
                    break
                # Ensure move is still valid (board may have changed contextually)
                if not board.is_valid_move(move[0], move[1]):
                    continue
                new_board = board.forecast_move(move[0], move[1])
                if new_board is None:
                    continue
                # Minimax search (our move just played, now opponent's turn)
                val = self.minimax_rec(new_board, depth-1, alpha, beta, maximizing=False)
                if val is None:
                    # Search aborted due to timeout
                    break
                if val > best_val:
                    best_val = val
                    current_best = move
                    alpha = max(alpha, best_val)
                    if alpha >= beta:
                        break
            # Update best move if this iteration completed
            best_move = current_best
            if self.debug:
                print(f"Depth {depth}: best move {best_move}, value {best_val}")
        if self.debug:
            print(f"Chosen move: {best_move}")
        return best_move

    def minimax_rec(self, board, depth, alpha, beta, maximizing):
        # Terminal or depth cutoff
        if board.is_game_over() or depth == 0 or self.time_left() < 0.01:
            return self.evaluate(board)

        if maximizing:
            max_val = -self.INF
            moves = board.get_valid_moves()
            if not moves:
                return self.evaluate(board)
            for move in moves:
                new_board = board.forecast_move(move[0], move[1])
                if new_board is None:
                    continue
                val = self.minimax_rec(new_board, depth-1, alpha, beta, False)
                if val is None:
                    return None  # propagate timeout signal
                max_val = max(max_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break  # alpha-beta prune
            return max_val
        else:
            min_val = self.INF
            moves = board.get_valid_moves(enemy=True)
            if not moves:
                return self.evaluate(board)
            for move in moves:
                # Simulate opponent's move by swapping perspective
                temp = board.get_copy()
                temp.reverse_perspective()
                if not temp.apply_move(move[0], move[1]):
                    continue
                temp.reverse_perspective()
                val = self.minimax_rec(temp, depth-1, alpha, beta, True)
                if val is None:
                    return None
                min_val = min(min_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break  # alpha-beta prune
            return min_val

    def evaluate(self, board):
        # Heuristic evaluation of board state
        my_eggs  = board.chicken_player.get_eggs_laid()
        opp_eggs = board.chicken_enemy.get_eggs_laid()
        egg_diff = my_eggs - opp_eggs

        # Check terminal win/loss
        if board.is_game_over():
            winner = board.get_winner()
            if winner == Result.PLAYER:
                return 1000   # large positive for win
            elif winner == Result.ENEMY:
                return -1000  # large negative for loss
            else:
                return 0      # tie

        # Penalty for being far from board edge (trapdoors are more likely central)
        x, y = board.chicken_player.get_location()
        if board.chicken_player.get_location() in board.found_trapdoors:
            return -9999
        size = board.game_map.MAP_SIZE - 1
        dist_edge = min(x, size - x, y, size - y)
        # Final score: eggs difference (maximized) minus edge-distance penalty
        return egg_diff * self.EGG_WEIGHT - dist_edge * self.EDGE_WEIGHT
