import React, { useState, useCallback } from 'react';
import FairyBoard from './components/FairyBoard';
import SideMenu from './components/SideMenu';

const ParentComponent = () => {
    const initialFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
    const [boardOrientation, setBoardOrientation] = useState('white');
    const [gamePosition, setGamePosition] = useState(initialFen);
    const [currentStep, setCurrentStep] = useState(0);
    const [moveHistory, setMoveHistory] = useState([])

    // Logic to start a new game in FairyBoard
    const startNewGame = () => {
        setMoveHistory([initialFen]);
        setCurrentStep(0);
        setGamePosition(initialFen);
    };    

    // Logic to navigate through game history
    const navigateHistory = (step) => {
        const newStep = currentStep + step;
        if (newStep >= 0 && newStep < moveHistory.length) {
            setCurrentStep(newStep);
            setGamePosition(moveHistory[newStep]);
        }
    };
    
    const updateMoveHistory = useCallback((newPosition) => {
        setMoveHistory(prevHistory => [...prevHistory, newPosition]);
        setCurrentStep(prevStep => prevStep + 1); // Update to point to the latest move
    }, []);
    
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
                flipBoard={flipBoard} />
        </div>
    );
};

export default ParentComponent;