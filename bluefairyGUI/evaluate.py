import io
import os
import glob
import chess
import chess.engine

class GameAnalyzer:
    def __init__(self):
        # Initialize the chess board
        self.board = chess.Board()
        
        # Path to the Stockfish engine
        self.engine_path = "../engines/stockfish"
        
        # Set up the Stockfish engine
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)

    def load_game(self, game_data, format="PGN"):
        all_games = []

        # Check if game_data is a directory path
        if os.path.isdir(game_data):
            pgn_files = glob.glob(os.path.join(game_data, '*.pgn'))
            for pgn_file_path in pgn_files:
                with open(pgn_file_path, 'r') as pgn_file:
                    while True:
                        game = chess.pgn.read_game(pgn_file)
                        if game is None:
                            break
                        all_games.append(game)
        else:
            # Handling a PGN/FEN string
            try:
                if format.upper() == "PGN":
                    pgn_io = io.StringIO(game_data)
                    game = chess.pgn.read_game(pgn_io)
                    self.board = game.board()
                    all_games.append(game)
                elif format.upper() == "FEN":
                    self.board.set_fen(game_data)
                    all_games.append(self.board)
            except Exception as e:
                print(f"Error loading game: {e}")
                return False

        return all_games

    def analyze_game(self):
        analysis_results = []

        # Reset the board to the start of the game
        self.board.reset()

        # Iterate over all moves in the game
        for move in self.board.legal_moves:
            # Make the move on the board
            self.board.push(move)

            # Analyze the current board position
            info = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))
            analysis_results.append(info)

            # Undo the move to analyze the next one
            self.board.pop()

        return analysis_results

    def analyze_position(self, position_fen):
        # Set the board to the specified position
        self.board.set_fen(position_fen)

        # Analyze the position
        info = self.engine.analyse(self.board, chess.engine.Limit(depth=20))

        return info

    def get_analysis_results(self, analysis_results):
        formatted_results = []
        for result in analysis_results:
            # Format each analysis result, e.g., score, best move
            formatted_result = {
                'score': result['score'],
                'best_move': result['pv'][0] if 'pv' in result else None
            }
            formatted_results.append(formatted_result)
        return formatted_results

    def identify_blunders(self, analysis_results):
        blunders = []
        for i, result in enumerate(analysis_results):
            # A blunder can be identified by a significant negative change in score
            if i > 0:
                score_diff = result['score'].relative.score(mate_score=10000) - analysis_results[i - 1]['score'].relative.score(mate_score=10000)
                if score_diff < -100:  # Threshold for blunder, can be adjusted
                    blunders.append({'move': i, 'score_diff': score_diff})
        return blunders

    def suggest_improvements(self, analysis_results):
        improvements = []
        for blunder in self.identify_blunders(analysis_results):
            move_num = blunder['move']
            suggested_move = analysis_results[move_num]['best_move']
            if suggested_move:
                improvements.append({'move_num': move_num, 'suggested_move': suggested_move})
        return improvements

    # Additional helper methods as needed
