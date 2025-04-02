import { useEffect } from 'react';

import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import AddIcon from '@mui/icons-material/Add';

import ButtonBase from '@mui/material/ButtonBase';

import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';

import { useTheme } from '@mui/material/styles';

export default function ButtonDemo() {
  const theme = useTheme();

  useEffect(() => {}, []);

  return (
    <Box width="100%" height="100%" sx={{ p: 5 }}>
      <Stack spacing={6} direction="column">
        {/* FILLED BUTTONS */}
        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Filled Buttons</Typography>
          </Box>

          <Box>
            <Button variant="contained">Label</Button>
          </Box>

          <Box>
            <Button variant="contained" startIcon={<AddIcon />}>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="contained" disabled>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="contained" startIcon={<AddIcon />} disabled>
              Label
            </Button>
          </Box>
        </Stack>

        {/* FILLED BUTTONS */}
        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Outlined Buttons</Typography>
          </Box>

          <Box>
            <Button variant="outlined">Label</Button>
          </Box>

          <Box>
            <Button variant="outlined" startIcon={<AddIcon />}>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="outlined" disabled>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="outlined" startIcon={<AddIcon />} disabled>
              Label
            </Button>
          </Box>
        </Stack>

        {/* TEXT BUTTONS */}
        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Text Buttons</Typography>
          </Box>

          <Box>
            <Button variant="text">Label</Button>
          </Box>

          <Box>
            <Button variant="text" startIcon={<AddIcon />}>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="text" disabled>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="text" startIcon={<AddIcon />} disabled>
              Label
            </Button>
          </Box>
        </Stack>

        {/* ELEVATED BUTTONS */}
        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Elevated Buttons</Typography>
          </Box>

          <Box>
            <Button variant="elevated">Label</Button>
          </Box>

          <Box>
            <Button variant="elevated" startIcon={<AddIcon />}>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="elevated" disabled>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="elevated" startIcon={<AddIcon />} disabled>
              Label
            </Button>
          </Box>
        </Stack>

        {/* TONAL BUTTONS */}
        <Stack spacing={2} direction="column">
          <Box>
            <Typography variant="titleMedium">Tonal Buttons</Typography>
          </Box>

          <Box>
            <Button variant="tonal">Label</Button>
          </Box>

          <Box>
            <Button variant="tonal" startIcon={<AddIcon />}>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="tonal" disabled>
              Label
            </Button>
          </Box>

          <Box>
            <Button variant="tonal" startIcon={<AddIcon />} disabled>
              Label
            </Button>
          </Box>
        </Stack>
      </Stack>
    </Box>
  );
}
