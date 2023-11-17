import io
import os
import glob
import asyncio
import chess
import chess.engine
import chess.pgn
import logging

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
        for move in game.mainline_moves():
            board.push(move)
            info = await self.engine.analyse(board, chess.engine.Limit(depth=20))

            # Adjust score to be from White's perspective
            if board.turn == chess.BLACK:  # After White's move
                adjusted_score = info['score'].white()
            else:  # After Black's move, invert the score
                adjusted_score = -info['score'].black()

            analysis_results.append({'score': adjusted_score, 'move': move})
            # No need to pop the move, as we're iterating through mainline_moves

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

    def identify_opening_from_pgn(self, pgn_string):
        game = chess.pgn.read_game(io.StringIO(pgn_string))
        moves = [self.board.san(move) for move in game.mainline_moves()]
        return self.find_opening(moves)