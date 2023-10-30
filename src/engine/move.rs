use std::collections::HashMap;

pub struct MoveGenerator {
    board_evaluator: BoardEvaluator,
}

impl MoveGenerator {
    pub fn new(board_evaluator: BoardEvaluator) -> Self {
        Self { board_evaluator }
    }

    pub fn generate_move(&self, board_state: &BoardState, model: &Model) -> chess::ChessMove {
        let move_scores = self.get_scores_for_moves(board_state, model);
        // Logic to choose the best move based on scores
        // Placeholder code here
        chess::ChessMove::default()
    }

    fn get_scores_for_moves(&self, board_state: &BoardState, model: &Model) -> HashMap<chess::ChessMove, f64> {
        let possible_moves = board_state.get_possible_moves();
        let mut move_scores = HashMap::new();

        for mv in possible_moves {
            let new_board_state = board_state.clone().apply_move(mv).unwrap(); // Placeholder, need to add error handling
            let score = self.board_evaluator.evaluate_board(&new_board_state, model);
            move_scores.insert(mv, score);
        }

        move_scores
    }
}
