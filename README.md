# Bluefairy

Bluefairy is a non-UCI compliant chess engine and GUI, developed with a unique approach. Instead of using traditional reinforcement techniques with Minimax algorithms and self-play, Bluefairy uses a combination of Deep Q-Networks (DQNs), Long Short-Term Memory (LSTM) layers and a hyper-parameterized board state to calculate a "winning chances" score from training on games, puzzles, and human-opponent play. The engine is not designed to search for the objective best move, but to emulate and exploit different human playing styles and patterns. The engine is "zero depth" because it does not evaluate the opponent's move when considering its own. Instead, it infers resulting possible board states from a given move to determine what move to make.

# Architecture

Deep Neural Network (DNN)
 		Architecture: A multi-layer feedforward neural network. The network takes the board state, ELO rating, time remaining when available, and other parameters as input and outputs a "winning chances" score for each legal move.

   Training Data: Extensively parameterized data from human games, focusing on board states that are statistically favorable for winning against humans.
 		Optimization: Backpropagation with optimization algorithms such as Adam or RMSprop.
 		Regularization: Techniques like dropout or L1/L2 regularization to prevent overfitting.
 		Activation Functions: ReLU for hidden layers and a softmax for the output layer to interpret the results as probabilities.

Reinforcement Learning (RL)
 		Algorithm: Deep Q-Network (DQN) combined with techniques like experience replay.
 		State Space: The board state, ELO rating, time remaining and other parameters constitute the state space.
 		Action Space: All legal moves in the current board state.
 		Reward Function: Rewards are given for achieving statistically favorable board states against humans. Penalties for “unfavorable states”.
 		Exploration-Exploitation Strategy: Epsilon-greedy strategy, where the model occasionally explores new moves rather than exploiting known good moves.

Rule-Based Heuristics
 		Opening Book: Predefined set of good opening moves based on traditional chess theory.
 		Time-Based Rules: Quick decisions when the clock is running low.
 		ELO-Based Rules: Simple strategies for lower ELO levels where prediction of human behavior is easier.

Ensemble Method
 		Weighting Mechanism: The ensemble will weigh the output of the DNN, RL model, and rule-based heuristics based on their reliability and the current game state.
 		Decision Making: Choose the move with the highest "winning chances" score after ensemble weighting.

Model Interpretability
 		Techniques: Methods like SHAP (SHapley Additive exPlanations) or LIME (Local Interpretable Model-agnostic Explanations) to interpret the model's decisions for debugging and improvement.

<!-- - /models
- /src
    - /engine
        - chess.rs
        - board_evaluator.rs
    - /utils
        - some_utility.rs
    - main.rs -->
