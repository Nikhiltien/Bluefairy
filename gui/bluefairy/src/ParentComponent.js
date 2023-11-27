import React, { useState, useCallback, useEffect } from 'react';
import FairyBoard from './components/FairyBoard';
import SideMenu from './components/SideMenu';
import EvaluationBar from './components/EvaluationBar';
import { Chess } from 'chess.js';

class MoveNode {
    constructor(move, position, parent = null) {
        this.move = move; // SAN notation of the move
        this.position = position; // FEN string after the move
        this.parent = parent; // Reference to the parent node
        this.children = []; // Array of child nodes
    }

    addChild(move, position) {
        const childNode = new MoveNode(move, position, this);
        this.children.push(childNode);
        return childNode;
    }
}

const ParentComponent = () => {
    const initialFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
    const root = new MoveNode(null, initialFen);
    const [currentNode, setCurrentNode] = useState(new MoveNode(null, initialFen));
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
        console.log(gamePosition)
        if (ws) {
            ws.send(JSON.stringify({ command: 'reset' }));
        }
    };

    // Logic to navigate through game history
    const navigateHistory = (step) => {
        let newCurrentNode = currentNode;
        if (step === -1 && newCurrentNode.parent) { // Move back
            newCurrentNode = newCurrentNode.parent;
        } else if (step === 1 && newCurrentNode.children.length > 0) { // Move forward
            newCurrentNode = newCurrentNode.children[0]; // Assuming the first child is the main line
        }
    
        setCurrentNode(newCurrentNode);
        setGamePosition(newCurrentNode.position);
    };     
    
    const [currentPgn, setCurrentPgn] = useState('');

    // const [pgnInput, setPgnInput] = useState('');

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
        // Create a new move node and update the current node
        const game = new Chess(currentNode.position);
        game.move(sanMove);
        const newPosition = game.fen();
        const newNode = currentNode.addChild(sanMove, newPosition);
    
        setCurrentNode(newNode);
        setCurrentPgn(game.pgn());
    
        if (ws) {
            ws.send(JSON.stringify({ move: sanMove }));
        }
    }, [currentNode, ws]);        

    const loadGameFromPgn = async (pgn) => {
        const response = await fetch('http://127.0.0.1:5000/load_pgn', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ pgn })
        });
    
        if (response.ok) {
            const data = await response.json();
            setMoveHistory(data.moveList);
            setCurrentStep(0);
    
            // Update the chess.js instance with moves from the PGN
            const game = new Chess();
            data.moveList.forEach(move => {
                game.move(move);
            });
            setGamePosition(game.fen()); // Update the game position to the final state after applying moves
            setCurrentStep(0);
        } else {
            console.error('Failed to load PGN');
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