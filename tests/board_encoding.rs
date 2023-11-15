use Bluefairy::encode::{ChessPiece, encode_board};

#[cfg(test)]
mod tests {
    use super::*;
    use ndarray::Array3;

    #[test]
    fn test_encode_empty_board() {
        let empty_board = vec![vec![ChessPiece::Empty; 8]; 8];
        let encoded = encode_board(empty_board);
        // Ensure all elements are zero
        let all_zeros = Array3::zeros((8, 8, 13));
        assert_eq!(encoded, all_zeros.into_dyn());
    }

    #[test]
    fn test_encode_single_piece() {
        let mut board = vec![vec![ChessPiece::Empty; 8]; 8];
        board[0][0] = ChessPiece::WhiteKing;
        let encoded = encode_board(board);

        // Use the correct depth index for WhiteKing as per the new encoding logic
        const WHITE_KING_INDEX: usize = 6;
        assert_eq!(encoded[[0, 0, WHITE_KING_INDEX]], 1);

        // Check all other positions are zero
        for (dim, &value) in encoded.indexed_iter() {
            let i = dim[0];
            let j = dim[1];
            let k = dim[2];

            if !(i == 0 && j == 0 && k == WHITE_KING_INDEX) {
                assert_eq!(value, 0);
            }
        }
    }

    // More tests for different board states and pieces...
}
