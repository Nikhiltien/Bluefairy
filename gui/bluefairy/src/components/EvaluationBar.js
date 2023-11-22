import React from 'react';
import { Paper, Typography } from '@mui/material';

const EvaluationBar = () => {
    return (
        <Paper style={{ width: '30px', height: '550px', marginLeft: '20px', textAlign: 'center', padding: '10px', backgroundColor: '#ffffff' }}>
            <Typography variant="body1" style={{ color: 'white' }}>
            </Typography>
            {/* Placeholder for evaluation metrics */}
        </Paper>
    );
};

export default EvaluationBar;
