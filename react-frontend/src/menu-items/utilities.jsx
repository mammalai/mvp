import FormatColorTextIcon from '@mui/icons-material/FormatColorText';
import ColorLensIcon from '@mui/icons-material/ColorLens';
import TonalityIcon from '@mui/icons-material/Tonality';

// icons
const icons = {
  FormatColorTextIcon,
  ColorLensIcon,
  TonalityIcon
};

// ==============================|| MENU ITEMS - UTILITIES ||============================== //

const utilities = {
  id: 'utilities',
  title: 'Utilities',
  type: 'group',
  children: [
    {
      id: 'util-typography',
      title: 'Typography',
      type: 'item',
      url: '/typography',
      icon: icons.FormatColorTextIcon
    },
    {
      id: 'util-color',
      title: 'Color',
      type: 'item',
      url: '/color',
      icon: icons.ColorLensIcon
    },
    {
      id: 'util-shadow',
      title: 'Shadow',
      type: 'item',
      url: '/shadow',
      icon: icons.TonalityIcon
    }
  ]
};

export default utilities;
