import React from 'react';
import { Paper, Typography } from '@mui/material';

const EvaluationBar = () => {
    return (
        <Paper style={{ width: '30px', height: '500px', marginLeft: '20px', textAlign: 'center', padding: '10px', backgroundColor: '#0D2233' }}>
            <Typography variant="body1" style={{ color: 'white' }}>
            </Typography>
            {/* Placeholder for evaluation metrics */}
        </Paper>
    );
};

export default EvaluationBar;
