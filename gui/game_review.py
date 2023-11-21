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

    event = game.headers.get("Event", "Unknown Event")
    white_player = game.headers.get("White", "Unknown Player")
    black_player = game.headers.get("Black", "Unknown Player")
    result = game.headers.get("Result", "Unknown Result")

    # Create the plot title
    plot_title = f"{event}" #

    print("Saving game review data, please wait...")
    blunders = {}
    scores = []
    blunder_positions = []
    blunders_with_best_moves = {}

    for move_number, (move, move_info) in enumerate(zip(game.mainline_moves(), analysis_results), start=1):
        score = move_info['score'].score(mate_score=10000)
        scores.append(score / 100)  # Normalize score for graphing
        
        if move_number < len(analysis_results) - 1:
            next_score = analysis_results[move_number]['score'].score(mate_score=10000)
            if abs(next_score - score) > BLUNDER_THRESHOLD:
                blunder_positions.append(move_number)
                best_move = await analyzer.get_best_move(game, move_number)
                blunders_with_best_moves[str(move_number)] = best_move

    # print(blunders_with_best_moves)
    evaluations = [move_info['score'].score(mate_score=10000) for move_info in analysis_results]

    await db_manager.update_all_moves(unique_identifier, evaluations, blunders_with_best_moves)
    await db_manager.mark_reviewed(unique_identifier)

    if plot_evaluations:
        # scores = [result['score'].score(mate_score=10000) / 100 for result in analysis_results]
        
        plt.figure(figsize=(10, 6))
        moves = range(1, len(scores) + 1)
        plt.plot(moves, scores, marker='o')
        for blunder_pos in blunder_positions:
            plt.plot(blunder_pos, scores[blunder_pos - 1], marker='o', color='red')

        above_zero = [score > 0 for score in scores]
        below_zero = [score <= 0 for score in scores]

        plt.fill_between(moves, scores, 0, where=above_zero, interpolate=True, color='lightgray')
        plt.fill_between(moves, scores, 0, where=below_zero, interpolate=True, color='darkgray')

        plt.title(plot_title)
        plt.xlabel("Move Number")
        plt.ylabel("Evaluation")
        plt.xlim(left=1)
        plt.ylim(-10, 10)
        plt.grid(True)
        plt.show()

    await analyzer.close_engine()

# asyncio.run(analyze_games_from_db(db_manager, unique_identifier))