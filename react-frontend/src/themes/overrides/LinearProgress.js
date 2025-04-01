// ==============================|| OVERRIDES - LINER PROGRESS ||============================== //


export default function LinearProgress(theme) {

  return {
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          height: 6,
          borderRadius: 100,
          backgroundColor: theme.palette.m3.surfaceVariant,
        },
        bar: {
          borderRadius: 100,
          backgroundColor: theme.palette.m3.primary,
        },
      }
    }
  };
}
