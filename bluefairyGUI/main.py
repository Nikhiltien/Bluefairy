from evaluate import GameAnalyzer
import asyncio
import chess.pgn

async def analyze_first_games(directory, num_games=3):
    analyzer = GameAnalyzer("../engines/stockfish")

    await analyzer.init_engine()
    all_games = analyzer.load_games_from_directory(directory)

    # Check if there are enough games loaded
    if len(all_games) < num_games:
        print(f"Not enough games in the directory. Found only {len(all_games)} games.")
        await analyzer.close_engine()
        return

    for i in range(num_games):
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

    await analyzer.close_engine()

directory_path = "games"
asyncio.run(analyze_first_games(directory_path))