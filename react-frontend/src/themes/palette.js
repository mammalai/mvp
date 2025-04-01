// material-ui
import { createTheme } from '@mui/material/styles';

// third-party
import { presetDarkPalettes, presetPalettes } from '@ant-design/colors';

// project imports
import ThemeOption from './theme';

// ==============================|| DEFAULT THEME - PALETTE ||============================== //

const M3Light = {
  "primary": "#68548E",
  "surfaceTint": "#68548E",
  "onPrimary": "#FFFFFF",
  "primaryContainer": "#EBDDFF",
  "onPrimaryContainer": "#230F46",
  "secondary": "#635B70",
  "onSecondary": "#FFFFFF",
  "secondaryContainer": "#E9DEF8",
  "onSecondaryContainer": "#1F182B",
  "tertiary": "#7E525D",
  "onTertiary": "#FFFFFF",
  "tertiaryContainer": "#FFD9E1",
  "onTertiaryContainer": "#31101B",
  "error": "#BA1A1A",
  "onError": "#FFFFFF",
  "errorContainer": "#FFDAD6",
  "onErrorContainer": "#410002",
  "background": "#FEF7FF",
  "onBackground": "#1D1B20",
  "surface": "#FEF7FF",
  "onSurface": "#1D1B20",
  "surfaceVariant": "#E7E0EB",
  "onSurfaceVariant": "#49454E",
  "outline": "#7A757F",
  "outlineVariant": "#CBC4CF",
  "shadow": "#000000",
  "scrim": "#000000",
  "inverseSurface": "#322F35",
  "inverseOnSurface": "#F5EFF7",
  "inversePrimary": "#D3BCFD",
  "primaryFixed": "#EBDDFF",
  "onPrimaryFixed": "#230F46",
  "primaryFixedDim": "#D3BCFD",
  "onPrimaryFixedVariant": "#4F3D74",
  "secondaryFixed": "#E9DEF8",
  "onSecondaryFixed": "#1F182B",
  "secondaryFixedDim": "#CDC2DB",
  "onSecondaryFixedVariant": "#4B4358",
  "tertiaryFixed": "#FFD9E1",
  "onTertiaryFixed": "#31101B",
  "tertiaryFixedDim": "#F0B7C5",
  "onTertiaryFixedVariant": "#643B46",
  "surfaceDim": "#DED8E0",
  "surfaceBright": "#FEF7FF",
  "surfaceContainerLowest": "#FFFFFF",
  "surfaceContainerLow": "#F8F1FA",
  "surfaceContainer": "#F2ECF4",
  "surfaceContainerHigh": "#EDE6EE",
  "surfaceContainerHighest": "#E7E0E8"
}

const M3Dark = {
  "primary": "#B6C4FF",
  "surfaceTint": "#B6C4FF",
  "onPrimary": "#1E2D61",
  "primaryContainer": "#354479",
  "onPrimaryContainer": "#DCE1FF",
  "secondary": "#C2C5DD",
  "onSecondary": "#2B3042",
  "secondaryContainer": "#424659",
  "onSecondaryContainer": "#DEE1F9",
  "tertiary": "#E3BADA",
  "onTertiary": "#43273F",
  "tertiaryContainer": "#5B3D57",
  "onTertiaryContainer": "#FFD7F5",
  "error": "#FFB4AB",
  "onError": "#690005",
  "errorContainer": "#93000A",
  "onErrorContainer": "#FFDAD6",
  "background": "#121318",
  "onBackground": "#E3E1E9",
  "surface": "#121318",
  "onSurface": "#E3E1E9",
  "surfaceVariant": "#45464F",
  "onSurfaceVariant": "#C6C5D0",
  "outline": "#90909A",
  "outlineVariant": "#45464F",
  "shadow": "#000000",
  "scrim": "#000000",
  "inverseSurface": "#E3E1E9",
  "inverseOnSurface": "#2F3036",
  "inversePrimary": "#4D5C92",
  "primaryFixed": "#DCE1FF",
  "onPrimaryFixed": "#04164B",
  "primaryFixedDim": "#B6C4FF",
  "onPrimaryFixedVariant": "#354479",
  "secondaryFixed": "#DEE1F9",
  "onSecondaryFixed": "#161B2C",
  "secondaryFixedDim": "#C2C5DD",
  "onSecondaryFixedVariant": "#424659",
  "tertiaryFixed": "#FFD7F5",
  "onTertiaryFixed": "#2C122A",
  "tertiaryFixedDim": "#E3BADA",
  "onTertiaryFixedVariant": "#5B3D57",
  "surfaceDim": "#121318",
  "surfaceBright": "#38393F",
  "surfaceContainerLowest": "#0D0E13",
  "surfaceContainerLow": "#1A1B21",
  "surfaceContainer": "#1E1F25",
  "surfaceContainerHigh": "#292A2F",
  "surfaceContainerHighest": "#34343A"
}

export default function Palette(mode, presetColor) {
  const colors = presetPalettes;

  let greyPrimary = [
    '#ffffff',
    '#fafafa',
    '#f5f5f5',
    '#f0f0f0',
    '#d9d9d9',
    '#bfbfbf',
    '#8c8c8c',
    '#595959',
    '#262626',
    '#141414',
    '#000000'
  ];
  let greyAscent = ['#fafafa', '#bfbfbf', '#434343', '#1f1f1f'];
  let greyConstant = ['#fafafb', '#e6ebf1'];

  colors.grey = [...greyPrimary, ...greyAscent, ...greyConstant];

  const paletteColor = ThemeOption(colors, presetColor, mode);

  if (mode === 'light') {
    return createTheme({
      palette: {
        m3: {
          main: M3Light.primary,
          ...M3Light,
        },
        mode,
        common: {
          black: '#000',
          white: '#fff',
        },
        ...paletteColor,
        text: {
          primary: paletteColor.grey[700],
          secondary: paletteColor.grey[500],
          disabled: paletteColor.grey[400],
        },
        action: {
          disabled: paletteColor.grey[300],
        },
        divider: paletteColor.grey[200],
        background: {
          paper: paletteColor.grey[0],
          default: paletteColor.grey.A50,
        },
      },
    });
  } else if (mode === 'dark') { 
    return createTheme({
      palette: {
        ...M3Dark,
        mode,
        common: {
          black: '#000',
          white: '#fff',
        },
        ...paletteColor,
        text: {
          primary: paletteColor.grey[700],
          secondary: paletteColor.grey[500],
          disabled: paletteColor.grey[400],
        },
        action: {
          disabled: paletteColor.grey[300],
        },
        divider: paletteColor.grey[200],
        background: {
          paper: paletteColor.grey[0],
          default: paletteColor.grey.A50,
        },
      },
    });
  }
}
