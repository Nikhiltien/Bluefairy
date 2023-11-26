import io
import os
import glob
import asyncio
import chess
import chess.engine
import chess.pgn
import logging
from tqdm.asyncio import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GameAnalyzer:
    def __init__(self, _engine="stockfish"):
        self.board = chess.Board()
        self.engine_path = f"../engines/{_engine}"
        self.engine = None
        self.openings = {}

    async def init_engine(self):
        if not self.engine:
            transport, engine = await chess.engine.popen_uci(self.engine_path)
            self.engine = engine
            self.transport = transport

    async def close_engine(self):
        if self.engine:
            await self.engine.quit()

    @staticmethod
    def pgn_to_game(pgn_string):
        """
        Convert a PGN string to a python-chess Game object.
        """
        pgn_io = io.StringIO(pgn_string)
        game = chess.pgn.read_game(pgn_io)
        return game

    def load_games_from_directory(self, directory_path="../games"):
        all_games = []
        pgn_files = glob.glob(os.path.join(directory_path, '*.pgn'))
        for pgn_file_path in pgn_files:
            with open(pgn_file_path, 'r') as pgn_file:
                while True:
                    game = chess.pgn.read_game(pgn_file)
                    if game is None:
                        break
                    all_games.append(game)
        return all_games

    async def analyze_position_async(self, position_fen):
        self.board.set_fen(position_fen)
        info = await self.engine.analyse(self.board, chess.engine.Limit(depth=20))
        return info

    async def analyze_game_async(self, game):
        analysis_results = []

        board = game.board()
        total_moves = len(list(game.mainline_moves()))

        pbar = tqdm(total=total_moves, desc="Analyzing Game")

        for move in game.mainline_moves():
            board.push(move)
            info = await self.engine.analyse(board, chess.engine.Limit(depth=18))

            adjusted_score = info['score'].white() if board.turn == chess.BLACK else -info['score'].black()
            analysis_results.append({'score': adjusted_score, 'move': move})

            pbar.update(1)

        pbar.close()

        return analysis_results
    
    async def analyze_multiple_games(self, games):
        tasks = [self.analyze_game_async(game.board()) for game in games]
        return await asyncio.gather(*tasks)

    def get_analysis_results(self, analysis_results):
        formatted_results = [{'score': result['score'], 'best_move': result['move']} for result in analysis_results]
        return formatted_results

    def check_blunders(self, analysis_results):
        blunders = []
        last_score = None
        for i, result in enumerate(analysis_results):
            current_score = result['score'].white().score(mate_score=10000)
            if last_score is not None and (current_score - last_score) <= -150:
                blunders.append({'move': i, 'score_diff': current_score - last_score})
            last_score = current_score
        return blunders

    def suggest_improvements(self, analysis_results):
        improvements = []
        for blunder in self.identify_blunders(analysis_results):
            move_num = blunder['move']
            suggested_move = analysis_results[move_num]['best_move']
            if suggested_move:
                improvements.append({'move_num': move_num, 'suggested_move': suggested_move})
        return improvements

    def load_eco_book(self, file_path='../book/scid.eco'):
        with open(file_path, 'r') as eco_file:
            self.openings = self.build_opening_hashmap(eco_file.read())

    @staticmethod
    def build_opening_hashmap(eco_book):
        openings = {}
        lines = eco_book.split('\n')
        
        for line in lines:
            if line and line[0] in 'ABCDE':
                parts = line.split('"', 1)
                eco_code = parts[0].strip()
                opening_name = parts[1].split('"')[0].strip()
                moves = parts[1].split('*')[0].split('"')[1].strip().split(' ')
                moves_tuple = tuple(moves)
                openings[moves_tuple] = {'name': opening_name, 'eco': eco_code}
        
        return openings

    def find_opening(self, eco_moves):
        # Ensure eco_moves is a tuple
        if not isinstance(eco_moves, tuple):
            raise TypeError(f"Expected tuple, got {type(eco_moves)}")

        for length in range(len(eco_moves), 0, -1):
            opening_key = tuple(eco_moves[:length])
            if opening_key in self.openings:
                return self.openings[opening_key]['name'], self.openings[opening_key]['eco']
        return None, None

    def find_opening_from_game(self, game):
        """
        Identify the opening from a python-chess game object.
        """
        board = chess.Board()
        moves = [board.san(move) for move in game.mainline_moves()]
        return self.find_opening(tuple(moves))
    
    async def check_opening(self, db_manager, unique_identifiers):
        _, moves = await db_manager.get_game_by_identifier(unique_identifiers)

        moves = db_manager.convert_moves(moves)
        print(moves)

        eco_code, opening_name = self.find_opening(moves)
        print(f"Opening: {opening_name}, ECO Code: {eco_code}")

        await self.close_engine()

    async def get_best_move(self, game, move_number):
        """
        Get the best move for a given position in the game at a specific move number.
        """
        board = game.board()
        
        # Replay the game up to the specified move number
        for i, move in enumerate(game.mainline_moves()):
            if i + 1 == move_number:
                break
            board.push(move)

        # Analyze the position to get the best move
        result = await self.engine.play(board, chess.engine.Limit(time=0.1))
        best_move = result.move

        return str(best_move)
    
    def load_game_state_from_object(self, game_object):
        self.board.reset()  # Reset the board to the initial position
        for move in game_object.mainline_moves():
            try:
                self.board.push(move)
            except ValueError:
                print(f"Illegal move {move.uci()} at position {self.board.fen()}")
                break

    def current_fen(self):
        """
        Get the current FEN string of the game.
        """
        return self.board.fen()
    
    def extract_moves_from_game(self, game_object):
        """
        Extracts a list of moves in SAN format from a python-chess Game object.

        Args:
        game_object (chess.pgn.Game): The python-chess Game object.

        Returns:
        list: A list of moves in Standard Algebraic Notation (SAN).
        """
        moves_san = []
        try:
            board = game_object.board()
            for move in game_object.mainline_moves():
                moves_san.append(board.san(move))
                board.push(move)
        except Exception as e:
            print(f"An error occurred: {e}")
        return moves_san