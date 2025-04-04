// ==============================|| OVERRIDES - CARD CONTENT ||============================== //

export default function CardContent(theme) {
  return {
    MuiCardContent: {
      styleOverrides: {
        root: {
          padding: 20,
          '&:last-child': {
            paddingBottom: 20
          },
          '&:MuiTypography-root': {
            color: theme.palette.m3.onSurfaceVariant
          }
        }
      }
    }
  };
}
