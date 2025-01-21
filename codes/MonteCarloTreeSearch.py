import numpy as np
import random
from Environment import Connect4


class MCTS:
    def __init__(self, game, simulations=500):
        self.game = game
        self.simulations = simulations

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

    def expansion(self, node):
        """Expand the current node by creating a child node for each possible move."""
        valid_moves = [c for c in range(self.game.columns) if self.is_valid_location(self.game.board, c)]
        for move in valid_moves:
            row = self.get_next_open_row(self.game.board, move)
            self.game.drop_piece(move)
            node.child_nodes.append(move)
            self.game.switch_player()
        return node

def run_mcts_simulations(num_games, simulations_per_game):
    """Run multiple games to test the winning rate of MCTS."""
    mcts_wins = 0
    player2_wins = 0
    draws = 0

    for game_num in range(num_games):
        print(f"\nGame {game_num + 1}")
        game = Connect4()
        mcts = MCTS(game, simulations=simulations_per_game)

        while not game.game_over:
            game.print_board()

            if game.current_player == 1:  # Player 1 (MCTS)
                col = mcts.get_best_move()
                print(f"Player 1 (MCTS) chooses column: {col}")
            else:  # Player 2 (Random)
                valid_columns = [c for c in range(game.columns) if game.is_valid_location(c)]
                col = random.choice(valid_columns)
                print(f"Player 2 (Random) chooses column: {col}")

            game.drop_piece(col)
            winner = game.check_winner()
            if winner:
                game.print_board()
                print(f"Player {game.current_player} wins!")
                if winner == 1:
                    mcts_wins += 1
                else:
                    player2_wins += 1
                game.game_over = True
            elif game.is_draw():
                game.print_board()
                print("It's a draw!")
                draws += 1
                game.game_over = True
            else:
                game.switch_player()

    # Calculate win rates
    total_games = num_games
    mcts_win_rate = (mcts_wins / total_games) * 100
    player2_win_rate = (player2_wins / total_games) * 100
    draw_rate = (draws / total_games) * 100

    print(f"\nAfter {num_games} games with {simulations_per_game} simulations per game:")
    print(f"Player 1 (MCTS) wins: {mcts_win_rate:.2f}%")
    print(f"Player 2 (Random) wins: {player2_win_rate:.2f}%")
    print(f"Draws: {draw_rate:.2f}%")

if __name__ == "__main__":
    # Run the test with 100 simulations per game for 10 games
    run_mcts_simulations(num_games=10, simulations_per_game=100)
