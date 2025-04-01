// @project

import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';


/***************************  OVERRIDES - BUTTON  ***************************/

export const generateFocusVisibleStyles = (color) => ({
  outline: `2px solid ${color}`,
  outlineOffset: 2
});


export default function Button(theme) {
  return {
    MuiButton: {
      defaultProps: {
        disableFocusRipple: false
      },
      styleOverrides: {
        root: {
          fontSize: 14,
          lineHeight: 1.429,
          letterSpacing: 0.1,
          borderRadius: 100,
          borderWidth: 1.5,
          borderColor: theme.palette.m3.primary,
          boxShadow: 'none',

          // '&:focus-visible': generateFocusVisibleStyles(theme.palette.primary.main)
        },
        sizeSmall: {
          fontSize: 13,
          height: 34,
          padding: '10px 24px',
          '&.MuiButton-outlined': { padding: '9px 24px' }
        },
        sizeMedium: {
          height: 40,
          padding: '14px 24px',
          '&.MuiButton-outlined': { padding: '13px 24px' },
          [theme.breakpoints.down('sm')]: {
            padding: '10px 24px',
            '&.MuiButton-outlined': { padding: '9px 24px' }
          }
        },
        sizeLarge: {
          fontSize: 15,
          height: 46,
          padding: '20px 24px',
          '&.MuiButton-outlined': { padding: '19px 24px' },
          [theme.breakpoints.down('md')]: {
            padding: '14px 24px',
            '&.MuiButton-outlined': { padding: '13px 24px' }
          },
          [theme.breakpoints.down('sm')]: {
            padding: '10px 24px',
            '&.MuiButton-outlined': { padding: '9px 24px' }
          }
        }
      },
      variants: [
        {
          props: { variant: 'contained' },
          style: {
            backgroundColor: theme.palette.m3.primary,
            color: theme.palette.m3.onPrimary,
            boxShadow: 'none',
            '&:hover': {
              backgroundColor: blend(theme.palette.m3.primary, theme.palette.m3.onPrimary, 0.08),
              color: theme.palette.m3.onPrimary,
              // TO DO: check the MUI spec to implement this properly
              boxShadow: '0px 1px 2px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)',
            },
            // '&:focus': {
            //   backgroundColor: blend(theme.palette.m3.primary, theme.palette.m3.onPrimary, 0.12),
            //   color: theme.palette.m3.onPrimary
            // },
            '&:active': {
              boxShadow: 'none',
            },
            // TO DO: the colors are not mapping perfectly here
            '&:disabled': {
              backgroundColor: alpha(theme.palette.m3.onSurface, 0.12),
              color: alpha(theme.palette.m3.onSurface, 0.38)
            },
            '& .MuiTouchRipple-ripple, & .MuiTouchRipple-rippleVisible, & .MuiTouchRipple-child, & .MuiTouchRipple-childLeaving, & .MuiTouchRipple-childPulsate': {
              color: blend(theme.palette.m3.surfaceContainerLow, theme.palette.m3.primary, 0.48),
            },
          }
        },
        {
          props: { variant: 'outlined' },
          style: {
            backgroundColor: alpha(theme.palette.m3.main, 0.00), //transparent
            color: theme.palette.m3.primary,
            border: `2px solid ${theme.palette.m3.primary}`,
            '&:hover': {
              backgroundColor: alpha(theme.palette.m3.primary, 0.08),
              color: theme.palette.m3.primary
            },
            // '&:focus': {
            //   backgroundColor: alpha(theme.palette.m3.primary, 0.12),
            //   color: theme.palette.m3.primary
            // },
            '&:disabled': {
              color: alpha(theme.palette.m3.onSurface, 0.38),
              border: `2px solid ${alpha(theme.palette.m3.onSurface, 0.12)}`
            },
            '& .MuiTouchRipple-root': {
              '& .MuiTouchRipple-ripple, & .MuiTouchRipple-rippleVisible, & .MuiTouchRipple-child, & .MuiTouchRipple-childLeaving, & .MuiTouchRipple-childPulsate': {
                color: alpha(theme.palette.m3.primary, 0.24),
              },
            },
          }
        },
        {
          props: { variant: 'text' },
          style: {
            backgroundColor: 'none',
            color: theme.palette.m3.primary,
            '&:hover:not(:active)': {
              backgroundColor: blend(theme.palette.m3.onPrimary, theme.palette.m3.primary, 0.08),
              color: theme.palette.m3.primary
            },
            paddingLeft: '12px',
            paddingRight: '12px',
            // '&:focus': {
            //   backgroundColor: blend(theme.palette.m3.onPrimary, theme.palette.m3.primary, 0.12),
            //   color: theme.palette.m3.primary
            // },
            '&:disabled': {
              backgroundColor: 'none',
              color: alpha(theme.palette.m3.onSurface, 0.38),
            },
            '& .MuiTouchRipple-root': {
              '& .MuiTouchRipple-ripple, & .MuiTouchRipple-rippleVisible, & .MuiTouchRipple-child, & .MuiTouchRipple-childLeaving, & .MuiTouchRipple-childPulsate': {
                color: alpha(theme.palette.m3.primary, 0.48),
              },
            },
          }
        },
        {
          props: { variant: 'elevated' },
          style: {
            backgroundColor: theme.palette.m3.surfaceContainerLow,
            color: theme.palette.m3.primary,
            // TO DO: check the MUI spec to implement this properly
            boxShadow: '0px 1px 2px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)',
            '&:hover': {
              backgroundColor: blend(theme.palette.m3.surfaceContainerLow, theme.palette.m3.primary, 0.08),
              color: theme.palette.m3.primary,
              // TO DO: check the MUI spec to implement this properly
              // increase the box shadow on hover
              boxShadow: '0px 2px 3px rgba(0, 0, 0, 0.3), 0px 2px 4px 2px rgba(0, 0, 0, 0.15)',
            },
            // '&:focus': {
            //   backgroundColor: blend(theme.palette.m3.surfaceContainerLow, theme.palette.m3.primary, 0.12),
            //   color: theme.palette.m3.primary
            // },
            '&:active': {
              // TO DO: check the MUI spec to implement this properly
              // reduce the box shadow on active
              boxShadow: '0px 1px 2px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)'
              
            },
            '&:disabled': {
              backgroundColor: alpha(theme.palette.m3.onSurface, 0.12),
              color: alpha(theme.palette.m3.onSurface, 0.38),
              boxShadow: 'none'
            },
            '& .MuiTouchRipple-ripple, & .MuiTouchRipple-rippleVisible, & .MuiTouchRipple-child, & .MuiTouchRipple-childLeaving, & .MuiTouchRipple-childPulsate': {
              color: blend(theme.palette.m3.surfaceContainerLow, theme.palette.m3.primary, 0.48),
            },
          }
        },
        {
          props: { variant: 'tonal' },
          style: {
            backgroundColor: theme.palette.m3.secondaryContainer,
            color: theme.palette.m3.onSecondaryContainer,
            '&:hover:not(:active)': {
              backgroundColor: blend(theme.palette.m3.secondaryContainer, theme.palette.m3.onSecondaryContainer, 0.08),
              color: theme.palette.m3.onSecondaryContainer,
              // TO DO: check the MUI spec to implement this properly
              boxShadow: '0px 1px 2px rgba(0, 0, 0, 0.3), 0px 1px 3px 1px rgba(0, 0, 0, 0.15)',
            },
            // '&:focus': {
            //   backgroundColor: blend(theme.palette.m3.secondaryContainer, theme.palette.m3.onSecondaryContainer, 0.12),
            //   color: theme.palette.m3.onSecondaryContainer
            // },
            '&:disabled': {
              backgroundColor: alpha(theme.palette.m3.onSurface, 0.12),
              color: alpha(theme.palette.m3.onSurface, 0.38),
            },
            '& .MuiTouchRipple-ripple, & .MuiTouchRipple-rippleVisible, & .MuiTouchRipple-child, & .MuiTouchRipple-childLeaving, & .MuiTouchRipple-childPulsate': {
              color: blend(theme.palette.m3.secondaryContainer, theme.palette.m3.onSecondaryContainer, 0.48),
            },
          }
        },
      ]
    }
  };
}
