import numpy as np

class BoardHeuristicAI:
    def __init__(self):
        """Initialize the heuristic matrix for evaluating moves."""
        self.heuristic_matrix = np.array([
            [3, 4, 5, 7, 5, 4, 3],
            [4, 6, 8, 10, 8, 6, 4],
            [5, 8, 11, 13, 11, 8, 5],
            [5, 8, 11, 13, 11, 8, 5],
            [4, 6, 8, 10, 8, 6, 4],
            [3, 4, 5, 7, 5, 4, 3]
        ])

    def evaluate_move(self, game, col):
        """
        Evaluate the heuristic score of a move for the current player.
        :param game: Connect4 game instance
        :param col: Column index for evaluation
        :return: Heuristic score for the move
        """
        if not game.is_valid_location(col):
            return float('-inf')  # Invalid moves should not be considered

        # Simulate dropping the piece
        row = game.get_next_open_row(col)
        game.board[row][col] = game.current_player
        score = self.heuristic_matrix[row][col]
        game.board[row][col] = 0  # Undo the move
        return score

    def get_best_move(self, game):
        """
        Get the best move for the current player based on the heuristic.
        :param game: Connect4 game instance
        :return: Column index of the best move
        """
        valid_columns = [c for c in range(game.columns) if game.is_valid_location(c)]
        scores = [self.evaluate_move(game, c) for c in valid_columns]
        best_score = max(scores)
        best_columns = [valid_columns[i] for i in range(len(scores)) if scores[i] == best_score]
        return np.random.choice(best_columns)  # Break ties randomly
