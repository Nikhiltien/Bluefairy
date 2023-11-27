import React, { useState, useEffect } from 'react';
import { Paper, Typography, Box } from '@mui/material';

const EvaluationBar = ({ score }) => {
    const [progressHeight, setProgressHeight] = useState('50%');

    useEffect(() => {
        const normalizedHeight = ((score + 10) / 20) * 100 + '%';
        setProgressHeight(normalizedHeight);
    }, [score]);

    const barColor = score > 0 ? '#A9A9A9' : '#D3D3D3';  // Dark grey for positive, light grey for negative

    const displayScore = score !== null ? score.toFixed(2).toString() : '0';  // Display score with 2 decimal places

    return (
        <Paper style={{ width: '40px', height: '550px', marginLeft: '20px', textAlign: 'center', backgroundColor: '#333333', position: 'relative' }}>  {/* Dark grey background */}
            <Box
                sx={{
                    position: 'absolute',
                    bottom: '5px', // Reduced padding
                    left: '5px',
                    right: '5px',
                    top: '5px',
                    height: progressHeight,
                    backgroundColor: barColor,
                    border: '1px solid #888',
                    transition: 'height 0.5s ease-in-out',  // Animate height change
                }}
            />
            <Typography variant="body1" style={{ position: 'absolute', width: '100%', top: '50%', transform: 'translateY(-50%)', color: '#FFFFFF' }}>  {/* White text for contrast */}
                {displayScore}
            </Typography>
        </Paper>
    );
};

export default EvaluationBar;
