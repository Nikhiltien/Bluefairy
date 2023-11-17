from analysis import GameAnalyzer
import asyncio
from database import ChessDBManager

uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
db_manager = ChessDBManager(uri)
unique_identifiers = "Live Chess-2023.11.01-ITWillyB-niki0x-974f508f2e5258e017e67e7f8d36ad03d8e8c8a937e077ba873178257e125258"
analyzer = GameAnalyzer("stockfish")
analyzer.load_eco_book()

async def analyze_games_from_db(db_manager, unique_identifiers):
    await analyzer.init_engine()

    _, moves = await db_manager.get_game_by_identifier(unique_identifiers)

    moves = db_manager.convert_moves(moves)
    print(moves)

    eco_code, opening_name = analyzer.find_opening(moves)
    print(f"Opening: {opening_name}, ECO Code: {eco_code}")

    await analyzer.close_engine()

# Usage
asyncio.run(analyze_games_from_db(db_manager, unique_identifiers))