import React, { useState } from 'react';
import { Paper, Tabs, Tab, IconButton, Menu, MenuItem } from '@mui/material';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import FirstPageIcon from '@mui/icons-material/FirstPage';
import LastPageIcon from '@mui/icons-material/LastPage';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import SettingsIcon from '@mui/icons-material/Settings';
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

const SideMenu = ({ startNewGame, navigateHistory, flipBoard }) => {
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

    return (
        <GradientPaper>
            <Tabs orientation="vertical" variant="scrollable" value={value} onChange={handleChange}>
                <WhiteTextTab label="New Game" onClick={startNewGame} />
                <WhiteTextTab label="Game Library" />
                <WhiteTextTab label="Settings" onClick={handleOpenSettings} />
            </Tabs>

            {/* Settings Menu */}
            <Menu
                anchorEl={settingsAnchorEl}
                open={Boolean(settingsAnchorEl)}
                onClose={handleCloseSettings}
            >
                <MenuItem onClick={handleCloseSettings}>Engine Toggle</MenuItem>
                {/* Additional settings options */}
            </Menu>

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