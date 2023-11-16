from database import ChessDBManager
import whale
import logging

async def main():
    uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
    db_manager = ChessDBManager(uri)
    directory = 'games'
    parsed_games = await whale.parse_pgn_files(directory)

    for game in parsed_games:
        logging.info(f"Game metadata: {game['Metadata']}")
        logging.info(f"First 5 moves: {game['Moves'][:5]}")

        # Format game data
        game_data = {
            "metadata": game['Metadata'],
            "moves": game['Moves']
        }

        # Insert game into database
        game_id = await db_manager.insert_game(game_data)
        logging.info(f"Inserted game with ID: {game_id}")

    db_manager.close_connection()

import asyncio
asyncio.run(main())