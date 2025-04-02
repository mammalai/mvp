// ==============================|| OVERRIDES - TABS ||============================== //

export default function Tabs(theme) {
  return {
    MuiTabs: {
      styleOverrides: {
        root: {
          borderRadius: 38,
          borderColor: 'none',
          backgroundColor: theme.palette.m3.surface,
          // these two together remove the default height of the tabs and remove the indicator space
          '& .MuiTabs-indicator': {
            display: 'none'
          },
          minHeight: 'auto',
          '& .MuiTab-root': {
            padding: 28,
            borderRadius: 38
          }
        },
        vertical: {
          overflow: 'visible',
          '& .MuiTab-root': {
            padding: 18,
            borderRadius: 35
          }
        }
      }
    }
  };
}
