import React, { useState } from 'react';
import ProfileCard from './ProfileCard'; // Assuming you have a ProfileCard component

const ProfilesPage = () => {
  // Dummy profile data for testing
  const dummyProfiles = [
    { name: 'John Doe', elo: 1500, winRate: '70%' },
    { name: 'Alice Smith', elo: 1600, winRate: '65%' },
    { name: 'Bob Johnson', elo: 1450, winRate: '75%' },
    // Add more profiles as needed
  ];

  // State for the search input
  const [searchInput, setSearchInput] = useState('');

  // State for filtered profiles
  const [filteredProfiles, setFilteredProfiles] = useState(dummyProfiles);

  // Handle search input change
  const handleSearchInputChange = (e) => {
    const inputValue = e.target.value;
    setSearchInput(inputValue);

    // Filter profiles based on the search input
    const filtered = dummyProfiles.filter((profile) =>
      profile.name.toLowerCase().includes(inputValue.toLowerCase())
    );

    setFilteredProfiles(filtered);
  };

  return (
    <div>
      <h1>Profiles</h1>
      <div>
        {/* Search bar */}
        <input
          type="text"
          placeholder="Search profiles..."
          value={searchInput}
          onChange={handleSearchInputChange}
        />
      </div>
      <div>
        {/* Profile cards */}
        {filteredProfiles.map((profile, index) => (
          <ProfileCard
            key={index}
            name={profile.name}
            elo={profile.elo}
            winRate={profile.winRate}
          />
        ))}
      </div>
    </div>
  );
};

export default ProfilesPage;
