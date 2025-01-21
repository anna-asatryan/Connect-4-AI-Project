import numpy as np
import random
from Environment import Connect4



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
        """Evaluate the heuristic score of a move for the current player."""
        if not game.is_valid_location(col):
            return float('-inf')  # Invalid moves should not be considered

        # Simulate dropping the piece
        row = game.get_next_open_row(col)
        game.board[row][col] = game.current_player
        score = self.heuristic_matrix[row][col]
        game.board[row][col] = 0  # Undo the move
        return score


class MinimaxAI:
    def __init__(self, depth):
        """Initialize the Minimax AI with a given search depth."""
        self.depth = depth
        self.heuristic = BoardHeuristicAI()

    def minimax(self, game, depth, maximizing_player):
        """Minimax algorithm with heuristic evaluation."""
        winner = game.check_winner()
        if depth == 0 or winner or game.is_draw():
            if winner == 1:
                return None, float('inf')  # Maximizer (AI) wins
            elif winner == 2:
                return None, float('-inf')  # Minimizer (Opponent) wins
            else:
                return None, self.evaluate_board(game)

        valid_columns = [c for c in range(game.columns) if game.is_valid_location(c)]

        if maximizing_player:
            value = float('-inf')
            best_columns = []  # Track all columns with the best score
            for col in valid_columns:
                row = game.get_next_open_row(col)
                game.board[row][col] = 1
                _, new_score = self.minimax(game, depth - 1, False)
                game.board[row][col] = 0
                if new_score > value:
                    value = new_score
                    best_columns = [col]  # Reset and track the new best column
                elif new_score == value:
                    best_columns.append(col)  # Add to the list of best columns
            best_col = random.choice(best_columns)  # Randomly choose among the best columns
            return best_col, value
        else:
            value = float('inf')
            best_columns = []  # Track all columns with the best score
            for col in valid_columns:
                row = game.get_next_open_row(col)
                game.board[row][col] = 2
                _, new_score = self.minimax(game, depth - 1, True)
                game.board[row][col] = 0
                if new_score < value:
                    value = new_score
                    best_columns = [col]  # Reset and track the new best column
                elif new_score == value:
                    best_columns.append(col)  # Add to the list of best columns
            best_col = random.choice(best_columns)  # Randomly choose among the best columns
            return best_col, value


    def evaluate_board(self, game):
        """Evaluate the board state for intermediate nodes."""
        score = 0

        # Center column preference
        center_array = [game.board[r][game.columns // 2] for r in range(game.rows)]
        score += (center_array.count(1) - center_array.count(2)) * 3

        # Evaluate horizontal, vertical, and diagonal windows
        for r in range(game.rows):
            for c in range(game.columns - 3):
                window = game.board[r, c:c + 4]
                score += self.evaluate_window(window)

        for c in range(game.columns):
            col_array = game.board[:, c]
            for r in range(game.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window)

        for r in range(game.rows - 3):
            for c in range(game.columns - 3):
                window = [game.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        for r in range(3, game.rows):
            for c in range(game.columns - 3):
                window = [game.board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        """Evaluate a specific window of four cells."""
        score = 0
        if list(window).count(1) == 4:
            score += 100
        elif list(window).count(2) == 4:
            score -= 100
        return score

    def get_best_move(self, game):
        """Get the best move using the Minimax algorithm."""
        best_col, _ = self.minimax(game, self.depth, True)
        return best_col
    
class MinimaxAIWithPruning:
    def __init__(self, depth):
        """Initialize the Minimax AI with a given search depth."""
        self.depth = depth
        self.heuristic = BoardHeuristicAI()

    def minimax_with_pruning(self, game, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        :param game: The Connect4 game instance.
        :param depth: Depth of the search tree.
        :param alpha: Alpha value for pruning.
        :param beta: Beta value for pruning.
        :param maximizing_player: Boolean, True if maximizing player's turn.
        :return: Best column and its heuristic score.
        """
        winner = game.check_winner()
        if depth == 0 or winner or game.is_draw():
            if winner == 1:
                return None, float('inf')  # Maximizer wins
            elif winner == 2:
                return None, float('-inf')  # Minimizer wins
            else:
                return None, self.evaluate_board(game)  # Heuristic evaluation for intermediate states

        valid_columns = [c for c in range(game.columns) if game.is_valid_location(c)]

        if maximizing_player:
            value = float('-inf')
            best_columns = []  # Track all columns with the best score
            for col in valid_columns:
                row = game.get_next_open_row(col)
                game.board[row][col] = 1  # Simulate maximizer's move
                _, new_score = self.minimax_with_pruning(game, depth - 1, alpha, beta, False)
                game.board[row][col] = 0  # Undo the move
                if new_score > value:
                    value = new_score
                    best_columns = [col]  # Reset and track the new best column
                elif new_score == value:
                    best_columns.append(col)  # Add to the list of best columns
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff
            best_col = random.choice(best_columns)  # Randomly choose among the best columns,
            return best_col, value
        else:
            value = float('inf')
            best_columns = []  # Track all columns with the best score
            for col in valid_columns:
                row = game.get_next_open_row(col)
                game.board[row][col] = 2  # Simulate minimizer's move
                _, new_score = self.minimax_with_pruning(game, depth - 1, alpha, beta, True)
                game.board[row][col] = 0  # Undo the move
                if new_score < value:
                    value = new_score
                    best_columns = [col]  # Reset and track the new best column
                elif new_score == value:
                    best_columns.append(col)  # Add to the list of best columns
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cutoff
            best_col = random.choice(best_columns)  # Randomly choose among the best columns
            return best_col, value

    def evaluate_board(self, game):
        """Evaluate the board state for intermediate nodes."""
        score = 0

        # Center column preference
        center_array = [game.board[r][game.columns // 2] for r in range(game.rows)]
        score += (center_array.count(1) - center_array.count(2)) * 3

        # Evaluate horizontal, vertical, and diagonal windows
        for r in range(game.rows):
            for c in range(game.columns - 3):
                window = game.board[r, c:c + 4]
                score += self.evaluate_window(window)

        for c in range(game.columns):
            col_array = game.board[:, c]
            for r in range(game.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window)

        for r in range(game.rows - 3):
            for c in range(game.columns - 3):
                window = [game.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        for r in range(3, game.rows):
            for c in range(game.columns - 3):
                window = [game.board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window):
        """Evaluate a specific window of four cells."""
        score = 0
        if list(window).count(1) == 4:
            score += 100
        elif list(window).count(2) == 4:
            score -= 100
        return score

    def get_best_move(self, game):
        """Get the best move using Minimax with alpha-beta pruning."""
        best_col, _ = self.minimax_with_pruning(game, self.depth, float('-inf'), float('inf'), True)
        return best_col

