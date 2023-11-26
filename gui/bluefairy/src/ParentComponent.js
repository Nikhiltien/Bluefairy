import React, { useState, useCallback } from 'react';
import FairyBoard from './components/FairyBoard';
import SideMenu from './components/SideMenu';
import { Chess } from 'chess.js';

const ParentComponent = () => {
    const initialFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
    const [boardOrientation, setBoardOrientation] = useState('white');
    const [gamePosition, setGamePosition] = useState(initialFen);
    const [currentStep, setCurrentStep] = useState(0);
    const [moveHistory, setMoveHistory] = useState([])

    // Logic to start a new game in FairyBoard
    const startNewGame = () => {
        setMoveHistory([]); // Reset move history
        setCurrentStep(0);
        setGamePosition(initialFen);
    };    

    // Logic to navigate through game history
    const navigateHistory = (step) => {
        const newStep = currentStep + step;
        if (newStep >= 0 && newStep <= moveHistory.length) {
            const game = new Chess();
            // Iterate through the move history up to the new step
            for (let i = 0; i < newStep; i++) {
                game.move(moveHistory[i]);
            }
            setCurrentStep(newStep);
            setGamePosition(game.fen());
        }
    };
    
    const [currentPgn, setCurrentPgn] = useState('');

    const [pgnInput, setPgnInput] = useState('');

    const updateMoveHistory = useCallback((sanMove) => {
        setMoveHistory(prevHistory => {
            const newHistory = [...prevHistory, sanMove];
            const game = new Chess();
            newHistory.forEach(move => game.move(move));
            setCurrentPgn(game.pgn());
            return newHistory;
        });
        setCurrentStep(prevStep => prevStep + 1);
    }, []);

    const loadGameFromPgn = async (pgn) => {
        const response = await fetch('http://127.0.0.1:5000/load_pgn', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ pgn })
        });
    
        if (response.ok) {
            const data = await response.json();
            setGamePosition(data.initialFen);
            setMoveHistory(data.moveList);
            setCurrentStep(0);
        } else {
            console.error('Failed to load PGN');
        }
    };
    
    const evaluation = async () => {
        try {
            const response = await fetch('/evaluation', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({pgn: currentPgn})
            });
            const data = await response.json();
            if (data.status === 'success') {
                // Display analysis results
            } else {
                console.error(data.message);
            }
        } catch (error) {
            console.error('Error analyzing game:', error);
        }
    };    
    
    // Logic to flip the board
    const flipBoard = () => {
        setBoardOrientation(boardOrientation === 'white' ? 'black' : 'white');
        console.log("Board orientation flipped to:", boardOrientation === 'white' ? 'black' : 'white');
    };    

    const updateGamePosition = useCallback((position) => {
        setGamePosition(position);
    }, []);

    return (
        <div style={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'flex-start', padding: '20px', height: 'calc(100vh - 90px)' }}>
            <FairyBoard 
                boardOrientation={boardOrientation}
                gamePosition={gamePosition}
                setExternalGamePosition={updateGamePosition}
                updateMoveHistory={updateMoveHistory} />
            <SideMenu 
                startNewGame={startNewGame} 
                navigateHistory={navigateHistory} 
                flipBoard={flipBoard}
                moveHistory={moveHistory}
                loadGameFromPgn={loadGameFromPgn} />

        </div>
    );
};

export default ParentComponent;