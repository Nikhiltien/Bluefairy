import React, { useState, useCallback, useEffect } from 'react';
import FairyBoard from './components/FairyBoard';
import SideMenu from './components/SideMenu';
import EvaluationBar from './components/EvaluationBar';
import { Chess } from 'chess.js';

const ParentComponent = () => {
    const initialFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
    const [boardOrientation, setBoardOrientation] = useState('white');
    const [gamePosition, setGamePosition] = useState(initialFen);
    const [currentStep, setCurrentStep] = useState(0);
    const [moveHistory, setMoveHistory] = useState([])
    const [evaluationScore, setEvaluationScore] = useState(0);

    // Logic to start a new game in FairyBoard
    const startNewGame = () => {
        setMoveHistory([]);
        setCurrentStep(0);
        setGamePosition(initialFen);
    
        if (ws) {
            ws.send(JSON.stringify({ command: 'reset' }));
        }
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

    const [ws, setWs] = useState(null);

    useEffect(() => {
        const webSocketUrl = "ws://127.0.0.1:5000/ws"; // Adjust the URL as needed
        const newWs = new WebSocket(webSocketUrl);

        newWs.onopen = () => {
            console.log("Connected to WebSocket");
        };

        newWs.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Received from backend:", data);
            if (data.fen) {
                setGamePosition(data.fen);
            }
            if (data.evaluation) {
                setEvaluationScore(data.evaluation);
            }
        };

        newWs.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        setWs(newWs);

        // Cleanup function
        return () => {
            newWs.close();
        };
    }, []);

    // Include WebSocket as a dependency in useEffect
    useEffect(() => {
        if (ws) {
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.fen) {
                    setGamePosition(data.fen);
                }
                if (data.evaluation) {
                    setEvaluationScore(data.evaluation);
                }
            };
        }
    }, [ws]);

    const updateMoveHistory = useCallback((sanMove) => {
        setMoveHistory(prevHistory => {
            const newHistory = [...prevHistory, sanMove];
            const game = new Chess();
            newHistory.forEach(move => game.move(move));
            console.log("Frontend FEN:", game.fen());

            if (ws) {
                ws.send(JSON.stringify({ move: sanMove }));
            }

            setCurrentPgn(game.pgn());
            return newHistory;
        });
        setCurrentStep(prevStep => prevStep + 1);
    }, [ws]);

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
                setEvaluationScore(data.evaluationScore); // Update the evaluation score
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
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-start', gap: '5px' }}>
                <EvaluationBar score={evaluationScore} />
                <FairyBoard 
                    boardOrientation={boardOrientation}
                    gamePosition={gamePosition}
                    setExternalGamePosition={updateGamePosition}
                    updateMoveHistory={updateMoveHistory}
                />
            </div>
            <SideMenu 
                startNewGame={startNewGame} 
                navigateHistory={navigateHistory} 
                flipBoard={flipBoard}
                moveHistory={moveHistory}
                loadGameFromPgn={loadGameFromPgn}
            />
        </div>
    );
};

export default ParentComponent;