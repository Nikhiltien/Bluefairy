from analysis import GameAnalyzer
import asyncio
import io
import chess.pgn
from database import ChessDBManager
import matplotlib.pyplot as plt

uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
db_manager = ChessDBManager(uri)
unique_identifier = "Live Chess-2023.11.01-ITWillyB-niki0x-974f508f2e5258e017e67e7f8d36ad03d8e8c8a937e077ba873178257e125258"

async def analyze_games_from_db(db_manager, unique_identifier, plot_evaluations=True):
    analyzer = GameAnalyzer("stockfish")
    await analyzer.init_engine()

    game, moves = await db_manager.get_game_by_identifier(unique_identifier)
    if not game or not moves:
        print(f"No game data found for identifier: {unique_identifier}")
        return

    pgn_string = db_manager.convert_to_pgn(game, moves)

    pgn_io = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn_io)

    analysis_results = await analyzer.analyze_game_async(game)

    metadata = {
        "Event": game.headers.get("Event", "N/A"),
        "White": game.headers.get("White", "N/A"),
        "Black": game.headers.get("Black", "N/A"),
        "Result": game.headers.get("Result", "N/A"),
    }

    print("Storing evaluation, please wait...")
    for move_number, (move, move_info) in enumerate(zip(game.mainline_moves(), analysis_results), 1):
        score = move_info['score'].score(mate_score=10000)
        # print(f"Move {move_number} ({move}): Evaluation: {score}")
        await db_manager.upsert_move(unique_identifier, move_number, score)

    if plot_evaluations:
        scores = [result['score'].score(mate_score=10000) / 100 for result in analysis_results]
        
        plt.figure(figsize=(10, 6))
        moves = range(1, len(scores) + 1)
        plt.plot(moves, scores, marker='o')

        above_zero = [score > 0 for score in scores]
        below_zero = [score <= 0 for score in scores]

        plt.fill_between(moves, scores, 0, where=above_zero, interpolate=True, color='lightgray')
        plt.fill_between(moves, scores, 0, where=below_zero, interpolate=True, color='darkgray')

        plt.title(f"{metadata['Event']} Evaluation")
        plt.xlabel("Move Number")
        plt.ylabel("Evaluation")
        plt.xlim(left=0)
        plt.ylim(-10, 10)
        plt.grid(True)
        plt.show()

    await analyzer.close_engine()

# asyncio.run(analyze_games_from_db(db_manager, unique_identifier))