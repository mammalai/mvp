import { useEffect, useState } from 'react';


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

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';



import ButtonBase from '@mui/material/ButtonBase';

import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';

import { useTheme } from '@mui/material/styles';




export default function ButtonDemo() {

  const [value, setValue] = useState('one');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };


  const theme = useTheme();

  useEffect(() => {

  }, []);

  
  return (
    <Box bgcolor="#FFFFFF" width="100%" height="100%" sx={{p:5}}>
      <Stack spacing={6} direction="column">
        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Horizontal Tabs</Typography>
          </Box>
          <Grid container >
            <Tabs
              value={value}
              onChange={handleChange}
              aria-label="secondary tabs example"
              sx={{
                width: '100%',
                '& .MuiTabs-flexContainer': {
                  width: '100%',
                  display: 'flex',
                  justifyContent: 'space-between'
                },
                '& .MuiTab-root': {
                  flex: 1,
                  maxWidth: 'none'
                }
              }}
            >
              <Tab value="one" label="Overview" />
              <Tab value="two" label="Specs" />
              <Tab value="three" label="Guidelines" />
              <Tab value="four" label="Accessability" />
            </Tabs>
          </Grid>
        </Stack>

        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Vertical Tabs</Typography>
          </Box>
          <Grid container >
            <Tabs
              value={value}
              onChange={handleChange}
              orientation="vertical"
              aria-label="secondary tabs example"
              sx={{
                width: '20%',
                '& .MuiTabs-flexContainer': {
                  width: '100%',
                  display: 'flex',
                  justifyContent: 'space-between'
                },
                '& .MuiTab-root': {
                  flex: 1,
                  maxWidth: 'none'
                }
              }}
            >
              <Tab value="one" label="Overview" />
              <Tab value="two" label="Specs" />
              <Tab value="three" label="Guidelines" />
              <Tab value="four" label="Accessability" />
            </Tabs>
          </Grid>
        </Stack>

      </Stack>
      
      
      
    </Box>
    
  );
}
