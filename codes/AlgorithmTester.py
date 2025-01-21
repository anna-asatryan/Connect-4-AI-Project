import time
import tracemalloc
from GameController import GameController
from FeatureBasedHeuristic import FeatureBasedHeuristicAgent
from BoardHeuristic import BoardHeuristicAI

class AlgorithmTester:
    def __init__(self):
        self.results = []

    def test_algorithms(self, num_games=10):
        """Run a series of games between Feature-Based and Board-Based heuristics."""
        agent1 = FeatureBasedHeuristicAgent()
        agent2 = BoardHeuristicAI()

        agent1_name = "Feature-Based Heuristic"
        agent2_name = "Board-Based Heuristic"
        print(f"Testing {agent1_name} vs {agent2_name}")

        agent1_wins = 0
        agent2_wins = 0
        draws = 0

        metrics = {
            "agent1_execution_time": [],
            "agent2_execution_time": [],
            "agent1_memory_usage": [],
            "agent2_memory_usage": [],
        }

        for game_num in range(num_games):
            print(f"\nGame {game_num + 1}/{num_games}")
            controller = GameController()
            controller.agent_1 = agent1  # Set Player 1
            controller.agent_2 = agent2  # Set Player 2
            controller.game.current_player = 1  # Feature-Based starts

            while not controller.game.game_over:
                if controller.game.current_player == 1:
                    # Measure execution time and memory usage for Feature-Based Heuristic
                    tracemalloc.start()
                    start_time = time.time()
                    col = agent1.get_move(controller.game)
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    metrics["agent1_execution_time"].append(end_time - start_time)
                    metrics["agent1_memory_usage"].append(peak / 10**6)
                else:
                    # Measure execution time and memory usage for Board-Based Heuristic
                    tracemalloc.start()
                    start_time = time.time()
                    col = agent2.get_best_move(controller.game)
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    metrics["agent2_execution_time"].append(end_time - start_time)
                    metrics["agent2_memory_usage"].append(peak / 10**6)

                # Execute the move
                controller.game.drop_piece(col)

                # Check if the game has ended
                winner = controller.game.check_winner()
                if winner:
                    controller.game.game_over = True
                    if winner == 1:
                        agent1_wins += 1
                    else:
                        agent2_wins += 1
                elif controller.game.is_draw():
                    controller.game.game_over = True
                    draws += 1
                else:
                    controller.game.switch_player()

        # Summarize results
        self.results.append({
            "agent1": agent1_name,
            "agent2": agent2_name,
            "agent1_wins": agent1_wins,
            "agent2_wins": agent2_wins,
            "draws": draws,
            "agent1_avg_execution_time": sum(metrics["agent1_execution_time"]) / len(metrics["agent1_execution_time"]),
            "agent2_avg_execution_time": sum(metrics["agent2_execution_time"]) / len(metrics["agent2_execution_time"]),
            "agent1_avg_memory_usage": sum(metrics["agent1_memory_usage"]) / len(metrics["agent1_memory_usage"]),
            "agent2_avg_memory_usage": sum(metrics["agent2_memory_usage"]) / len(metrics["agent2_memory_usage"]),
        })

    def print_results(self):
        """Print the results of the tests."""
        for result in self.results:
            print(f"\nMatch: {result['agent1']} vs {result['agent2']}")
            print(f"  {result['agent1']} Wins: {result['agent1_wins']}")
            print(f"  {result['agent2']} Wins: {result['agent2_wins']}")
            print(f"  Draws: {result['draws']}")
            print(f"  {result['agent1']} Avg Time: {result['agent1_avg_execution_time']:.6f} sec")
            print(f"  {result['agent2']} Avg Time: {result['agent2_avg_execution_time']:.6f} sec")
            print(f"  {result['agent1']} Avg Memory: {result['agent1_avg_memory_usage']:.6f} MB")
            print(f"  {result['agent2']} Avg Memory: {result['agent2_avg_memory_usage']:.6f} MB")


if __name__ == "__main__":
    tester = AlgorithmTester()
    tester.test_algorithms(num_games=1000)  # Run 10 games for testing
    tester.print_results()
