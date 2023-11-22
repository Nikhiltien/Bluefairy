import React from 'react';
import { CssBaseline, Box, Grid } from '@mui/material';
import MenuBar from './components/MenuBar';
import FairyBoard from './components/FairyBoard';
import EvaluationBar from './components/EvaluationBar';
import Sidebar from './components/SideMenu';

const App = () => {
  return (
      <>
          <CssBaseline />
          <div style={{ minHeight: '100vh', background: 'linear-gradient(to right, #0A1929, #123456)' }}>
              <MenuBar />
              <Box style={{ marginTop: '20px', padding: '20px' }}>
                  <Grid container spacing={2}>
                      <Grid item xs={12} md={8} style={{ display: 'flex', justifyContent: 'center' }}>
                          <div style={{ display: 'flex' }}>
                              <EvaluationBar />
                              <FairyBoard />
                          </div>
                      </Grid>
                      <Grid item xs={12} md={4}>
                          <Sidebar />
                      </Grid>
                  </Grid>
              </Box>
          </div>
      </>
  );
};

export default App;