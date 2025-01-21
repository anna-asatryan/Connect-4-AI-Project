import numpy as np

class Connect4:
    def __init__(self):
        """Initialize the Connect-4 board and game state."""
        self.rows = 6
        self.columns = 7
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.game_over = False
        self.current_player = 1  # Player 1 starts

    

    def is_valid_location(self, col):
        """Check if the column has at least one open slot."""
        return self.board[5][col] == 0

    def drop_piece(self, col):
        """
        Drop a piece for the current player into the specified column.
        The piece falls to the lowest available row.
        """
        if not self.is_valid_location(col):
            raise ValueError("Column is full. Choose another column.")

        # Find the lowest available row in the column
        row = self.get_next_open_row(col)
        self.board[row][col] = self.current_player
        
        
    def get_next_open_row(self, col):
        """
        Find the next open row in the specified column.
        Returns the row index for the lowest available slot.
        """
        for r in range(0, 6, 1):  # Start from the bottom row
            if self.board[r][col] == 0:
                return r
        raise ValueError("Column is full.")
        

    def print_board(self):
        """Print the board to the console."""
        print(np.flip(self.board, 0))  # Flip the board to display the bottom row first

    def check_winner(self):
        """
        Check for a winner (four in a row).
        Returns the winning player number (1 or 2), or None if no winner yet.
        """
        # Check horizontal locations
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if self.board[r][c] == self.current_player and \
                   self.board[r][c] == self.board[r][c + 1] == self.board[r][c + 2] == self.board[r][c + 3]:
                    return self.current_player

        # Check vertical locations
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if self.board[r][c] == self.current_player and \
                   self.board[r][c] == self.board[r + 1][c] == self.board[r + 2][c] == self.board[r + 3][c]:
                    return self.current_player

        # Check positively sloped diagonals
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if self.board[r][c] == self.current_player and \
                   self.board[r][c] == self.board[r + 1][c + 1] == self.board[r + 2][c + 2] == self.board[r + 3][c + 3]:
                    return self.current_player

        # Check negatively sloped diagonals
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                if self.board[r][c] == self.current_player and \
                   self.board[r][c] == self.board[r - 1][c + 1] == self.board[r - 2][c + 2] == self.board[r - 3][c + 3]:
                    return self.current_player

        return None

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 3 - self.current_player  # If 1, switch to 2; if 2, switch to 1

    def is_draw(self):
        """Check if the game is a draw (board is full)."""
        return not any(self.is_valid_location(c) for c in range(self.columns))

    def reset_game(self):
        """Reset the board and game state."""
        self.board = np.zeros((self.rows, self.columns), dtype=int)
        self.game_over = False
        self.current_player = 1


import random

# Example gameplay with Player 1 as manual and Player 2 as random
def play_game():
    game = Connect4()

    while not game.game_over:
        game.print_board()

        try:
            if game.current_player == 1:  # Player 1 (manual input)
                col = int(input(f"Player {game.current_player}, choose a column (0-6): "))
                if col < 0 or col >= game.columns:
                    print("Invalid column. Choose between 0 and 6.")
                    continue
            else:  # Player 2 (random move)
                valid_columns = [c for c in range(game.columns) if game.is_valid_location(c)]
                col = random.choice(valid_columns)
                print(f"Player {game.current_player} (AI) chooses column: {col}")

            game.drop_piece(col)
            winner = game.check_winner()
            if winner:
                game.print_board()
                print(f"Player {winner} wins!")
                game.game_over = True
            elif game.is_draw():
                game.print_board()
                print("It's a draw!")
                game.game_over = True
            else:
                game.switch_player()
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    play_game()

