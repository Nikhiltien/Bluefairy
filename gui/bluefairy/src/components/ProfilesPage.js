import React, { useState } from 'react';
import ProfileCard from './ProfileCard';
import { TextField, Grid, Container, Typography, Slider, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const ProfilesPage = () => {
  // Dummy data
  const dummyProfiles = [
    { name: 'John Doe', elo: 1500, winRate: '70%', opening: 'Sicilian Defense' },
    { name: 'Alice Smith', elo: 1600, winRate: '65%', opening: 'French Defense' },
    { name: 'Bob Johnson', elo: 1450, winRate: '75%', opening: 'Ruy Lopez' },
    // Add more profiles as needed
  ];

  // State for filters
  const [searchInput, setSearchInput] = useState('');
  const [eloRange, setEloRange] = useState([1000, 2000]);
  const [selectedOpening, setSelectedOpening] = useState('');

  // Filter profiles
  const filteredProfiles = dummyProfiles.filter((profile) =>
    profile.name.toLowerCase().includes(searchInput.toLowerCase()) &&
    profile.elo >= eloRange[0] && profile.elo <= eloRange[1] &&
    (selectedOpening === '' || profile.opening === selectedOpening)
  );

  // Handlers
  const handleSearchInputChange = (e) => {
    setSearchInput(e.target.value);
  };

  const handleEloRangeChange = (event, newValue) => {
    setEloRange(newValue);
  };

  const handleOpeningChange = (event) => {
    setSelectedOpening(event.target.value);
  };

  // Unique list of openings for the dropdown
  const openings = Array.from(new Set(dummyProfiles.map(p => p.opening)));

  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }}>
      <Typography variant="h4" gutterBottom style={{ color: 'lightgrey' }}>
        Profiles
      </Typography>
      
      {/* Search Bar */}
      <TextField
        fullWidth
        label="Search profiles..."
        variant="outlined"
        value={searchInput}
        onChange={handleSearchInputChange}
        style={{ marginBottom: '20px', backgroundColor: 'lightgrey', borderRadius: 4, color: 'black' }}
      />

      {/* Elo Range Slider */}
      <Typography gutterBottom>Elo Range</Typography>
      <Slider
        value={eloRange}
        onChange={handleEloRangeChange}
        valueLabelDisplay="auto"
        min={1000}
        max={3000}
        style={{ marginBottom: '20px' }}
      />

      {/* Opening Dropdown */}
      <FormControl fullWidth style={{ marginBottom: '20px' }}>
        <InputLabel>Most Played Opening</InputLabel>
        <Select
          value={selectedOpening}
          label="Most Played Opening"
          onChange={handleOpeningChange}
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          {openings.map((opening, index) => (
            <MenuItem key={index} value={opening}>{opening}</MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* Profiles Grid */}
      <Grid container spacing={3}>
        {filteredProfiles.map((profile, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <ProfileCard
              name={profile.name}
              elo={profile.elo}
              winRate={profile.winRate}
              opening={profile.opening}
            />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default ProfilesPage;
