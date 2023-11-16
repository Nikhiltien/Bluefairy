import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import asyncio
import motor
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

    def create_player_profile(self, player_data):
        """Insert a new player profile into the database."""
        result = self.db[PLAYERS_COLLECTION].insert_one(player_data)
        return result.inserted_id
    
    def update_player_profile(self, player_id, update_data):
        """Update an existing player's profile."""
        result = self.db[PLAYERS_COLLECTION].update_one({"player_id": player_id}, {"$set": update_data})
        return result.modified_count
    
    def get_player_data(self, query):
        """Fetch player data based on a query."""
        player_data = self.db[PLAYERS_COLLECTION].find_one(query)
        return player_data
    
    def delete_player_profile(self, player_id):
        """Delete a player profile from the database."""
        result = self.db[PLAYERS_COLLECTION].delete_one({"player_id": player_id})
        return result.deleted_count

    async def insert_game(self, game_data):
        """Insert a new chess game into the games collection."""
        result = await self.async_db[GAMES_COLLECTION].insert_one(game_data)
        return result.inserted_id

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

    async def insert_moves(self, game_id, moves):
        """Insert all moves of a specific game as a single document."""
        moves_document = {
            "game_id": game_id,
            "moves": moves
        }
        result = await self.async_db[MOVES_COLLECTION].insert_one(moves_document)
        return result.inserted_id

    def insert_variation(self, variation_data):
        # Insert a new variation into the 'variations' collection
        # variation_data should be a dictionary with variation details
        self.db['variations'].insert_one(variation_data)

    # Add methods for moves, player information, and other operations as needed

    def close_connection(self):
        self.client.close()