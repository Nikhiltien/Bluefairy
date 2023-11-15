from evaluate import GameAnalyzer
import chess.pgn

def main():
    analyzer = GameAnalyzer()

    # Sample PGN (part of a famous game)
    pgn_sample = """
    [Event "F/S Return Match"]
    [Site "Belgrade, Serbia JUG"]
    [Date "1992.11.04"]
    [Round "29"]
    [White "Fischer, Robert J."]
    [Black "Spassky, Boris V."]
    [Result "1/2-1/2"]

    1. e4 e5 2. Nf3 Nc6 3. Bb5 a6
    """

    if analyzer.load_game(pgn_sample):
        print("Game loaded successfully!")

        # Test analyze_game method
        game_analysis = analyzer.analyze_game()
        print("Game Analysis:")
        print(game_analysis)

        # Test analyze_position method with a sample position
        position_fen = "r1bqkbnr/1ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 2 4"
        position_analysis = analyzer.analyze_position(position_fen)
        print("Position Analysis:")
        print(position_analysis)
    else:
        print("Failed to load the game.")

if __name__ == "__main__":
    main()
