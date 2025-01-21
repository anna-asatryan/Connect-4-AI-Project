from Environment import Connect4
from FeatureBasedHeuristic import FeatureBasedHeuristicAgent
from BoardHeuristic import BoardHeuristicAI
from GameInterface import GameInterface
import pygame


class GameController:
    def __init__(self, agent_1=None, agent_2=None):
        self.game = Connect4()
        self.agent_1 = agent_1 if agent_1 else FeatureBasedHeuristicAgent()
        self.agent_2 = agent_2 if agent_2 else BoardHeuristicAI()
        self.interface = GameInterface()

    def play_game(self):
        """Play a game between the Feature-Based Heuristic and the Board-Based Heuristic."""
        print("Starting the game between Feature-Based Heuristic and Board-Based Heuristic!")
        self.interface.draw_board(self.game.board)
        pygame.display.update()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Allow window to close
                    pygame.quit()
                    exit()

            if self.game.game_over:
                print("Game over!")
                pygame.time.wait(5000)  # Wait 5 seconds at the end
                running = False
                continue

            if self.game.current_player == 1:  # Player 1: Feature-Based Heuristic
                col = self.agent_1.get_move(self.game)
                print(f"Player 1 (Feature-Based Heuristic) chooses column {col + 1}")
            else:  # Player 2: Board-Based Heuristic
                col = self.agent_2.get_best_move(self.game)
                print(f"Player 2 (Board-Based Heuristic) chooses column {col + 1}")

            if self.game.is_valid_location(col):
                self.game.drop_piece(col)
                print(f"Piece dropped in column {col + 1}")
                self.interface.draw_board(self.game.board)
                pygame.display.update()

                # Add delay between moves
                pygame.time.wait(1500)  # Wait 2 seconds before the next move

                winner = self.game.check_winner()
                if winner:
                    print(f"Player {winner} wins!")
                    self.interface.display_winner(winner)
                    self.game.game_over = True
                elif self.game.is_draw():
                    print("Game is a draw!")
                    self.interface.display_winner(None)
                    self.game.game_over = True
                else:
                    self.game.switch_player()
