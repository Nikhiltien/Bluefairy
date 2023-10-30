extern crate chess;

pub struct BoardState {
    board: chess::Board,
    move_gen: chess::MoveGen,
}

impl BoardState {
    pub fn initialize_board() -> Self {
        let board = chess::Board::default();
        let move_gen = chess::MoveGen::new_legal(&board);
        Self { board, move_gen }
    }

    pub fn apply_move(&mut self, mv: chess::ChessMove) -> chess::Result<()> {
        self.board = self.board.make_move_new(mv);
        self.move_gen = chess::MoveGen::new_legal(&self.board);
        Ok(())
    }

    pub fn get_possible_moves(&self) -> Vec<chess::ChessMove> {
        self.move_gen.clone().collect()
    }

    pub fn game_status(&self) -> chess::BoardStatus {
        self.board.status()
    }
    
    pub fn get_board_hash(&self) -> u64 {
        self.board.get_hash()
    }
    
    pub fn is_move_legal(&self, mv: chess::ChessMove) -> bool {
        chess::MoveGen::legal_quick(&self.board, mv)
    }
}