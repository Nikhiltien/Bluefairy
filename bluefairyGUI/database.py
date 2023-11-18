import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import asyncio
import motor
import logging
from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_NAME = "Bluefairy"
PLAYERS_COLLECTION = "players"
GAMES_COLLECTION = "games"
MOVES_COLLECTION = "moves"

class ChessDBManager:
    def __init__(self, uri="mongodb://localhost:27017"):
        self.client = MongoClient(uri)
        self.db = self.client[DATABASE_NAME]
        self.async_client = AsyncIOMotorClient(uri)
        self.async_db = self.async_client[DATABASE_NAME]

    def close_connection(self):
        self.client.close()

    @staticmethod
    def generate_game_hash(moves):
        """Generate a hash from the list of moves."""
        move_string = ' '.join([f"{move['ply']} {move['move']}" for move in moves])
        return hashlib.sha256(move_string.encode()).hexdigest()
    
    async def upsert_player_profile(self, player_name, elo):
        """Create or update a player profile."""
        result = await self.async_db[PLAYERS_COLLECTION].update_one(
            {"name": player_name},
            {"$set": {"elo": elo}},
            upsert=True  # Creates a new document if one doesn't exist
        )
        return result.upserted_id or result.modified_count
    
    def get_player_data(self, query):
        """Fetch player data based on a query."""
        player_data = self.db[PLAYERS_COLLECTION].find_one(query)
        return player_data
    
    def delete_player_profile(self, player_id):
        """Delete a player profile from the database."""
        result = self.db[PLAYERS_COLLECTION].delete_one({"player_id": player_id})
        return result.deleted_count
    
    async def get_game_by_identifier(self, unique_identifier):
        """Check if a game with the given unique identifier exists."""
        game = await self.async_db[GAMES_COLLECTION].find_one({"unique_identifier": unique_identifier})
        if not game:
            return None, None  # Return None for both game and moves if the game is not found

        moves_document = await self.async_db[MOVES_COLLECTION].find_one({"game_id": game['_id']})
        moves = moves_document['moves'] if moves_document else None
        return (game, moves)

    async def insert_game(self, game_metadata, moves):
        """Insert a new chess game into the games collection if it doesn't exist."""
        game_hash = self.generate_game_hash(moves)
        unique_identifier = f"{game_metadata['Event']}-{game_metadata['Date']}-{game_metadata['White']}-{game_metadata['Black']}-{game_hash}"
        existing_game, existing_moves = await self.get_game_by_identifier(unique_identifier)
        if existing_game:
            print(f"GameID {existing_game['_id']} already exists.")
            return unique_identifier

        game_metadata['unique_identifier'] = unique_identifier
        result = await self.async_db[GAMES_COLLECTION].insert_one(game_metadata)
        game_id = result.inserted_id
        await self.insert_moves(game_id, moves)
        return unique_identifier
    
    async def search_games(self, player_name=None, elo_range=None, game_id=None):
        """Search for games based on player name, elo range, or game ID."""
        query = {}

        if player_name:
            # Assuming 'White' and 'Black' fields store player names
            query["$or"] = [{"White": player_name}, {"Black": player_name}]

        if elo_range:
            # You'll need to parse the elo_range and form a query
            pass

        if game_id:
            query["game_id"] = game_id

        cursor = self.async_db[GAMES_COLLECTION].find(query)
        return [game async for game in cursor]

    async def get_games_by_player(self, player_id):
        """Retrieve chess games involving a specific player."""
        cursor = self.async_db[GAMES_COLLECTION].find({"players": player_id})
        return [game async for game in cursor]

    async def update_game(self, game_id, update_data):
        """Update details of a specific game."""
        result = await self.async_db[GAMES_COLLECTION].update_one({"game_id": game_id}, {"$set": update_data})
        return result.modified_count

    async def delete_game(self, game_id):
        """Delete a specific game from the database."""
        result = await self.async_db[GAMES_COLLECTION].delete_one({"game_id": game_id})
        return result.deleted_count
    
    async def fetch_game_pgns(self, unique_identifiers):
        pgns = []
        for unique_identifier in unique_identifiers:
            game = await self.async_db[GAMES_COLLECTION].find_one({"unique_identifier": unique_identifier})
            if not game:
                continue

            moves_document = await self.async_db[MOVES_COLLECTION].find_one({"game_id": game['_id']})
            if not moves_document:
                continue

            moves = moves_document['moves']
            pgn_string = self.convert_to_pgn(game, moves)
            pgns.append(pgn_string)

        return pgns
    
    def convert_to_pgn(self, game_metadata, moves):
        pgn_parts = []

        # Add headers
        pgn_parts.append(f'[Event "{game_metadata.get("Event", "Unknown")}"]')
        pgn_parts.append(f'[Site "{game_metadata.get("Site", "Unknown")}"]')
        pgn_parts.append(f'[Date "{game_metadata.get("Date", "????")}"]')
        pgn_parts.append(f'[Round "{game_metadata.get("Round", "?")}"]')
        pgn_parts.append(f'[White "{game_metadata.get("White", "Unknown")}"]')
        pgn_parts.append(f'[Black "{game_metadata.get("Black", "Unknown")}"]')
        pgn_parts.append(f'[Result "{game_metadata.get("Result", "*")}"]')

        pgn_parts.append("\n\n")

        for i, move in enumerate(moves):
            if i % 2 == 0:  # White's move
                # Add move number before white's move
                pgn_parts.append(f"{(i // 2) + 1}.")
                pgn_parts.append(move['move'])
            else:  # Black's move
                # Add move number before black's move
                pgn_parts.append(f"{(i // 2) + 1}...")
                pgn_parts.append(move['move'])
            
            # Add clock annotation if available
            if 'time' in move:
                time_formatted = self.format_time(move['time'])
                pgn_parts.append(f"{{[%clk {time_formatted}]}}")

        pgn_string = " ".join(pgn_parts)
        return pgn_string
    
    def convert_moves(self, moves, include_time=False):
        pgn_parts = []

        # Process moves
        for i, move in enumerate(moves):
            # Add move number for both white's and black's moves
            move_number = (i // 2) + 1
            if i % 2 == 0:  # White's move
                formatted_move = f"{move_number}.{move['move']}"
            else:  # Black's move
                formatted_move = f"{move['move']}"

            pgn_parts.append(formatted_move)

            # Add clock annotation if available and included
            if include_time and 'time' in move:
                time_formatted = self.format_time(move['time'])
                pgn_parts.append(f"{{[%clk {time_formatted}]}}")

        pgn_string = " ".join(pgn_parts)

        moves_list = pgn_string.split(' ')
        formatted_moves = []

        for move in moves_list:
            # Append each move to the list
            formatted_moves.append(move)

        eco_moves = tuple(formatted_moves)

        return eco_moves
    
    def format_time(self, time_in_seconds):
        """Format time in seconds into a clock annotation format (H:MM:SS)."""
        hours = int(time_in_seconds // 3600)
        minutes = int((time_in_seconds % 3600) // 60)
        seconds = int(time_in_seconds % 60)
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    async def insert_moves(self, game_id, moves):
        """Insert all moves of a specific game as a single document."""
        moves_document = {
            "game_id": game_id,
            "moves": moves
        }
        result = await self.async_db[MOVES_COLLECTION].insert_one(moves_document)
        return result.inserted_id
    
    async def upsert_move(self, unique_identifier, move_number, evaluation):
        # First, fetch the game ID using the unique identifier
        game_record = await self.async_db[GAMES_COLLECTION].find_one({"unique_identifier": unique_identifier})
        if not game_record:
            print(f"Game with unique identifier {unique_identifier} not found.")
            return

        game_id = game_record['_id']

        # Prepare the update for the move
        move_update = {
            "$set": {
                f"moves.{move_number - 1}.evaluation": evaluation  # Adjust for 0-based indexing
            }
        }

        # Perform the update
        await self.async_db[MOVES_COLLECTION].update_one({"game_id": game_id}, move_update)

    def insert_variation(self, variation_data):
        # Insert a new variation into the 'variations' collection
        # variation_data should be a dictionary with variation details
        self.db['variations'].insert_one(variation_data)

    async def update_wr(self, player_name):
        """Calculate the win/loss ratio for a player."""
        games_as_white = await self.async_db[GAMES_COLLECTION].count_documents({"White": player_name})
        wins_as_white = await self.async_db[GAMES_COLLECTION].count_documents({"White": player_name, "Result": "1-0"})

        games_as_black = await self.async_db[GAMES_COLLECTION].count_documents({"Black": player_name})
        wins_as_black = await self.async_db[GAMES_COLLECTION].count_documents({"Black": player_name, "Result": "0-1"})

        win_ratio_white = wins_as_white / games_as_white if games_as_white > 0 else 0
        win_ratio_black = wins_as_black / games_as_black if games_as_black > 0 else 0

        return {"white_win_ratio": win_ratio_white, "black_win_ratio": win_ratio_black}