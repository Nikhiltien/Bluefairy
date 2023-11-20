from analysis import GameAnalyzer
import asyncio
import io
import chess.pgn
from database import ChessDBManager
import matplotlib.pyplot as plt

# uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
# db_manager = ChessDBManager(uri)
# unique_identifier = "Live Chess-2023.11.01-ITWillyB-niki0x-974f508f2e5258e017e67e7f8d36ad03d8e8c8a937e077ba873178257e125258"

BLUNDER_THRESHOLD = 150

async def analyze_games_from_db(db_manager, unique_identifier, plot_evaluations=True):
    analyzer = GameAnalyzer("stockfish")
    analyzer.load_eco_book()
    await analyzer.init_engine()

    game, moves = await db_manager.get_game_by_identifier(unique_identifier)
    if not game or not moves:
        print(f"No game data found for identifier: {unique_identifier}")
        return

    eco_moves = db_manager.convert_moves(moves)

    pgn_string = db_manager.convert_to_pgn(game, moves)

    pgn_io = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn_io)

    eco_code, opening_name = analyzer.find_opening(eco_moves)
    await db_manager.update_game_with_opening(unique_identifier, eco_code)

    analysis_results = await analyzer.analyze_game_async(game)

    metadata = {
        "Event": game.headers.get("Event", "N/A"),
        "White": game.headers.get("White", "N/A"),
        "Black": game.headers.get("Black", "N/A"),
        "Result": game.headers.get("Result", "N/A"),
    }
    game_description = f"{metadata['Date']}, {metadata['White']} ({metadata['WhiteElo']}) vs. {metadata['Black']} ({metadata['BlackElo']}), {metadata['Result']}"

    print("Saving game review data, please wait...")
    evaluations = [move_info['score'].score(mate_score=10000) for move_info in analysis_results]
    await db_manager.update_all_moves(unique_identifier, evaluations)
    await db_manager.mark_reviewed(unique_identifier)

    if plot_evaluations:
        scores = [result['score'].score(mate_score=10000) / 100 for result in analysis_results]
        
        plt.figure(figsize=(10, 6))
        moves = range(1, len(scores) + 1)
        plt.plot(moves, scores, marker='o')

        above_zero = [score > 0 for score in scores]
        below_zero = [score <= 0 for score in scores]

        plt.fill_between(moves, scores, 0, where=above_zero, interpolate=True, color='lightgray')
        plt.fill_between(moves, scores, 0, where=below_zero, interpolate=True, color='darkgray')

        plt.title(game_description)
        plt.xlabel("Move Number")
        plt.ylabel("Evaluation")
        plt.xlim(left=1)
        plt.ylim(-10, 10)
        plt.grid(True)
        plt.show()

    await analyzer.close_engine()

# asyncio.run(analyze_games_from_db(db_manager, unique_identifier))