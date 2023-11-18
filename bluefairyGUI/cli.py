import sys
import whale
import asyncio
import logging
from scraper import ChessComPlayerArchives
from database import ChessDBManager

def display_ascii_title():
    ascii_art = """
    ______ _             __      _             
    | ___ \ |           / _|    (_)            
    | |_/ / |_   _  ___| |_ __ _ _ _ __ _   _  
    | ___ \ | | | |/ _ \  _/ _` | | '__| | | | 
    | |_/ / | |_| |  __/ || (_| | | |  | |_| | 
    \____/|_|\__,_|\___|_| \__,_|_|_|   \__, | 
                                         __/ | 
                                        |___/  
    """
    print(ascii_art)

def get_player_name():
    return input("Enter player name: ")

async def search_games_in_db(player_name, elo_range, game_id):
    db_manager = ChessDBManager("mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority")
    games = await db_manager.search_games(player_name, elo_range, game_id)
    db_manager.close_connection()
    return games

async def handle_game_downloads_and_ingestion(source, player_name, months):
    uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
    db_manager = ChessDBManager(uri)

    # Download and process games
    if source.lower() == 'chess.com':
        player_archives = ChessComPlayerArchives(player_name)
        player_archives.fetch_and_download_archives(months, 'games')
        await whale.main()
    elif source.lower() == 'lichess':
        print("Lichess option is not available at the moment.")
        return

    db_manager.close_connection()

def get_search_criteria():
    print("Search database by player name, elo range, and/or a gameID.")
    player_name = input("Player name: ")
    elo_range = input("Elo range: ")
    game_id = input("Game ID: ")
    return player_name, elo_range, game_id

async def main():
    display_ascii_title()

    player_name, elo_range, game_id = get_search_criteria()
    games = await search_games_in_db(player_name, elo_range, game_id)

    if not games:
        print("No games found based on the provided criteria.")
        import_choice = input("Would you like to import games? (Y/n): ")
        if import_choice.lower() == 'y':
            choice = input("Choose a source (chess.com/lichess): ")
            months = input("How many months of game data would you like to download (for chess.com): ")
            await handle_game_downloads_and_ingestion(choice, player_name, int(months))
            games = await search_games_in_db(player_name, elo_range, game_id)

    if games:
        print("Select a game from the list:")
        for i, game in enumerate(games, start=1):
            print(f"{i}. {game}")  # Format this line based on how your game data is structured
        game_choice = int(input("Enter the number of the game you want to analyze: "))
        selected_game = games[game_choice - 1]
        # Add functionality to analyze or display the selected game

if __name__ == "__main__":
    asyncio.run(main())