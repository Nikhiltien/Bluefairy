import sys
import whale
import asyncio
import logging
from prettytable import PrettyTable
from game_review import analyze_games_from_db
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
    print("v0.0.1")

def get_player_name():
    return input("Enter player name: ")

async def search_games_in_db(player_name, elo_range, game_id):
    uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
    db_manager = ChessDBManager(uri)
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

async def refresh_player_profile(player_name):
    """
    Refreshes the player profile by fetching the last month's game data.
    """
    print(f"Refreshing profile for {player_name}...")
    await handle_game_downloads_and_ingestion('chess.com', player_name, 1)
    print("Profile refresh complete.")

def get_search_criteria():
    print("Search database by player name, elo range, and/or a gameID.")
    player_name = input("Player name: ")
    elo_range = input("Elo range: ")
    game_id = input("Game ID: ")
    return player_name, elo_range, game_id

async def search_player_profile():
    player_name = input("Enter player name: ")
    uri = "mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"
    db_manager = ChessDBManager(uri)
    
    # Fetch player profile and win/loss ratios
    player_profile = db_manager.get_player_data({"name": player_name})
    win_loss_ratios = await db_manager.update_wr(player_name)

    db_manager.close_connection()

    if player_profile:
        # Creating a PrettyTable instance
        table = PrettyTable()
        table.field_names = ["Username", "Elo", "Win Ratio (White)", "Win Ratio (Black)"]

        # Adding player data and win/loss ratios to the table
        table.add_row([
            player_profile.get('name', 'N/A'), 
            player_profile.get('elo', 'N/A'),
            f"{win_loss_ratios['white_win_ratio'] * 100:.2f}%",
            f"{win_loss_ratios['black_win_ratio'] * 100:.2f}%"
        ])

        print(table)
        while True:
            choice = input("Options: \n1. Refresh Profile\n2. Return to Main Menu\nEnter choice (1/2): ")
            if choice == '1':
                await refresh_player_profile(player_name)
                break  # Break after refreshing to avoid repetition
            elif choice == '2':
                break  # Return to main menu
            else:
                print("Invalid choice. Please enter 1 or 2.")
    else:
        print(f"No profile found for player '{player_name}'.")

def format_game_list(games, page=1, total_pages=1):
    for i, game in enumerate(games, start=1):
        if game is None:
            continue  # Skip None values

        event = game.get('Event', 'Unknown Event')
        date = game.get('Date', 'Unknown Date')
        white = game.get('White', 'Unknown')
        black = game.get('Black', 'Unknown')
        elo_white = game.get('WhiteElo', 'N/A')
        elo_black = game.get('BlackElo', 'N/A')
        result = game.get('Result', 'Unknown Result')
        opening = game.get('Opening', 'Unknown')
        reviewed_mark = '*' if game.get('review') else ''
        
        print(f"{i}. {reviewed_mark}{date}, {white} ({elo_white}) vs. {black} ({elo_black}), {result}, {opening}")
    
    print(f"Page {page}/{total_pages} - Enter 1 or 9 to navigate, '/m' for main menu")

async def search_and_display_games():
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
        games_per_page = 7
        # Padding pages for navigation
        pages = [games[i:i + games_per_page] for i in range(0, len(games), games_per_page)]
        for page in pages:
            page.insert(0, None)  # Placeholder for '1'
            page.append(None)     # Placeholder for '9'

        total_pages = len(pages)
        page_number = 1

        while True:
            displayed_games = pages[page_number - 1]
            format_game_list(displayed_games, page_number, total_pages)

            choice = input("Enter the game number to analyze or navigate: ")

            if choice == '1' and page_number > 1:
                page_number -= 1
            elif choice == '9' and page_number < total_pages:
                page_number += 1
            elif choice == '/m':
                return
            elif choice.isdigit():
                game_index = int(choice) - 1
                if 1 <= game_index <= len(displayed_games) and displayed_games[game_index] is not None:
                    selected_game = displayed_games[game_index]
                    unique_identifier = selected_game['unique_identifier']
                    await analyze_games_from_db(ChessDBManager("mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority"), unique_identifier)
                else:
                    print("Invalid game number.")
            else:
                print("Invalid input.")

async def main():
    display_ascii_title()

    while True:
        choice = input("Choose an option: \n1. Search for Player Profile\n2. Search for Game\nEnter choice (1/2) or '/m' to exit: ")
        if choice == '/m':
            break
        elif choice == '1':
            await search_player_profile()
        elif choice == '2':
            await search_and_display_games()
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    asyncio.run(main())