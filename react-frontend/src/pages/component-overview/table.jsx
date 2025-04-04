import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import { useTheme } from '@mui/material/styles';
import Typography from '@mui/material/Typography';

function createData(name, calories, fat, carbs, protein) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9)
];

export default function BasicTable() {
  const theme = useTheme();

  return (
    <Box bgcolor="" width="100%" height="100%" sx={{ p: 5 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} md={8}>
          <Card
            variant="outlined"
            sx={{
              borderRadius: '28px',
              border: `1px solid ${theme.palette.m3.outlineVariant}`,
              backgroundColor: 'transparent',
              minWidth: 700
            }}
          >
            <TableContainer>
              <Table
                aria-label="simple table"
                sx={{
                  minWidth: 650,
                  '& .MuiTableRow-root:hover': {
                    backgroundColor: 'transparent'
                  }
                }}
              >
                <TableHead
                  sx={{
                    bgcolor: theme.palette.m3.surface,
                    borderBottom: `1px solid ${theme.palette.m3.outlineVariant}`
                  }}
                >
                  <TableRow>
                    <TableCell>
                      <Typography variant="bodyLarge">
                        <b>Dessert (100g serving)</b>
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="bodyLarge">
                        <b>Calories</b>
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="bodyLarge">
                        <b>Fat&nbsp;(g)</b>
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="bodyLarge">
                        <b>Carbs&nbsp;(g)</b>
                      </Typography>
                    </TableCell>
                    <TableCell align="right">
                      <Typography variant="bodyLarge">
                        <b>Protein&nbsp;(g)</b>
                      </Typography>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {rows.map((row) => (
                    <TableRow
                      key={row.name}
                      hover
                      sx={{
                        // '&:last-child td, &:last-child th': { border: 0 },
                        backgroundColor: 'none',
                        '&:hover': { backgroundColor: 'none' },
                        '& td, & th': {
                          borderBottom: `1px solid ${theme.palette.m3.outlineVariant}`
                        }
                      }}
                    >
                      <TableCell
                      // component="th"
                      // scope="row"
                      // sx={{borderRight: `1px solid #000`, }}
                      >
                        {row.name}
                      </TableCell>
                      <TableCell align="right">{row.calories}</TableCell>
                      <TableCell align="right">{row.fat}</TableCell>
                      <TableCell align="right">{row.carbs}</TableCell>
                      <TableCell align="right">{row.protein}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
