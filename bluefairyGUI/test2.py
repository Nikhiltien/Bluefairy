from database import ChessDBManager
import asyncio

async def main():
    db_manager = ChessDBManager(uri="mongodb+srv://Cluster07315:Z2tCYVB3UnF7@cluster07315.49ooxiq.mongodb.net/?retryWrites=true&w=majority")
    unique_identifier = "Live Chess-2023.11.10-niki0x-Tjommyen-cb8b52c573de56bf6c7a605d206f8445e0bfd54af42cca1ae5d2b53fb7611cfb"
    pgn_string = await db_manager.fetch_game_pgn(unique_identifier)
    print(pgn_string)

asyncio.run(main())