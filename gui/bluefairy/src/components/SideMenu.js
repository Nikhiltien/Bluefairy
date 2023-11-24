import React, { useState } from 'react';
import GameLibraryTab from './GameLibraryTab';
import { Paper, Tabs, Tab, IconButton, Menu, MenuItem, List, ListItem, Grid, ListItemText } from '@mui/material';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import FirstPageIcon from '@mui/icons-material/FirstPage';
import LastPageIcon from '@mui/icons-material/LastPage';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import { styled } from '@mui/material/styles';

const GradientPaper = styled(Paper)({
    background: 'linear-gradient(180deg, #252525 0%, #3D3D3D 100%)',
    color: 'white',
    width: '300px',
    marginLeft: '20px',
    padding: '10px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    height: '100%',
    boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.5)', // Adds shadow for depth
    border: '1px solid #474747', // Adds a subtle border
});

const WhiteTextTab = styled(Tab)({
    color: 'white', // Set text color to white
});

const MoveHistoryList = styled(List)({
    maxHeight: 200, // Set a maximum height
    overflow: 'auto', // Enable scrolling
    backgroundColor: '#3D3D3D',
    color: 'white',
    marginTop: '10px',
});

const SideMenu = ({ startNewGame, navigateHistory, flipBoard, moveHistory, loadGameFromPgn }) => {
    const [value, setValue] = useState(0);
    const [settingsAnchorEl, setSettingsAnchorEl] = useState(null);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const handleOpenSettings = (event) => {
        setSettingsAnchorEl(event.currentTarget);
    };

    const handleCloseSettings = () => {
        setSettingsAnchorEl(null);
    };

    const pairedMoves = [];
    for (let i = 0; i < moveHistory.length; i += 2) {
        pairedMoves.push({
            moveNumber: Math.floor(i / 2) + 1,
            white: moveHistory[i],
            black: moveHistory[i + 1]
        });
    }

    return (
        <GradientPaper>
            <Tabs orientation="vertical" variant="scrollable" value={value} onChange={handleChange}>
                <WhiteTextTab label="New Game" onClick={startNewGame} />
                <WhiteTextTab label="Game Library" />
                <WhiteTextTab label="Settings" onClick={handleOpenSettings} />
            </Tabs>

            {value === 1 && <GameLibraryTab loadGameFromPgn={loadGameFromPgn} />}

            {/* Settings Menu */}
            <Menu
                anchorEl={settingsAnchorEl}
                open={Boolean(settingsAnchorEl)}
                onClose={handleCloseSettings}
            >
                <MenuItem onClick={handleCloseSettings}>Engine Toggle</MenuItem>
                {/* Additional settings options */}
            </Menu>

            <MoveHistoryList>
                {pairedMoves.map(({ moveNumber, white, black }) => (
                    <ListItem key={moveNumber}>
                        <Grid container spacing={2}>
                            <Grid item xs={4}>
                                {moveNumber}.
                            </Grid>
                            <Grid item xs={4}>
                                {white}
                            </Grid>
                            <Grid item xs={4}>
                                {black || ''}
                            </Grid>
                        </Grid>
                    </ListItem>
                ))}
            </MoveHistoryList>

            <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <IconButton style={{ color: 'white' }} onClick={() => navigateHistory(-2)}>
                    <FirstPageIcon />
                </IconButton>
                <IconButton style={{ color: 'white' }} onClick={() => navigateHistory(-1)}>
                    <ArrowBackIosNewIcon />
                </IconButton>
                <IconButton style={{ color: 'white' }} onClick={flipBoard}>
                    <AutorenewIcon />
                </IconButton>
                <IconButton style={{ color: 'white' }} onClick={() => navigateHistory(1)}>
                    <ArrowForwardIosIcon />
                </IconButton>
                <IconButton style={{ color: 'white' }} onClick={() => navigateHistory(2)}>
                    <LastPageIcon />
                </IconButton>
            </div>
        </GradientPaper>
    );
};

export default SideMenu;