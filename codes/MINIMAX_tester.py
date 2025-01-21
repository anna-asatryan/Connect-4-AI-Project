import time
import tracemalloc
from Minimax_variations import MinimaxAI, MinimaxAIWithPruning
from Environment import Connect4

def simulate_games_with_metrics(game_class, depth1, depth2, num_games=10):
    """
    Simulate games between two agents with alternating starts and track their performance metrics.
    Args:
        game_class: Class of the Connect4 game instance.
        depth1: Depth of the first agent (MinimaxAI).
        depth2: Depth of the second agent (MinimaxAI).
        num_games: Total number of games to simulate (must be even for equal starts).
    """
    agent1 = MinimaxAIWithPruning(depth1)  # Switch agents to MinimaxAIWithPruning() for testing MINIMAX with alpha-beta pruning
    agent2 = MinimaxAIWithPruning(depth2)

    results = {"agent1_wins": 0, "agent2_wins": 0, "draws": 0}
    metrics = {
        "agent1": {"total_time": 0, "total_memory": 0, "move_count": 0},
        "agent2": {"total_time": 0, "total_memory": 0, "move_count": 0},
    }

    agent1_start = num_games // 2  # Number of games where agent1 starts
    agent2_start = num_games - agent1_start  # Number of games where agent2 starts

    for game_num in range(num_games):
        game = game_class()
        game.reset_game()

        # Determine starting agent
        if game_num < agent1_start:
            current_agent = agent1
            next_agent = agent2
            current_agent_name = "agent1"
            next_agent_name = "agent2"
        else:
            current_agent = agent2
            next_agent = agent1
            current_agent_name = "agent2"
            next_agent_name = "agent1"

        # Play the game
        while not game.game_over:
            # Measure time and memory for the current move
            tracemalloc.start()
            start_time = time.time()

            col = current_agent.get_best_move(game)

            end_time = time.time()
            current_memory, _ = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Update metrics
            metrics[current_agent_name]["total_time"] += (end_time - start_time)
            metrics[current_agent_name]["total_memory"] += current_memory / (1024 * 1024)  # Convert to MB
            metrics[current_agent_name]["move_count"] += 1

            # Make the move if valid
            if game.is_valid_location(col):
                game.drop_piece(col)

                # Check game state
                if game.check_winner():
                    results[f"{current_agent_name}_wins"] += 1
                    game.game_over = True
                    break
                elif game.is_draw():
                    results["draws"] += 1
                    game.game_over = True
                    break

                # Switch agents
                game.switch_player()
                current_agent, next_agent = next_agent, current_agent
                current_agent_name, next_agent_name = next_agent_name, current_agent_name

    # Calculate averages for each agent
    for agent_name in metrics:
        metrics[agent_name]["avg_time"] = metrics[agent_name]["total_time"] / metrics[agent_name]["move_count"]
        metrics[agent_name]["avg_memory"] = metrics[agent_name]["total_memory"] / metrics[agent_name]["move_count"]

    return results, metrics


def test_depth_pairs(game_class, depth_pairs, num_games_per_pair):
    """
    Test multiple pairs of depths for MinimaxAI.
    Args:
        game_class: Class of the Connect4 game instance.
        depth_pairs: List of depth pairs to test.
        num_games_per_pair: Number of games to simulate for each pair.
    """
    for depth1, depth2 in depth_pairs:
        print(f"\nTesting Depth {depth1} vs Depth {depth2}...")
        results, metrics = simulate_games_with_metrics(game_class, depth1, depth2, num_games_per_pair)

        print(f"\nResults for Depth {depth1} vs Depth {depth2}:")
        print(f"Agent with Depth {depth1} Wins: {results['agent1_wins']}")
        print(f"Agent with Depth {depth2} Wins: {results['agent2_wins']}")
        print(f"Draws: {results['draws']}")

        print("\nPerformance Metrics:")
        print(f"Agent Depth {depth1} - Average Time: {metrics['agent1']['avg_time']:.6f} sec, "
              f"Average Memory: {metrics['agent1']['avg_memory']:.6f} MB")
        print(f"Agent Depth {depth2} - Average Time: {metrics['agent2']['avg_time']:.6f} sec, "
              f"Average Memory: {metrics['agent2']['avg_memory']:.6f} MB")


if __name__ == "__main__":
    depth_pairs = [(1, 2), (2, 3), (3, 4), (4, 5), (2, 6)]
    num_games_per_pair = 10

    # Run the tests
    test_depth_pairs(Connect4, depth_pairs, num_games_per_pair)
