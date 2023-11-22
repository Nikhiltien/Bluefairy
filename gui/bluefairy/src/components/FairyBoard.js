import React, { useState, useEffect, useMemo } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import { Typography, Alert } from '@mui/material';

const FairyBoard = () => {
    const game = useMemo(() => new Chess(), []);
    const [gamePosition, setGamePosition] = useState(game.fen());
    const [boardOrientation, setBoardOrientation] = useState('white');
    const [statusMessage, setStatusMessage] = useState('');
    const [isGameOver, setIsGameOver] = useState(false);

    const checkGameOver = () => {
        if (game.game_over()) {
            if (game.in_checkmate()) {
                const winner = game.turn() === 'b' ? 'White' : 'Black';
                setStatusMessage(`Checkmate! ${winner} wins.`);
            } else if (game.in_draw()) {
                setStatusMessage('Draw!');
            }
            return true;
        }
        return false;
    };

    useEffect(() => {
        checkGameOver();
    }, [gamePosition]);

    const onDrop = (sourceSquare, targetSquare, piece) => {
        try {
            const move = game.move({
                from: sourceSquare,
                to: targetSquare,
                // Handle promotion. You may need a more complex logic here for user to choose the piece
                promotion: piece === 'P' && targetSquare[1] === '8' ? 'q' :
                           piece === 'p' && targetSquare[1] === '1' ? 'q' : undefined
            });

            if (move === null) {
                setStatusMessage('Illegal move');
                return false;
            }

            setGamePosition(game.fen());
            setStatusMessage('');
            return true;
        } catch (error) {
            console.error("Error during move:", error);
            setStatusMessage('An unexpected error occurred');
            return false;
        }
    };

    const flipBoard = () => {
        setBoardOrientation(boardOrientation === 'white' ? 'black' : 'white');
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
            <Button onClick={flipBoard} style={{ marginTop: '10px' }}>
                Flip Board
            </Button>
        </div>
    );
};

export default FairyBoard;