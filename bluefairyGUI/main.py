from evaluate import GameAnalyzer
import asyncio
import matplotlib.pyplot as plt
import chess.pgn

async def analyze_first_games(directory, num_games=1):
    analyzer = GameAnalyzer("stockfish")

    await analyzer.init_engine()
    all_games = analyzer.load_games_from_directory(directory)

    # Check if there are enough games loaded
    if len(all_games) < num_games:
        print(f"Not enough games in the directory. Found only {len(all_games)} games.")
        await analyzer.close_engine()
        return

    for i in range(min(num_games, len(all_games))):
        game = all_games[i]
        analysis_results = await analyzer.analyze_game_async(game)

        # Extract metadata from the game
        metadata = {
            "Event": game.headers.get("Event", "N/A"),
            "White": game.headers.get("White", "N/A"),
            "Black": game.headers.get("Black", "N/A"),
            "WhiteElo": game.headers.get("WhiteElo", "N/A"),
            "BlackElo": game.headers.get("BlackElo", "N/A"),
            "TimeControl": game.headers.get("TimeControl", "N/A")
        }

        print(f"Game {i + 1} Metadata: {metadata}")

        # Displaying results for each game
        move_number = 1
        for move, move_info in zip(game.mainline_moves(), analysis_results):
            print(f"Move {move_number} ({move}): Evaluation: {move_info['score']}")
            move_number += 1
        print("\n")

        scores = [result['score'].score(mate_score=10000) / 100 for result in analysis_results]

        # Plotting
        plt.figure(figsize=(10, 6))
        moves = range(1, len(scores) + 1)
        plt.plot(moves, scores, marker='o')

        # Create boolean arrays for conditions
        above_zero = [score > 0 for score in scores]
        below_zero = [score <= 0 for score in scores]

        # Shading areas above and below 0
        plt.fill_between(moves, scores, 0, where=above_zero, interpolate=True, color='lightgray')
        plt.fill_between(moves, scores, 0, where=below_zero, interpolate=True, color='darkgray')

        # Graph customization
        plt.title(f"Game {i + 1} Evaluation")
        plt.xlabel("Move Number")
        plt.ylabel("Evaluation")
        plt.xlim(left=0)
        plt.ylim(-10, 10)
        plt.grid(True)
        plt.show()

directory_path = "games"
asyncio.run(analyze_first_games(directory_path))