import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';
import { useEffect } from 'react';

// import the typography function
import Typography from '../typography';

/***************************  OVERRIDES - BUTTON  ***************************/

export const generateFocusVisibleStyles = (color) => ({
  outline: `2px solid ${color}`,
  outlineOffset: 2
});


export default function Card(theme) {

  useEffect(() => {
    console.log(Typography().titleMedium);
  }, []);


  return {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          '& .MuiCardHeader-subheader': {
            ...Typography().bodyMedium,
            color: theme.palette.m3.onSurface
          }
        }
      },
      variants: [
        {
          props: { variant: 'outlined' },
          style: {
            backgroundColor: theme.palette.m3.surface,
            border: `1px solid ${theme.palette.m3.outlineVariant}`,
            '& .MuiCardHeader-title': {
              ...Typography().titleMedium,
              color: theme.palette.m3.onSurface
            },
            
          }
        },
        {
          props: { variant: 'filled' },
          style: {
            backgroundColor: theme.palette.m3.surfaceContainerHighest,
          }
        }

      ]
    }
  };
}