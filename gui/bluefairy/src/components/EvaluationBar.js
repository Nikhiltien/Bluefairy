import React, { useState, useEffect } from 'react';
import { Paper, Typography, Box } from '@mui/material';

const EvaluationBar = ({ score }) => {
    const [progressHeight, setProgressHeight] = useState('50%');
    const [barPosition, setBarPosition] = useState('bottom');

    useEffect(() => {
        let normalizedHeight;
        if (score >= 0) {
            // Positive scores fill from top
            normalizedHeight = 50 + ((score / 10) * 50);
            setBarPosition('top');
        } else {
            // Negative scores fill from bottom
            normalizedHeight = 50 - ((Math.abs(score) / 10) * 50);
            setBarPosition('bottom');
        }
        setProgressHeight(`${Math.max(0, Math.min(100, normalizedHeight))}%`);
    }, [score]);

    // Swap colors here
    const barColor = score > 0 ? '#D3D3D3' : '#A9A9A9';  // Light grey for positive, dark grey for negative

    const displayScore = score !== null ? score.toFixed(2).toString() : '0';

    return (
        <Paper style={{ width: '40px', height: '550px', marginLeft: '20px', textAlign: 'center', backgroundColor: '#333333', position: 'relative' }}>
            <Box
                sx={{
                    position: 'absolute',
                    bottom: 0,
                    left: '5px',
                    right: '5px',
                    height: progressHeight,
                    backgroundColor: barColor,
                    border: '1px solid #888',
                    transition: 'height 0.5s ease-in-out',
                }}
            />
            <Typography variant="body1" style={{ position: 'absolute', width: '100%', top: '50%', transform: 'translateY(-50%)', color: '#FFFFFF' }}>
                {displayScore}
            </Typography>
        </Paper>
    );
};

export default EvaluationBar;
