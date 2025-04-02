// material-ui
import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';

import Typography from '../typography';

// ==============================|| OVERRIDES - TAB ||============================== //

export default function Tab(theme) {
  return {
    MuiTab: {
      styleOverrides: {
        root: {
          minHeight: 46,
          color: theme.palette.m3.onSurface, // font color
          ...Typography().labelLarge,
          fontWeight: 400,
          '&.Mui-selected': {
            color: theme.palette.m3.onSecondaryContainer,
            backgroundColor: theme.palette.m3.secondaryContainer,
            fontWeight: 500,
            outline: 'none',
            borderBottom: 'none'
          },
          '&.Mui-selected:hover': {
            backgroundColor: blend(theme.palette.m3.secondaryContainer, theme.palette.m3.onSurface, 0.08),
            color: theme.palette.m3.onSecondaryContainer,
            fontWeight: 500
          },
          '&:hover': {
            backgroundColor: blend(theme.palette.m3.surface, theme.palette.m3.onSurface, 0.08),
            color: theme.palette.m3.onSurface,
            fontWeight: 500
          },
          '&:focus-visible': {
            borderRadius: 28,
            backgroundColor: theme.palette.m3.secondaryContainer,
            outline: `2px solid ${theme.palette.secondary.dark}`,
            outlineOffset: -3
          }
        }
      }
    }
  };
}
