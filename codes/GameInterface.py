import pygame
import numpy as np

class GameInterface:
    def __init__(self):
        """Initialize the Pygame interface."""
        pygame.init()

        # Colors
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        # Dimensions
        self.SQUARESIZE = 100
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.width = 7 * self.SQUARESIZE
        self.height = (6 + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)

        # Pygame screen setup
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Connect-4")
        self.font = pygame.font.SysFont("monospace", 75)

    def draw_board(self, board):
        """Draw the Connect-4 board."""
        for r in range(6):
            for c in range(7):
                pygame.draw.rect(
                    self.screen, self.BLUE,
                    (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                )
                pygame.draw.circle(
                    self.screen, self.BLACK,
                    (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)),
                    self.RADIUS
                )

        for r in range(6):
            for c in range(7):
                if board[r][c] == 1:
                    pygame.draw.circle(
                        self.screen, self.RED,
                        (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                        self.RADIUS
                    )
                elif board[r][c] == 2:
                    pygame.draw.circle(
                        self.screen, self.YELLOW,
                        (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                        self.RADIUS
                    )
        pygame.display.update()

    def display_winner(self, winner):
        """Display the winner in the graphical interface."""
        if winner:
            label = self.font.render(f"Player {winner} wins!", True, self.RED if winner == 1 else self.YELLOW)
        else:
            label = self.font.render("It's a Draw!", True, self.BLACK)
        self.screen.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(3000)
