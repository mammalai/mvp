// ==============================|| OVERRIDES - TYPOGRAPHY ||============================== //

export default function typography(theme) {
  return {
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
    }

    // // heading - large
    // h1: {
    //   fontWeight: 400,
    //   fontSize: 57,

    //   // lineHeight = lineHeight in figma / fontSize. i.e 1.123 = 64/57
    //   lineHeight: 1.123,
    //   letterSpacing: -0.25,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 45,
    //     lineHeight: 1.156
    //   },
    //   [theme.breakpoints.down('sm')]: {
    //     fontSize: 32,
    //     lineHeight: 1.222
    //   }
    // },

    // // heading - medium
    // h2: {
    //   fontWeight: 400,
    //   fontSize: 45,
    //   lineHeight: 1.156,
    //   letterSpacing: 0,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 36,
    //     lineHeight: 1.222
    //   },
    //   [theme.breakpoints.down('sm')]: {
    //     fontSize: 24,
    //     lineHeight: 1.333
    //   }
    // },

    // // disaply - medium
    // h3: {
    //   fontWeight: 400,
    //   fontSize: 28,
    //   lineHeight: 1.286,
    //   letterSpacing: 0,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 24,
    //     lineHeight: 1.333
    //   },
    //   [theme.breakpoints.down('sm')]: {
    //     fontSize: 20,
    //     lineHeight: 1.4
    //   }
    // },

    // // disaply - small
    // h4: {
    //   fontWeight: 400,
    //   fontSize: 24,
    //   lineHeight: 1.333,
    //   letterSpacing: 0,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 20,
    //     lineHeight: 1.4
    //   },
    //   [theme.breakpoints.down('sm')]: {
    //     fontSize: 16,
    //     lineHeight: 1.5
    //   }
    // },

    // // label - large
    // h5: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 500,
    //   fontSize: 22,
    //   lineHeight: 1.273,
    //   letterSpacing: 0,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 16,
    //     lineHeight: 1.5,
    //     letterSpacing: 0.15
    //   }
    // },

    // // paragraph - large
    // h6: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 400,
    //   fontSize: 22,
    //   lineHeight: 1.364,
    //   letterSpacing: 0,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 16,
    //     lineHeight: 1.5,
    //     letterSpacing: 0.5
    //   }
    // },

    // // paragraph - medium
    // body1: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 400,
    //   fontSize: 16,
    //   lineHeight: 1.5,
    //   letterSpacing: 0.5,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 14,
    //     lineHeight: 1.429,
    //     letterSpacing: 0.25
    //   }
    // },

    // // paragraph - small
    // body2: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 400,
    //   fontSize: 14,
    //   lineHeight: 1.429,
    //   letterSpacing: 0.25,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 12,
    //     lineHeight: 1.5
    //   }
    // },

    // // label - medium
    // subtitle1: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 500,
    //   fontSize: 16,
    //   lineHeight: 1.5,
    //   letterSpacing: 0.15,
    //   [theme.breakpoints.down('md')]: {
    //     fontWeight: 600,
    //     fontSize: 14,
    //     lineHeight: 1.429,
    //     letterSpacing: 0.1
    //   }
    // },

    // // label - small
    // subtitle2: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 600,
    //   fontSize: 14,
    //   lineHeight: 1.429,
    //   letterSpacing: 0.1,
    //   [theme.breakpoints.down('md')]: {
    //     fontSize: 12,
    //     lineHeight: 1.5
    //   }
    // },

    // // hyperlink - small
    // caption: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 600,
    //   fontSize: 12,
    //   lineHeight: 1.333,
    //   letterSpacing: 0
    // },

    // // hyperlink - large
    // caption1: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 400,
    //   fontSize: 16,
    //   lineHeight: 1.5,
    //   letterSpacing: 0.5
    // },

    // // hyperlink - medium
    // caption2: {
    //   fontFamily: FONT_ROBOTO,
    //   fontWeight: 500,
    //   fontSize: 14,
    //   lineHeight: 1.429,
    //   letterSpacing: 0.1
    // },

    // // button
    // button: {
    //   textTransform: 'capitalize'
    // }
  };
}
