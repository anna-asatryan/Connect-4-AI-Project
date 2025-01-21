import random

class RandomAgent:
    @staticmethod
    def get_move(game):
        """
        Choose a random valid column for the current player.
        :param game: Connect4 game instance
        :return: Column index of the move
        """
        valid_columns = [c for c in range(game.columns) if game.is_valid_location(c)]
        return random.choice(valid_columns)
