import React from 'react';
import { CssBaseline, Box } from '@mui/material';
import MenuBar from './components/MenuBar';
import AppRouter from './AppRouter'; // Import AppRouter

const App = () => {
  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to right, #0A1929, #123456)' }}>
      <CssBaseline />
      <MenuBar />
      <Box style={{ marginTop: '20px', padding: '20px' }}>
        <AppRouter /> {/* Use AppRouter here */}
      </Box>
    </div>
  );
};

export default App;