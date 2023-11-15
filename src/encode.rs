#![allow(non_snake_case)]

use ndarray::{Array1, Array2, Array3, ArrayD, Axis};
use rand::seq::SliceRandom;
// use rand::thread_rng;

#[derive(Clone, Copy)]
pub enum ChessPiece {
    Empty,
    WhitePawn,
    WhiteRook,
    WhiteKnight,
    WhiteBishop,
    WhiteQueen,
    WhiteKing,
    BlackPawn,
    BlackRook,
    BlackKnight,
    BlackBishop,
    BlackQueen,
    BlackKing,
}    

pub fn encode_board(board_state: Vec<Vec<ChessPiece>>) -> ArrayD<i32> {
    let mut encoded_board = Array3::zeros((8, 8, 13));

    for (i, row) in board_state.iter().enumerate() {
        for (j, piece) in row.iter().enumerate() {
            if let ChessPiece::Empty = piece {
                continue; // Skip empty pieces
            }

            let depth_index = match piece {
                ChessPiece::Empty => unreachable!(), // We already checked for Empty
                ChessPiece::WhitePawn => 1,
                ChessPiece::WhiteRook => 2,
                ChessPiece::WhiteKnight => 3,
                ChessPiece::WhiteBishop => 4,
                ChessPiece::WhiteQueen => 5,
                ChessPiece::WhiteKing => 6,
                ChessPiece::BlackPawn => 7,
                ChessPiece::BlackRook => 8,
                ChessPiece::BlackKnight => 9,
                ChessPiece::BlackBishop => 10,
                ChessPiece::BlackQueen => 11,
                ChessPiece::BlackKing => 12,
            };
            encoded_board[[i, j, depth_index]] = 1;
        }
    }

    let encoded_board_dynamic = encoded_board.into_dyn();

    encoded_board_dynamic
}

#[allow(dead_code)]
fn normalize(
    mut features: Array2<f32>, 
    axis: Axis,
    mean: Option<Array1<f32>>,
    std: Option<Array1<f32>>) 
    -> Result<(Array2<f32>, Array1<f32>, Array1<f32>), &'static str> {
    
    let (mean, std) = match (mean, std) {
        (Some(mean), Some(std)) => (mean, std),
        _ => {
            let mean = features.mean_axis(axis).ok_or("Failed to compute mean")?;
            // Use `std_axis` directly without `ok_or`
            let std = features.std_axis(axis, 0.0);

            // Optional: Add custom checks here if needed
            // Example: Check if `std` contains any non-zero values
            if std.iter().all(|&x| x == 0.0) {
                return Err("Standard deviation computation resulted in zeros");
            }

            (mean, std)
        }
    };

    let mean_broadcasted = mean.clone().insert_axis(axis);
    let std_broadcasted = std.clone().insert_axis(axis); // Clone `std` before moving
    
    features = (features - &mean_broadcasted) / &std_broadcasted;

    Ok((features, mean, std)) // Both `mean` and `std` are still valid here
}

#[allow(dead_code)]
fn split_data(data: Array2<f32>, labels: Array2<f32>, train_ratio: f32, val_ratio: f32) -> (Array2<f32>, Array2<f32>, Array2<f32>, Array2<f32>, Array2<f32>, Array2<f32>) {
    let mut rng = rand::thread_rng();
    
    let combined: Vec<_> = data.axis_iter(Axis(0)).zip(labels.axis_iter(Axis(0))).collect();
    let shuffled: Vec<_> = combined.choose_multiple(&mut rng, combined.len()).cloned().collect();
    
    let (shuffled_data, shuffled_labels): (Vec<_>, Vec<_>) = shuffled.into_iter().unzip();
    
    let total_rows = data.shape()[0];
    let train_end = (train_ratio * total_rows as f32).round() as usize;
    let val_end = train_end + (val_ratio * total_rows as f32).round() as usize;

    let train_data_vec: Vec<f32> = shuffled_data[0..train_end].iter().flat_map(|a| a.iter().cloned()).collect();
    let train_labels_vec: Vec<f32> = shuffled_labels[0..train_end].iter().flat_map(|a| a.iter().cloned()).collect();
    let train_data = Array2::from_shape_vec((train_end, data.shape()[1]), train_data_vec).unwrap();
    let train_labels = Array2::from_shape_vec((train_end, labels.shape()[1]), train_labels_vec).unwrap();

    let val_data_vec: Vec<f32> = shuffled_data[train_end..val_end].iter().flat_map(|a| a.iter().cloned()).collect();
    let val_labels_vec: Vec<f32> = shuffled_labels[train_end..val_end].iter().flat_map(|a| a.iter().cloned()).collect();
    let val_data = Array2::from_shape_vec((val_end - train_end, data.shape()[1]), val_data_vec).unwrap();
    let val_labels = Array2::from_shape_vec((val_end - train_end, labels.shape()[1]), val_labels_vec).unwrap();

    let test_data_vec: Vec<f32> = shuffled_data[val_end..].iter().flat_map(|a| a.iter().cloned()).collect();
    let test_labels_vec: Vec<f32> = shuffled_labels[val_end..].iter().flat_map(|a| a.iter().cloned()).collect();
    let test_data = Array2::from_shape_vec((total_rows - val_end, data.shape()[1]), test_data_vec).unwrap();
    let test_labels = Array2::from_shape_vec((total_rows - val_end, labels.shape()[1]), test_labels_vec).unwrap();
    
    (train_data, train_labels, val_data, val_labels, test_data, test_labels)
}

#[allow(dead_code)]
fn create_batches(data: Array2<f32>, labels: Array2<f32>, batch_size: usize) -> Vec<(Array2<f32>, Array2<f32>)> {
    let mut rng = rand::thread_rng();
    let mut batches: Vec<(Array2<f32>, Array2<f32>)> = Vec::new();
    
    let combined: Vec<_> = data.axis_iter(Axis(0)).zip(labels.axis_iter(Axis(0))).collect();
    let shuffled: Vec<_> = combined.choose_multiple(&mut rng, combined.len()).cloned().collect();
    
    let (shuffled_data, shuffled_labels): (Vec<_>, Vec<_>) = shuffled.into_iter().unzip();
    
    for i in (0..shuffled_data.len()).step_by(batch_size) {
        let batch_end = std::cmp::min(i + batch_size, shuffled_data.len());

        let batch_data_vec: Vec<f32> = shuffled_data[i..batch_end].iter().flat_map(|a| a.iter().cloned()).collect();
        let batch_labels_vec: Vec<f32> = shuffled_labels[i..batch_end].iter().flat_map(|a| a.iter().cloned()).collect();
        let batch_data = Array2::from_shape_vec((batch_end - i, data.shape()[1]), batch_data_vec).unwrap();
        let batch_labels = Array2::from_shape_vec((batch_end - i, labels.shape()[1]), batch_labels_vec).unwrap();
        
        batches.push((batch_data, batch_labels));
    }
    
    batches
}