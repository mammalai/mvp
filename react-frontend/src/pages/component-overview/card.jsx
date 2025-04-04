import { useEffect } from 'react';

import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import AddIcon from '@mui/icons-material/Add';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { red } from '@mui/material/colors';

import ButtonBase from '@mui/material/ButtonBase';

import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';

import { useTheme } from '@mui/material/styles';

export default function ButtonDemo() {
  const theme = useTheme();

  useEffect(() => {}, []);

  return (
    <Box bgcolor="#FFFFFF" width="100%" height="100%" sx={{ p: 5 }}>
      <Stack spacing={6} direction="column">
        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Filled Card</Typography>
          </Box>
          <Grid container>
            <Grid item xs={12} md={6}>
              <Card variant="filled">
                <CardHeader
                  avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
                      R
                    </Avatar>
                  }
                  action={
                    <IconButton aria-label="settings" sx={{ color: theme.palette.m3.onSurface }}>
                      <MoreVertIcon />
                    </IconButton>
                  }
                  title="Shrimp and Chorizo Paella"
                  subheader="September 14, 2016"
                />
                <CardMedia
                  component="img"
                  height="194"
                  image="https://plus.unsplash.com/premium_photo-1719522017304-e56503664ffd?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                  alt="Paella dish"
                />
                <CardContent>
                  <Typography variant="body2">
                    This impressive paella is a perfect party dish and a fun meal to cook together with your guests. Add 1 cup of frozen
                    peas along with the mussels, if you like.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Stack>

        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Outlined Card</Typography>
          </Box>
          <Grid container>
            <Grid item xs={12} md={6}>
              <Card variant="outlined">
                <CardHeader
                  avatar={
                    <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
                      R
                    </Avatar>
                  }
                  action={
                    <IconButton aria-label="settings" sx={{ color: theme.palette.m3.onSurface }}>
                      <MoreVertIcon />
                    </IconButton>
                  }
                  title="Shrimp and Chorizo Paella"
                  subheader="September 14, 2016"
                />
                <CardMedia
                  component="img"
                  height="194"
                  image="https://plus.unsplash.com/premium_photo-1719522017304-e56503664ffd?q=80&w=3270&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                  alt="Paella dish"
                />
                <CardContent>
                  <Typography variant="body2">
                    This impressive paella is a perfect party dish and a fun meal to cook together with your guests. Add 1 cup of frozen
                    peas along with the mussels, if you like.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Stack>
      </Stack>
    </Box>
  );
}
