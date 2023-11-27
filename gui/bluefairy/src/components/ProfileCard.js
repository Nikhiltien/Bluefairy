import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const ProfileCard = ({ name, elo, winRate }) => {
  return (
    <Card style={{ marginBottom: 20 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {name}
        </Typography>
        <Typography color="text.secondary">
          Elo: {elo}
        </Typography>
        <Typography color="text.secondary">
          Win Rate: {winRate}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ProfileCard;