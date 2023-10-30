extern crate chess;

pub fn convert_move_to_string(chess_move: chess::ChessMove) -> String {
    let from = chess_move.get_source().to_string();
    let to = chess_move.get_dest().to_string();
    let promotion = chess_move.get_promotion().map_or(String::new(), |p| p.to_string());
    
    format!("{}{}{}", from, to, promotion)
}

pub fn convert_string_to_move(move_str: &str) -> Result<chess::ChessMove, String> {
    if move_str.len() < 4 {
        return Err("Invalid move string length".to_string());
    }

    let from = &move_str[0..2];
    let to = &move_str[2..4];
    let promotion = if move_str.len() > 4 { Some(&move_str[4..]) } else { None };

    let from_square = chess::Square::from_str(from).map_err(|_| "Invalid source square".to_string())?;
    let to_square = chess::Square::from_str(to).map_err(|_| "Invalid destination square".to_string())?;
    let promotion_piece = promotion.map(|p| chess::Piece::from_str(p).map_err(|_| "Invalid promotion piece".to_string()));

    if let Some(Err(err)) = promotion_piece {
        return Err(err);
    }

    Ok(chess::ChessMove::new(from_square, to_square, promotion_piece.ok().flatten()))
}
