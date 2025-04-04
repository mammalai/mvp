// ==============================|| DEFAULT THEME - TYPOGRAPHY ||============================== //

export default function Typography(fontFamily) {
  return {
    htmlFontSize: 16,
    fontFamily,
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
    fontWeightBold: 600,

    // display - large
    displayLarge: {
      fontWeight: 400,
      fontSize: '57px',
      lineHeight: '64px',
      letterSpacing: '-0.25px'
    },

    // display - medium
    displayMedium: {
      fontWeight: 400,
      fontSize: '45px',
      lineHeight: '52px',
      letterSpacing: '0px'
    },

    // display - small
    displaySmall: {
      fontWeight: 400,
      fontSize: '36px',
      lineHeight: '44px',
      letterSpacing: '0px'
    },

    // Heading - large
    headingLarge: {
      fontWeight: 400,
      fontSize: '32px',
      lineHeight: '40px',
      letterSpacing: '0px'
    },

    // Heading - medium
    headingMedium: {
      fontWeight: 400,
      fontSize: '28px',
      lineHeight: '36px',
      letterSpacing: '0px'
    },

    // Heading - small
    headingSmall: {
      fontWeight: 400,
      fontSize: '24px',
      lineHeight: '32px',
      letterSpacing: '0px'
    },

    // Title - large
    titleLarge: {
      fontWeight: 400,
      fontSize: '22px',
      lineHeight: '28px',
      letterSpacing: '0px'
    },

    // Title - Medium
    titleMedium: {
      fontWeight: 500,
      fontSize: '16px',
      lineHeight: '24px',
      letterSpacing: '0.15px'
    },

    // Title - Small
    titleSmall: {
      fontWeight: 500,
      fontSize: '14px',
      lineHeight: '20px',
      letterSpacing: '0.1px'
    },

    // Body - Large
    labelLarge: {
      fontWeight: 400,
      fontSize: '14px',
      lineHeight: '20px',
      letterSpacing: '0.1px'
    },

    // Body - Medium
    labelMedium: {
      fontWeight: 400,
      fontSize: '12px',
      lineHeight: '16px',
      letterSpacing: '0.5px'
    },

    // Body - Small
    labelSmall: {
      fontWeight: 400,
      fontSize: '11px',
      lineHeight: '16px',
      letterSpacing: '0.5px'
    },

    // Body large
    bodyLarge: {
      fontWeight: 400,
      fontSize: '16px',
      lineHeight: '24px',
      letterSpacing: '0.5px'
    },

    // Body medium
    bodyMedium: {
      fontWeight: 400,
      fontSize: '14px',
      lineHeight: '20px',
      letterSpacing: '0.25px'
    },

    // Body small
    bodySmall: {
      fontWeight: 400,
      fontSize: '12px',
      lineHeight: '16px',
      letterSpacing: '0.4px'
    },

    h1: {
      fontWeight: 600,
      fontSize: '2.375rem',
      lineHeight: 1.21
    },
    h2: {
      fontWeight: 600,
      fontSize: '1.875rem',
      lineHeight: 1.27
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.5rem',
      lineHeight: 1.33
    },
    h4: {
      fontWeight: 600,
      fontSize: '1.25rem',
      lineHeight: 1.4
    },
    h5: {
      fontWeight: 600,
      fontSize: '1rem',
      lineHeight: 1.5
    },
    h6: {
      fontWeight: 400,
      fontSize: '0.875rem',
      lineHeight: 1.57
    },
    caption: {
      fontWeight: 400,
      fontSize: '0.75rem',
      lineHeight: 1.66
    },
    body1: {
      fontSize: '0.875rem',
      lineHeight: 1.57
    },
    body2: {
      fontSize: '0.75rem',
      lineHeight: 1.66
    },
    subtitle1: {
      fontSize: '0.875rem',
      fontWeight: 600,
      lineHeight: 1.57
    },
    subtitle2: {
      fontSize: '0.75rem',
      fontWeight: 500,
      lineHeight: 1.66
    },
    overline: {
      lineHeight: 1.66
    },
    button: {
      textTransform: 'capitalize'
    }
  };
}
