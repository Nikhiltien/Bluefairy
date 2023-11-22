import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';

const MenuBar = () => {
    return (
        <AppBar position="static" style={{ background: '#0A1929' }}>
            <Toolbar>
                <Typography variant="h6" style={{ flexGrow: 1 }}>
                    Chess Analysis App
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