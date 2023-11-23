import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import '../App.css';

const MenuBar = () => {
    return (
        <AppBar position="static" style={{ background: '#0A1929' }}>
            <Toolbar>
                <Typography variant="h6" style={{ flexGrow: 1, fontFamily: 'Roboto Mono, monospace', fontSize: '1.5em', color: '#fff' }}>
                    BlueFairy
                </Typography>
                <Button color="inherit">Home</Button>
                <Button color="inherit">Analysis</Button>
                <Button color="inherit">Games Library</Button>
                <Button color="inherit">Settings</Button>
            </Toolbar>
        </AppBar>
    );
};

export default MenuBar;