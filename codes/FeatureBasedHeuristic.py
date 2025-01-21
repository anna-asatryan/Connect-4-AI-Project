from Environment import Connect4  # Import the Connect4 class
import numpy as np

class FeatureBasedHeuristicAgent:
    def __init__(self):
        self.feature_weights = {
            "win": float('inf'),
            "three_with_two_options": 900_000,
            "three_with_one_option": [40_000, 30_000, 20_000, 10_000],  # Depends on direction
            "unconnected": [40, 70, 120, 200, 120, 70, 40],  # Central column favored
        }

    def evaluate(self, game):
        """Feature-Based Heuristic Evaluation with randomness."""
        board = game.board
        score = 0

        # Feature 1: Check for winning state
        if game.check_winner() == game.current_player:
            return self.feature_weights["win"]

        # Feature 2: Check for three connected with two options
        score += self.evaluate_threes(board, game.current_player, with_two_options=True)

        # Feature 3: Check for three connected with one option
        score += self.evaluate_threes(board, game.current_player, with_two_options=False)

        # Feature 4: Evaluate unconnected discs (favor central column)
        score += self.evaluate_unconnected(board)

        # Add randomness to prevent repetitive behavior
        score += np.random.uniform(-500, 500)  # Add larger random variation

        return score

    def evaluate_threes(self, board, player, with_two_options):
        """Evaluate sequences of three connected discs."""
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, vertical, diagonals

        for r in range(board.shape[0]):
            for c in range(board.shape[1]):
                if board[r][c] == player:
                    for dr, dc in directions:
                        count = 0
                        spaces = 0
                        for i in range(4):
                            nr, nc = r + dr * i, c + dc * i
                            if 0 <= nr < board.shape[0] and 0 <= nc < board.shape[1]:
                                if board[nr][nc] == player:
                                    count += 1
                                elif board[nr][nc] == 0:
                                    spaces += 1
                            else:
                                break

                        if count == 3:
                            if with_two_options and spaces == 2:
                                score += self.feature_weights["three_with_two_options"]
                            elif not with_two_options and spaces == 1:
                                score += self.feature_weights["three_with_one_option"][spaces - 1]

        return score

    def evaluate_unconnected(self, board):
        """Evaluate unconnected discs based on column centrality."""
        score = 0
        num_columns = len(self.feature_weights["unconnected"])  # Should match the number of columns (7)

        for c in range(board.shape[1]):  # Iterate over all columns
            if c >= num_columns:
                continue  # Prevent IndexError if column index exceeds feature_weights list length
            for r in range(board.shape[0]):  # Iterate over rows
                if board[r][c] != 0:  # Disc is found
                    col_score = self.feature_weights["unconnected"][c]
                    score += col_score
                    break  # Only count the top disc in each column
        return score

    def get_move(self, game):
        """Evaluate each move and choose the best."""
        valid_columns = [col for col in range(game.columns) if game.is_valid_location(col)]
        scores = []

        for col in valid_columns:
            temp_game = Connect4()  # Temporary game state for simulation
            temp_game.board = game.board.copy()
            temp_game.current_player = game.current_player
            temp_game.drop_piece(col)
            score = self.evaluate(temp_game)
            scores.append((col, score))

        # Select column with highest score, with random tiebreaking
        max_score = max([s[1] for s in scores])
        best_columns = [col for col, score in scores if score == max_score]

        # Add randomness to the choice if there are ties
        return np.random.choice(best_columns)
