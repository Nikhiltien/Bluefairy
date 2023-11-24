import React from 'react';
import { Paper, Grid } from '@mui/material';
import { styled } from '@mui/material/styles';

const HistoryPaper = styled(Paper)({
    background: 'linear-gradient(180deg, #252525 0%, #3D3D3D 100%)',
    color: 'white',
    width: '300px',
    margin: '20px',
    padding: '10px',
    overflowY: 'auto',
    height: 'calc(100% - 40px)',
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.5)',
    border: '1px solid #474747',
});

const MoveHistory = ({ moveHistory }) => {
    // Process the moveHistory to pair the moves
    const pairedMoves = [];
    for (let i = 0; i < moveHistory.length; i += 2) {
        pairedMoves.push({
            moveNumber: Math.floor(i / 2) + 1,
            white: moveHistory[i],
            black: moveHistory[i + 1]
        });
    }

    return (
        <HistoryPaper>
            <Grid container spacing={2}>
                {pairedMoves.map(({ moveNumber, white, black }) => (
                    <React.Fragment key={moveNumber}>
                        <Grid item xs={4}>
                            {moveNumber}.
                        </Grid>
                        <Grid item xs={4}>
                            {white}
                        </Grid>
                        <Grid item xs={4}>
                            {black || ''}
                        </Grid>
                    </React.Fragment>
                ))}
            </Grid>
        </HistoryPaper>
    );
};

export default MoveHistory;
