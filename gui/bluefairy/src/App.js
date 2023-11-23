import React from 'react';
import { CssBaseline, Box, Grid } from '@mui/material';
import MenuBar from './components/MenuBar';
import ParentComponent from './ParentComponent';

const App = () => {
  return (
    <>
      <CssBaseline />
      <div style={{ minHeight: '100vh', background: 'linear-gradient(to right, #0A1929, #123456)' }}>
        <MenuBar />
        <Box style={{ marginTop: '20px', padding: '20px' }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={12} style={{ display: 'flex', justifyContent: 'center' }}>
              <ParentComponent />
            </Grid>
          </Grid>
        </Box>
      </div>
    </>
  );
};

export default App;