import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []

    def make_move(self, move):
        try:
            move = chess.Move.from_uci(move)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move.uci())
                return True
            else:
                return False
        except ValueError:
            return False

    def undo_move(self):
        if self.move_history:
            self.board.pop()
            self.move_history.pop()
            return True
        return False

    def game_state(self):
        # Returns the current state of the game (checkmate, stalemate, etc.)
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_insufficient_material():
            return "Draw: Insufficient Material"
        else:
            return "Ongoing"

    def current_board(self):
        # Returns the board state in a format suitable for the frontend
        return self.board.fen()
