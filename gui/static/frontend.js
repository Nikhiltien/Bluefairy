import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { Chessboard, FEN, INPUT_EVENT_TYPE } from '/static/cm/src/Chessboard.js';
import { Markers } from "/static/cm/src/extensions/markers/Markers.js";
import { Chess } from '/static/chess.js';

function ChessApp() {
    const [game, setGame] = useState(new Chess());
    const [board, setBoard] = useState(null);
    const [fen, setFen] = useState(FEN.start); // FEN string state
    const [history, setHistory] = useState([]); // Move history state

    // WebSocket setup
    useEffect(() => {
        const socket = new WebSocket("ws://localhost:5000/ws");

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

        return () => socket.close(); // Clean up the socket when the component unmounts
    }, []);

    // Function to send moves through the WebSocket
    const sendMove = (move) => {
        // Implementation of sending move
    };

    // Function to update evaluation (assuming it's part of your app logic)
    async function updateEvaluation(boardPosition) {
        // Call to backend API to get evaluation
        // Update evaluation bar based on response
    }

    // Input Handler for chess moves
    const inputHandler = (event) => {
      if (event.type === INPUT_EVENT_TYPE.moveInputStarted) {
          return game.turn() === event.piece.charAt(0);
      }
      if (event.type === INPUT_EVENT_TYPE.validateMoveInput) {
          let move = game.move({ from: event.squareFrom, to: event.squareTo });
          if (move) {
              setFen(game.fen());
              setHistory(game.history({ verbose: true }));
              // Additional UI updates based on the move
          } else {
              console.warn("invalid move", move);
          }
          return move !== null;
      }
      return true;
    };

    // Initialize the chessboard
    useEffect(() => {
      const newBoard = new Chessboard(document.getElementById('chessboard'), {
          position: fen, 
          assetsUrl: "static/cm/assets/",
          assetsCache: false,
          style: {
              cssClass: "chess-club",
              showCoordinates: true,
              borderType: 1,
              pieces: {
                  file: "pieces/staunty.svg",
              },
              animationDuration: 300
          },
          extensions: [{class: Markers}]
      });

      setBoard(newBoard);

      newBoard.enableMoveInput(inputHandler);

      return () => newBoard.destroy(); // Clean up the board when the component unmounts
  }, [fen]); // fen added to dependency array

  return (
    <div>
        {/* Components for player info, game navigation, etc. */}
        <div id="chessboard" className="chessboard" style={{ width: '100%' }}></div>
    </div>
);
}

export default ChessApp;

ReactDOM.render(<ChessApp />, document.getElementById('root'));