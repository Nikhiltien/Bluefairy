import React from 'react';
import { Paper, Tabs, Tab } from '@mui/material';

const Sidemenu = () => {
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <Paper style={{ width: '300px', marginLeft: '20px' }}>
            <Tabs
                orientation="vertical"
                variant="scrollable"
                value={value}
                onChange={handleChange}
            >
                <Tab label="Game Selection" />
                <Tab label="Computer Analysis" />
                <Tab label="User Notes" />
            </Tabs>
            {/* Placeholder for tab content */}
        </Paper>
    );
};

export default Sidemenu;
