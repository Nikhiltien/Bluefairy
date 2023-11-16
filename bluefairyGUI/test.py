from database import ChessDBManager
import whale
import logging

async def main():
    db_manager = ChessDBManager()
    directory = 'games'
    parsed_games = await whale.parse_pgn_files(directory)

    for game in parsed_games:
        logging.info(f"Game metadata: {game['Metadata']}")
        logging.info(f"First few moves: {game['Moves'][:5]}")  # Print first few moves for each game

    game_id = await db_manager.insert_game(parsed_games)
    print(f"Inserted game with ID: {game_id}")

    db_manager.close_connection()

import asyncio
asyncio.run(main())