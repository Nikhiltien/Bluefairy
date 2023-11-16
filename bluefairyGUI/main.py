from analysis import GameAnalyzer
import asyncio
import matplotlib.pyplot as plt
import chess.pgn

async def analyze_games(directory, num_games, plot_evaluations=False):
    analyzer = GameAnalyzer("stockfish")

    await analyzer.init_engine()
    all_games = analyzer.load_games_from_directory(directory)

    if not all_games:
        print("No games found in the directory.")
        await analyzer.close_engine()
        return

    games_to_analyze = all_games if num_games <= 0 else all_games[:num_games]

    for i, game in enumerate(games_to_analyze):
        analysis_results = await analyzer.analyze_game_async(game)

        metadata = {
            "Event": game.headers.get("Event", "N/A"),
            "White": game.headers.get("White", "N/A"),
            "Black": game.headers.get("Black", "N/A"),
            "WhiteElo": game.headers.get("WhiteElo", "N/A"),
            "BlackElo": game.headers.get("BlackElo", "N/A"),
            "TimeControl": game.headers.get("TimeControl", "N/A")
        }

        print(f"Game {i + 1} Metadata: {metadata}")

        for move_number, (move, move_info) in enumerate(zip(game.mainline_moves(), analysis_results), 1):
            print(f"Move {move_number} ({move}): Evaluation: {move_info['score']}")

        if plot_evaluations:
            scores = [result['score'].score(mate_score=10000) / 100 for result in analysis_results]
            
            plt.figure(figsize=(10, 6))
            moves = range(1, len(scores) + 1)
            plt.plot(moves, scores, marker='o')

            above_zero = [score > 0 for score in scores]
            below_zero = [score <= 0 for score in scores]

            plt.fill_between(moves, scores, 0, where=above_zero, interpolate=True, color='lightgray')
            plt.fill_between(moves, scores, 0, where=below_zero, interpolate=True, color='darkgray')

            plt.title(f"Game {i + 1} Evaluation")
            plt.xlabel("Move Number")
            plt.ylabel("Evaluation")
            plt.xlim(left=0)
            plt.ylim(-10, 10)
            plt.grid(True)
            plt.show()

directory_path = "games"
asyncio.run(analyze_games(directory_path, num_games=0, plot_evaluations=False))