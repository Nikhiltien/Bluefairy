import React, { useState, useEffect, useMemo } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import { Typography, Alert, Button } from '@mui/material';

const FairyBoard = ({ initialFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', boardOrientation = 'white', onFlipBoard }) => {
    const [game, setGame] = useState(() => new Chess(initialFen === 'start' ? undefined : initialFen));
    const [gamePosition, setGamePosition] = useState(game.fen());
    const [statusMessage, setStatusMessage] = useState('');
    const [moveHistory, setMoveHistory] = useState([]);

    useEffect(() => {
        // Check for game over scenarios
        // if (game.game_over()) {
        //     if (game.in_checkmate()) {
        //         const winner = game.turn() === 'b' ? 'White' : 'Black';
        //         setStatusMessage(`Checkmate! ${winner} wins.`);
        //     } else if (game.in_draw()) {
        //         setStatusMessage('Draw!');
        //     }
        //     return true;
        // }
        // return false;
    }, [gamePosition]);

    const onDrop = (sourceSquare, targetSquare, piece) => {
        // if (game.game_over()) {
        //     setStatusMessage('Game is over. Start a new game to continue.');
        //     return false;
        // }

        try {
            const move = game.move({
                from: sourceSquare,
                to: targetSquare,
                promotion: piece === 'P' && targetSquare[1] === '8' ? 'q' :
                           piece === 'p' && targetSquare[1] === '1' ? 'q' : undefined
            });

            if (move === null) {
                setStatusMessage('Illegal move');
                return false;
            }

            setGamePosition(game.fen());
            setMoveHistory(game.history({ verbose: true }));
            setStatusMessage('');
            return true;
        } catch (error) {
            console.error("Error during move:", error);
            // setStatusMessage('An unexpected error occurred');
            return false;
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Chessboard 
                boardWidth={550} 
                position={gamePosition} 
                onPieceDrop={onDrop}
                orientation={boardOrientation}
            />
            {statusMessage && (
                <Alert severity="info" style={{ marginTop: '10px' }}>
                    {statusMessage}
                </Alert>
            )}
        </div>
    );
};

export default FairyBoard;