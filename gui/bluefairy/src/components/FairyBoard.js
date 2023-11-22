import React from 'react';
import { Chessboard } from 'react-chessboard';

const FairyBoard = () => {
    return (
        <div style={{ display: 'flex' }}>
            <Chessboard boardWidth={500} />
        </div>
    );
};

export default FairyBoard;
