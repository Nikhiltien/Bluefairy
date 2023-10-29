# Bluefairy

Bluefairy is a non UCI compliant chess engine written in Rust, developed with a unique approach. Instead of traditional reinforcement techniques through self-play, Bluefairy uses a combination of Deep Q-Networks (DQNs) and Long Short-Term Memory (LSTM) layers to generate a "winning chances" score from training on human games. The engine is not designed to search for the objective best move, but to emulate and exploit different human playing styles and patterns.
