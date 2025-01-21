# Connect-4 AI Project

This repository contains an academic study on the AI strategies for solving the classic Connect-4 game. The focus of this project is the paper (final report), which evaluates and compares various algorithms and heuristics, supported by code implementations and experimental results.

---

## Abstract

Connect-4 is a two-player strategy game where various artificial intelligence techniques can be explored. The study evaluates multiple AI algorithms and heuristics to identify strategies for solving Connect-4. It explores the Monte Carlo Tree Search (MCTS), Minimax algorithm variations, and heuristic approaches, such as feature-based and board-based methods. Through testing, the project assesses different agents’ computation time, memory usage, and win rates. Results highlight the first-player advantage, the effectiveness of Minimax with Alpha-Beta Pruning, and the high computational cost of MCTS.

---

## Repository Structure

### 1. **`FinalReport.pdf`**
   - The main academic paper detailing the research, algorithms, experiments, and conclusions.

### 2. **`Presentation.pdf`**
   - Supporting presentation slides summarizing the project, including visuals and key insights.

### 3. **`codes/`**
   This folder contains all the code implementations for the Connect-4 game and the AI algorithms. Below is a breakdown of the key files:

   - **`Main.py`**: Entry point to run the game. Initializes the game environment and manages gameplay.
   - **`Environment.py`**: Contains the main game logic, like board initialization.
   - **`BoardHeuristic.py`**: Implements the heuristic AI, evaluating board states based on specific strategies and patterns.
   - **`RandomAgent.py`**: Defines the logic for the random agent, which makes purely random moves.
   - **`GameController.py`**: Manages interactions between the players, game logic, and AI agents.
   - **`Utility.py`**: Provides utility functions for common board operations, such as printing the board and checking valid moves.
   - **`Constants.py`**: Defines constants used throughout the project, such as board dimensions and player symbols.
   - **`MINIMAX_tester.py`**: A script to test and evaluate the performance of the Minimax algorithm.
   - **`MonteCarloTreeSearch.py`**: A script to test the Monte Carlo Tree Search algorithm.
   - **`AlphaBeta_Monte.py`**: A script that compares Monte Carlo Tree Search and Minimax with Alpha-Beta Pruning.

---

### **How to Run the Code**

1. Clone the repository:
   ```bash
   git clone https://github.com/anna-asatryan/Connect-4-AI-Project.git
