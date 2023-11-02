enum ChessPiece {
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

use ndarray::Array1;

fn encode_board(board_state: Vec<Vec<ChessPiece>>) -> Array1<i32> {
    let mut one_hot_vector = Array1::zeros(832); // 64 squares * 13 possible states
    
    for (i, row) in board_state.iter().enumerate() {
        for (j, &cell) in row.iter().enumerate() {

            let index = i * 8 * 13 + j * 13 + cell as usize;
            
            one_hot_vector[index] = 1;
        }
    }
    
    return one_hot_vector;
}

use ndarray::{Array1, Array2, Axis};

// Function to normalize features using Z-score normalization
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
            let std = features.std_axis(axis, 0.0).ok_or("Failed to compute standard deviation")?;
            (mean, std)
        }
    };

    let mean_broadcasted = mean.insert_axis(axis);
    let std_broadcasted = std.insert_axis(axis);
    
    features = (features - &mean_broadcasted) / &std_broadcasted;

    return Ok((features, mean, std));
}

extern crate rand;
use rand::seq::SliceRandom;
use ndarray::Array2;

// Function to split data into training, validation, and test sets
fn split_data(mut data: Array2<f32>, mut labels: Array2<f32>, train_ratio: f32, val_ratio: f32) -> (Array2<f32>, Array2<f32>, Array2<f32>, Array2<f32>, Array2<f32>, Array2<f32>) {
    let mut rng = rand::thread_rng();
    
    let combined: Vec<_> = data.axis_iter(Axis(0)).zip(labels.axis_iter(Axis(0))).collect();
    let shuffled: Vec<_> = combined.choose_multiple(&mut rng, combined.len()).cloned().collect();
    
    let (shuffled_data, shuffled_labels): (Vec<_>, Vec<_>) = shuffled.into_iter().unzip();
    
    let total_rows = data.shape()[0];
    let train_end = (train_ratio * total_rows as f32).round() as usize;
    let val_end = train_end + (val_ratio * total_rows as f32).round() as usize;
    
    let train_data = Array2::from_shape_vec((train_end, data.shape()[1]), shuffled_data[0..train_end].concat()).unwrap();
    let train_labels = Array2::from_shape_vec((train_end, labels.shape()[1]), shuffled_labels[0..train_end].concat()).unwrap();
    
    let val_data = Array2::from_shape_vec((val_end - train_end, data.shape()[1]), shuffled_data[train_end..val_end].concat()).unwrap();
    let val_labels = Array2::from_shape_vec((val_end - train_end, labels.shape()[1]), shuffled_labels[train_end..val_end].concat()).unwrap();
    
    let test_data = Array2::from_shape_vec((total_rows - val_end, data.shape()[1]), shuffled_data[val_end..].concat()).unwrap();
    let test_labels = Array2::from_shape_vec((total_rows - val_end, labels.shape()[1]), shuffled_labels[val_end..].concat()).unwrap();
    
    return (train_data, train_labels, val_data, val_labels, test_data, test_labels);
}

extern crate rand;
use rand::seq::SliceRandom;
use ndarray::Array2;

// Function to create mini-batches
fn create_batches(data: Array2<f32>, labels: Array2<f32>, batch_size: usize) -> Vec<(Array2<f32>, Array2<f32>)> {
    let mut rng = rand::thread_rng();
    let mut batches: Vec<(Array2<f32>, Array2<f32>)> = Vec::new();
    
    let combined: Vec<_> = data.axis_iter(Axis(0)).zip(labels.axis_iter(Axis(0))).collect();
    let shuffled: Vec<_> = combined.choose_multiple(&mut rng, combined.len()).cloned().collect();
    
    let (shuffled_data, shuffled_labels): (Vec<_>, Vec<_>) = shuffled.into_iter().unzip();
    
    for i in (0..shuffled_data.len()).step_by(batch_size) {
        let batch_end = std::cmp::min(i + batch_size, shuffled_data.len());
        
        let batch_data = Array2::from_shape_vec((batch_end - i, data.shape()[1]), shuffled_data[i..batch_end].concat()).unwrap();
        let batch_labels = Array2::from_shape_vec((batch_end - i, labels.shape()[1]), shuffled_labels[i..batch_end].concat()).unwrap();
        
        batches.push((batch_data, batch_labels));
    }
    
    return batches;
}