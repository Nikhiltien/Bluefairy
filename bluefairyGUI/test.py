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
        game_id = await db_manager.insert_game(game_metadata)
        logging.info(f"Inserted game with ID: {game_id}")

        # Extract and store moves
        await db_manager.insert_moves(game_id, game['Moves'])
        logging.info(f"Inserted moves for game ID: {game_id}")

        # Update player profiles
        white_player = game_metadata['White']
        black_player = game_metadata['Black']
        white_elo = game_metadata.get('WhiteElo')
        black_elo = game_metadata.get('BlackElo')
        db_manager.update_player_profile(white_player, {"elo": white_elo})
        db_manager.update_player_profile(black_player, {"elo": black_elo})

    db_manager.close_connection()

import asyncio
asyncio.run(main())