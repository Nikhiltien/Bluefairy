import React, { useState, useEffect, useMemo } from 'react';
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

            const newFen = game.fen();
            setCurrentGamePosition(newFen);
            setExternalGamePosition(newFen); // Update the parent component
            updateMoveHistory(newFen); // Update the parent component
            // if (updateMoveHistory) {
            //     updateMoveHistory(game.history({ verbose: true }));
            // }

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
