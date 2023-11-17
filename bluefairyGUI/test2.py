from database import ChessDBManager
import asyncio

db_manager = ChessDBManager(uri="mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority")
unique_identifier = "Live Chess-2023.11.08-loveinyouratoms-Hikaru-1653038eaec84aad3d18a48a6f0ba418b7df973d0a352d0d787943f89ebba0e8"
# pgn_string = await db_manager.fetch_game_pgn(unique_identifier)


from analysis import GameAnalyzer
import asyncio
import matplotlib.pyplot as plt
import chess.pgn
from database import ChessDBManager

async def analyze_games_from_db(db_manager, num_games, plot_evaluations=False):
    analyzer = GameAnalyzer("stockfish")
    await analyzer.init_engine()

    # Fetch games from the database
    cursor = db_manager.async_db[GAMES_COLLECTION].find().limit(num_games)
    games_from_db = await cursor.to_list(length=num_games)

    for i, game_data in enumerate(games_from_db):
        # Reconstruct PGN from game data
        pgn_string = db_manager.convert_to_pgn(game_data)
        game = chess.pgn.read_game(pgn_string)

        analysis_results = await analyzer.analyze_game_async(game)

        print(f"Game {i + 1} Metadata: {game_data['metadata']}")

        for move_number, (move, move_info) in enumerate(zip(game.mainline_moves(), analysis_results), 1):
            print(f"Move {move_number} ({move}): Evaluation: {move_info['score']}")

            # Update move evaluations in the database
            move_update = {"$set": {f"moves.{move_number}.evaluation": move_info['score']}}
            await db_manager.async_db[MOVES_COLLECTION].update_one({"game_id": game_data["_id"]}, move_update)

        if plot_evaluations:
            scores = [result['score'].score(mate_score=10000) / 100 for result in analysis_results]
            # ... (plotting code)

    await analyzer.close_engine()

# Usage
db_uri = "mongodb://localhost:27017"
db_manager = ChessDBManager(db_uri)
asyncio.run(analyze_games_from_db(db_manager, num_games=10, plot_evaluations=True))
