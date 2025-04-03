// assets
import NoteIcon from '@mui/icons-material/Note';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';

// icons
const icons = {
  NoteIcon,
  QuestionMarkIcon
};

// ==============================|| MENU ITEMS - SAMPLE PAGE & DOCUMENTATION ||============================== //

const support = {
  id: 'support',
  title: 'Support',
  type: 'group',
  children: [
    {
      id: 'sample-page',
      title: 'Sample Page',
      type: 'item',
      url: '/sample-page',
      icon: icons.NoteIcon
    },
    {
      id: 'documentation',
      title: 'Documentation',
      type: 'item',
      url: 'https://codedthemes.gitbook.io/mantis/',
      icon: icons.QuestionMarkIcon,
      external: true,
      target: true
    }
  ]
};

export default support;
