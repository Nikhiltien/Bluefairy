import React from 'react';
import { Card, CardContent, Typography, Avatar, Grid, CardActions, Button } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person'; // You can replace this with an actual image

const ProfileCard = ({ name, elo, winRate }) => {
  return (
    <Card style={{ marginBottom: 20, maxWidth: 345 }}>
      <CardContent>
        <Grid container spacing={2} alignItems="center">
          <Grid item>
            <Avatar>
              <PersonIcon />
            </Avatar>
          </Grid>
          <Grid item xs>
            <Typography gutterBottom variant="h5" component="div">
              {name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Elo: {elo}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Win Rate: {winRate}
            </Typography>
          </Grid>
        </Grid>
      </CardContent>
      <CardActions>
        <Button size="small">View Profile</Button>
        {/* <Button size="small">Challenge</Button> */}
      </CardActions>
    </Card>
  );
};

export default ProfileCard;
