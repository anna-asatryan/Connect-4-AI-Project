import numpy as np
import random
from Environment import Connect4
from BoardHeuristic import BoardHeuristicAI


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
            best_col = random.choice(best_columns)  # Randomly choose among the best columns
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


    
import numpy as np
import random
import time

# Assuming all the previous code is already defined for Connect4, MCTS, Minimax with Pruning, etc.

class Game:
    def __init__(self, mcts_agent, minimax_agent):
        self.game_state = Connect4()  # Connect4 game instance
        self.mcts_agent = mcts_agent  # MCTS agent
        self.minimax_agent = minimax_agent  # Minimax AI with pruning agent
        self.players = [self.mcts_agent, self.minimax_agent]  # Players alternate

        # Pass the current game state to MCTS agent
        self.mcts_agent.set_game(self.game_state)

    def play(self):
        """Run the game loop where MCTS and Minimax AI take turns."""
        turn = 0
        while not self.game_state.game_over:
            current_agent = self.players[turn % 2]  # Player 1 (MCTS) or Player 2 (Minimax)
            print(f"Player {self.game_state.current_player}'s turn (Agent {type(current_agent).__name__}):")
            self.game_state.print_board()

            if isinstance(current_agent, MCTS):
                move = current_agent.get_best_move()  # MCTS decision
            elif isinstance(current_agent, MinimaxAIWithPruning):
                move = current_agent.get_best_move(self.game_state)  # Minimax decision

            print(f"Chosen column: {move}")
            self.game_state.drop_piece(move)

            # Check if the current player has won or if it's a draw
            winner = self.game_state.check_winner()
            if winner:
                self.game_state.print_board()
                print(f"Player {winner} wins!")
                break
            elif self.game_state.is_draw():
                self.game_state.print_board()
                print("It's a draw!")
                break

            # Switch player for the next turn
            self.game_state.switch_player()
            turn += 1


class MCTS:
    def __init__(self, simulations=500):
        self.game = None  # Initially, no game
        self.simulations = simulations

    def set_game(self, game):
        """Set the game state for the MCTS agent."""
        self.game = game

    def simulate(self):
        """Simulate a random game from the current state."""
        board_copy = self.game.board.copy()
        current_player = self.game.current_player
        while True:
            valid_columns = [c for c in range(self.game.columns) if self.is_valid_location(board_copy, c)]
            if not valid_columns:
                return 0  # Draw
            col = random.choice(valid_columns)
            row = self.get_next_open_row(board_copy, col)
            board_copy[row][col] = current_player
            if self.check_winner(board_copy, current_player):
                return 1 if current_player == self.game.current_player else -1
            current_player = 3 - current_player

    def get_best_move(self):
        """Get the best move using Monte Carlo simulations."""
        valid_columns = [c for c in range(self.game.columns) if self.game.is_valid_location(c)]
        scores = {col: 0 for col in valid_columns}
        for col in valid_columns:
            for _ in range(self.simulations):
                board_copy = self.game.board.copy()
                row = self.get_next_open_row(board_copy, col)
                board_copy[row][col] = self.game.current_player
                result = self.simulate()
                scores[col] += result
        return max(scores, key=scores.get)

    def is_valid_location(self, board, col):
        """Check if the column has at least one open slot."""
        return board[5][col] == 0

    def get_next_open_row(self, board, col):
        """Find the next open row in the specified column."""
        for r in range(len(board)):
            if board[r][col] == 0:
                return r
        raise ValueError("Column is full.")

    def check_winner(self, board, player):
        """Check if the player has won."""
        # Horizontal check
        for r in range(len(board)):
            for c in range(len(board[0]) - 3):
                if board[r][c] == player and all(board[r][c + i] == player for i in range(4)):
                    return True
        # Vertical check
        for c in range(len(board[0])):
            for r in range(len(board) - 3):
                if board[r][c] == player and all(board[r + i][c] == player for i in range(4)):
                    return True
        # Positive diagonal
        for r in range(len(board) - 3):
            for c in range(len(board[0]) - 3):
                if board[r][c] == player and all(board[r + i][c + i] == player for i in range(4)):
                    return True
        # Negative diagonal
        for r in range(3, len(board)):
            for c in range(len(board[0]) - 3):
                if board[r][c] == player and all(board[r - i][c + i] == player for i in range(4)):
                    return True
        return False


# Game setup: Create MCTS agent and Minimax with pruning AI
mcts_agent = MCTS(simulations=500)  # You can adjust the simulations
minimax_agent = MinimaxAIWithPruning(depth=4)  # Set the depth for Minimax with pruning

# Create a game and start playing
game = Game(mcts_agent=mcts_agent, minimax_agent=minimax_agent)
game.play()