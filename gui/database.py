import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import asyncio
import motor
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

DATABASE_NAME = "Bluefairy"
PLAYERS_COLLECTION = "players"
GAMES_COLLECTION = "games"
MOVES_COLLECTION = "moves"

class ChessDBManager:
    def __init__(self, uri="mongodb://localhost:27017"):
        self.uri = uri
        self.client = MongoClient(uri)
        self.db = self.client[DATABASE_NAME]
        self.async_client = AsyncIOMotorClient(uri)
        self.async_db = self.async_client[DATABASE_NAME]

    @asynccontextmanager
    async def get_connection(self):
        try:
            self.async_client = AsyncIOMotorClient(self.uri)
            self.async_db = self.async_client[DATABASE_NAME]
            yield self.async_db
        finally:
            self.async_client.close()

    def close_connection(self):
        self.client.close()
        if self.async_client:
            self.async_client.close()

    @staticmethod
    def generate_game_hash(moves):
        """Generate a hash from the list of moves."""
        move_string = ' '.join([f"{move['ply']} {move['move']}" for move in moves])
        return hashlib.sha256(move_string.encode()).hexdigest()
    
    async def insert_games_batch(self, games, batch_size=100):
        """Insert games in batches."""
        for i in range(0, len(games), batch_size):
            batch = games[i:i + batch_size]
            await self.async_db[GAMES_COLLECTION].insert_many(batch)
    
    async def upsert_player_profile(self, player_name):
        """Create a player profile if it doesn't already exist."""
        result = await self.async_db[PLAYERS_COLLECTION].update_one(
            {"name": player_name},
            {"$setOnInsert": {"name": player_name}},  # Sets the 'name' field only on insert
            upsert=True  # Creates a new document if one doesn't exist
        )
        return result.upserted_id or result.modified_count

    async def get_latest_game_elo(self, player_name):
        """Fetch the most recent game for a player and return the Elo rating."""
        # Assuming the games collection has a date field to sort by
        latest_game = await self.async_db[GAMES_COLLECTION].find_one(
            {"$or": [{"White": player_name}, {"Black": player_name}]},
            sort=[("Date", pymongo.DESCENDING)]
        )

        if latest_game is None:
            return None  # No games found for the player

        player_elo = latest_game['WhiteElo'] if latest_game['White'] == player_name else latest_game['BlackElo']
        return player_elo
    
    async def get_player_data(self, query):
        try:
            player_data = await self.async_db[PLAYERS_COLLECTION].find_one(query)
            return player_data
        except Exception as e:
            logging.error(f"Error fetching player data: {e}")

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

    async def insert_game(self, game_metadata, moves, opening_name=None):
        """Insert a new chess game into the games collection if it doesn't exist."""
        game_hash = self.generate_game_hash(moves)
        unique_identifier = f"{game_metadata['Event']}-{game_metadata['Date']}-{game_metadata['White']}-{game_metadata['Black']}-{game_hash}"
        existing_game, _ = await self.get_game_by_identifier(unique_identifier)
        if existing_game:
            print(f"GameID {existing_game['_id']} already exists.")
            return unique_identifier

        game_metadata['unique_identifier'] = unique_identifier
        game_metadata['opening_name'] = opening_name

        result = await self.async_db[GAMES_COLLECTION].insert_one(game_metadata)
        game_id = result.inserted_id
        await self.insert_moves(game_id, moves)
        return unique_identifier
    
    async def update_game_with_opening(self, unique_identifier, opening_name):
        await self.async_db[GAMES_COLLECTION].update_one(
            {"unique_identifier": unique_identifier}, 
            {"$set": {"Opening": opening_name}}
        )
    
    async def mark_reviewed(self, unique_identifier):
        await self.async_db[GAMES_COLLECTION].update_one(
            {"unique_identifier": unique_identifier},
            {"$set": {"review": True}}
        )
    
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
        headers = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]

        # Add headers with appropriate fallbacks
        for header in headers:
            value = game_metadata.get(header, None)
            if value is None or value.strip() == "":
                value = "?"  # Use '?' for missing or empty fields
            pgn_parts.append(f'[{header} "{value}"]')

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
        if time_in_seconds is None:
            return "n/a"

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
    
    async def update_all_moves(self, unique_identifier, evaluations, blunders):
        """Update moves and evaluations for a specific game, adding the best move for blunders."""
        game_record = await self.async_db[GAMES_COLLECTION].find_one({"unique_identifier": unique_identifier})
        if not game_record:
            print(f"Game with unique identifier {unique_identifier} not found.")
            return

        game_id = game_record['_id']
        move_updates = {}

        # Update evaluations and add best moves for blunders
        for i, eval in enumerate(evaluations):
            move_updates[f"moves.{i}.evaluation"] = eval
            ply_number = str(i + 1)  # Convert index to ply number
            if ply_number in blunders:
                move_updates[f"moves.{i}.best_move"] = blunders[ply_number]

        await self.async_db[MOVES_COLLECTION].update_one(
            {"game_id": game_id},
            {"$set": move_updates}
        )

    def insert_variation(self, variation_data):
        # Insert a new variation into the 'variations' collection
        # variation_data should be a dictionary with variation details
        self.db['variations'].insert_one(variation_data)

    async def update_wr_and_openings(self, player_name):
        """Calculate the win/loss ratio for a player and update their profile with this info, top 3 openings, and latest Elo."""
        # Count games played as White and wins as White
        games_as_white = await self.async_db[GAMES_COLLECTION].count_documents({"White": player_name})
        wins_as_white = await self.async_db[GAMES_COLLECTION].count_documents({"White": player_name, "Result": "1-0"})

        # Count games played as Black and wins as Black
        games_as_black = await self.async_db[GAMES_COLLECTION].count_documents({"Black": player_name})
        wins_as_black = await self.async_db[GAMES_COLLECTION].count_documents({"Black": player_name, "Result": "0-1"})

        # Calculate win ratios for both colors
        win_ratio_white = wins_as_white / games_as_white if games_as_white > 0 else 0
        win_ratio_black = wins_as_black / games_as_black if games_as_black > 0 else 0

        # Aggregate top 3 openings
        pipeline = [
            {"$match": {"$or": [{"White": player_name}, {"Black": player_name}]}},
            {"$group": {"_id": "$Opening", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 3}
        ]
        top_openings = await self.async_db[GAMES_COLLECTION].aggregate(pipeline).to_list(length=None)
        top_openings = [opening["_id"] for opening in top_openings if opening["_id"] is not None]

        # Fetch the Elo rating from the most recent game
        player_elo = await self.get_latest_game_elo(player_name)
        if player_elo is None:
            logging.warning(f"No recent games found for {player_name}. Elo rating not updated.")

        # Prepare update fields
        update_fields = {
            "white_win_ratio": win_ratio_white, 
            "black_win_ratio": win_ratio_black, 
            "top_openings": top_openings
        }

        # Update Elo if available
        if player_elo is not None:
            update_fields["elo"] = player_elo

        # Update player profile with all calculated and fetched data
        await self.async_db[PLAYERS_COLLECTION].update_one(
            {"name": player_name},
            {"$set": update_fields},
            upsert=True
        )

    async def store_best_moves(self, unique_identifier, best_move):
        """Store the best move for blunders in a specific game."""
        await self.async_db[GAMES_COLLECTION].update_one(
            {"unique_identifier": unique_identifier},
            {"$set": {"best_move": best_move}}
        )