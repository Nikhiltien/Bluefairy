import { Chessboard, FEN, INPUT_EVENT_TYPE, COLOR } from '/static/cm/src/Chessboard.js';
import { Markers } from "/static/cm/src/extensions/markers/Markers.js";
import { Chess } from '/static/chess.js';

let socket = new WebSocket("ws://localhost:5000/ws");

socket.onopen = function(e) {
  // Handle WebSocket connection opened
};

socket.onmessage = function(event) {
  let gameUpdate = JSON.parse(event.data);
  // Update the board based on the gameUpdate
};

socket.onclose = function(event) {
  if (event.wasClean) {
    // Handle WebSocket connection closed
  } else {
    // Handle connection error
  }
};

socket.onerror = function(error) {
  // Handle WebSocket error
};

function sendMove(move) {
  socket.send(JSON.stringify({ move }));
}

document.addEventListener("DOMContentLoaded", function() {
  const board = new Chessboard(document.getElementById('chessboard'), {
    position: FEN.start,
    assetsUrl: "static/cm/assets/",
    assetsCache: false,
    style: {
        cssClass: "green",
        showCoordinates: true,
        borderType: 1,
        pieces: {
            file: "pieces/standard.svg",
            tileSize: 40
            },
        animationDuration: 300
        },
    extensions: [{class: Markers}]
  });

  const game = new Chess();

  // Enable user interaction with the chessboard
  board.enableMoveInput((event) => {
    if (event.type === INPUT_EVENT_TYPE.moveInputStarted) {
        // Check if the piece that's being moved belongs to the player whose turn it is
        return game.turn() === event.piece.charAt(0);
    }
    if (event.type === INPUT_EVENT_TYPE.validateMoveInput) {
        // Validate and make the move
        let move = game.move({ from: event.squareFrom, to: event.squareTo });
        return move !== null; // Return true if the move is valid
    }
    // Handle other event types as needed
  });

  // Additional logic for handling game updates and interaction with the backend
});

async function updateEvaluation(boardPosition) {
  // Call to backend API to get evaluation
  // Update evaluation bar based on response
}
