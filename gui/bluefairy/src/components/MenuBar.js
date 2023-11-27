import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import '../App.css';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

const MenuBar = () => {
    // Common style for all buttons
    const buttonStyle = {
        fontFamily: 'Roboto Mono, monospace',
        color: '#fff',
        textDecoration: 'none', // Remove underlines from the link
    };

    return (
        <AppBar position="static" style={{ background: '#0A1929' }}>
            <Toolbar>
                <Typography variant="h6" style={{ flexGrow: 1, fontFamily: 'Roboto Mono, monospace', fontSize: '1.5em', color: '#fff' }}>
                    BlueFairy
                </Typography>
                <Link to="/" style={buttonStyle}>
                    <Button color="inherit" style={buttonStyle}>Home</Button>
                </Link>
                <Link to="/profiles" style={buttonStyle}>
                    <Button color="inherit" style={buttonStyle}>Profiles</Button>
                </Link>
                {/* Include other links as needed */}
                <Button color="inherit" style={buttonStyle}>Game Library</Button>
                <Button color="inherit" style={buttonStyle}>Settings</Button>
            </Toolbar>
        </AppBar>
    );
};

export default MenuBar;
