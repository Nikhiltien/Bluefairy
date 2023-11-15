import pymongo
import asyncio
import motor.motor_asyncio

class ChessDatabase:
    def __init__(self, db_url, db_name):
        # Initialize MongoDB client
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client[db_name]

    def insert_game(self, game_data):
        # Insert a new chess game into the 'games' collection
        # game_data should be a dictionary with game details
        self.db['games'].insert_one(game_data)

    def get_game_by_player(self, player_name):
        # Retrieve chess games by player name from the 'games' collection
        return list(self.db['games'].find({'players': player_name}))

    def insert_variation(self, variation_data):
        # Insert a new variation into the 'variations' collection
        # variation_data should be a dictionary with variation details
        self.db['variations'].insert_one(variation_data)

    # Add methods for moves, player information, and other operations as needed

    def close_connection(self):
        # Close the MongoDB client connection when done
        self.client.close()

async def main():
    # Connect to MongoDB asynchronously
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

    # Access a database and collection
    db = client['mydatabase']
    collection = db['mycollection']

    # Insert a document asynchronously
    document = {'key': 'value'}
    await collection.insert_one(document)

    # Find documents asynchronously
    async for doc in collection.find({'key': 'value'}):
        print(doc)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# # Example usage:
# if __name__ == "__main__":
#     db_url = "mongodb://localhost:27017/"  # MongoDB server URL
#     db_name = "chessdb"  # Database name

#     chess_db = ChessDatabase(db_url, db_name)

#     # Example: Insert a chess game
#     game_data = {
#         'players': ['Player1', 'Player2'],
#         'result': '1-0',
#         'moves': ['e4', 'e5', 'Nf3', 'Nc6']
#     }
#     chess_db.insert_game(game_data)

#     # Example: Retrieve games by player name
#     player_name = 'Player1'
#     games = chess_db.get_game_by_player(player_name)
#     print(f"Games played by {player_name}:")
#     for game in games:
#         print(game)

#     # Close the MongoDB connection when done
#     chess_db.close_connection()
