import { useEffect } from 'react';

import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import AddIcon from '@mui/icons-material/Add';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';

import ButtonBase from '@mui/material/ButtonBase';

import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';

import { useTheme } from '@mui/material/styles';

export default function ButtonDemo() {
  const dataJson = [
    { title: 'Buttons', description: 'Buttons are used to trigger actions in the application.' },
    { title: 'Cards', description: 'Cards are a flexible and extensible content container.' },
    { title: 'Tables', description: 'Tables are used to display data in a structured format.' },
    { title: 'Tabs', description: 'Tabs are used to switch between different views or content.' }
  ];

  const theme = useTheme();

  useEffect(() => {}, []);

  return (
    <Box width="100%" height="100%" sx={{ p: 5 }}>
      <Stack spacing={6} direction="column">
        {/* ALL COMPONENTS */}
        <Stack spacing={2} direction="column" sx={{ marginLeft: -2 }}>
          <Box>
            <Typography variant="titleMedium">All components</Typography>
          </Box>

          <Grid container spacing={2}>
            {dataJson.map((item, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card variant="outlined" sx={{ width: '100%' }}>
                  <CardHeader title={item.title} />
                  <Box display="flex" justifyContent="flex-end">
                    <Button variant="text">Learn more</Button>
                  </Box>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Stack>
      </Stack>
    </Box>
  );
}
