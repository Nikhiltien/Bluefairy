from database import ChessDBManager
import whale
import logging

async def main():
    uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
    db_manager = ChessDBManager(uri)
    directory = 'games'
    parsed_games = await whale.parse_pgn_files(directory)

    for game in parsed_games:
        # Extract and store game metadata
        game_metadata = game['Metadata']
        moves = game['Moves']
        game_id = await db_manager.insert_game(game_metadata, moves)
        logging.info(f"Processed game with ID: {game_id}")

        # Update player profiles
        white_player = game_metadata['White']
        black_player = game_metadata['Black']
        white_elo = game_metadata.get('WhiteElo', 'Unknown')
        black_elo = game_metadata.get('BlackElo', 'Unknown')
        await db_manager.upsert_player_profile(white_player, white_elo)
        await db_manager.upsert_player_profile(black_player, black_elo)

    db_manager.close_connection()

import asyncio
asyncio.run(main())