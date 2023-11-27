import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
import { Alert } from '@mui/material';

const FairyBoard = ({ boardOrientation, gamePosition, setExternalGamePosition, updateMoveHistory }) => {
    const game = useMemo(() => new Chess(), []);
    const [currentGamePosition, setCurrentGamePosition] = useState(game.fen());
    const [statusMessage, setStatusMessage] = useState('');

    useEffect(() => {
        if (gamePosition) {
            game.load(gamePosition);
            setCurrentGamePosition(game.fen());
        }
    }, [game, gamePosition]);    

    const onDrop = (sourceSquare, targetSquare, piece) => {
        console.log("Attempting move:", sourceSquare, targetSquare, piece);
        console.log("Current game state (FEN):", game.fen());
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

            const newFen = game.fen();
            setCurrentGamePosition(newFen);
            setExternalGamePosition(newFen); // Update the parent component
        
            if (updateMoveHistory && move.san) {
                updateMoveHistory(move.san); // Update the parent component with SAN notation
            }
        
            setStatusMessage('');
            return true;
        } catch (error) {
            console.error("Error during move:", error);
            return false;
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Chessboard 
                boardWidth={550} 
                position={currentGamePosition}
                onPieceDrop={onDrop}
                boardOrientation={boardOrientation}
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