import React, { useState, useEffect } from 'react';
import { Paper, Typography, LinearProgress, Box } from '@mui/material';

const EvaluationBar = ({ score }) => {
    const [progress, setProgress] = useState(50); // Middle of the bar represents an even score

    useEffect(() => {
        // Convert the chess score to a percentage for the progress bar
        const normalizedScore = (score + 10) / 20 * 100;
        setProgress(normalizedScore);
    }, [score]);

    const progressColor = score > 0 ? 'white' : 'black';

    return (
        <Paper style={{ width: '30px', height: '550px', marginLeft: '20px', textAlign: 'center', padding: '10px', backgroundColor: '#ffffff' }}>
            <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column-reverse', height: '100%' }}>
                <LinearProgress
                    variant="determinate"
                    value={progress}
                    sx={{ height: '100%', '& .MuiLinearProgress-bar': { backgroundColor: progressColor } }}
                />
            </Box>
            <Typography variant="body1" style={{ color: 'black' }}>
                {score >= 0 ? `+${score}` : score}
            </Typography>
        </Paper>
    );
};

export default EvaluationBar;
