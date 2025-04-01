// assets
import LoginIcon from '@mui/icons-material/Login';
import PasswordIcon from '@mui/icons-material/Password';

// icons
const icons = {
  LoginIcon,
  PasswordIcon
};

// ==============================|| MENU ITEMS - EXTRA PAGES ||============================== //

const pages = {
  id: 'authentication',
  title: 'Authentication',
  type: 'group',
  children: [
    {
      id: 'login1',
      title: 'Login',
      type: 'item',
      url: '/login',
      icon: icons.LoginIcon,
      target: true,
    },
    {
      id: 'register1',
      title: 'Register',
      type: 'item',
      url: '/register',
      icon: icons.LoginIcon,
      target: true,
    },
    {
      id: 'register-verify-1',
      title: 'Register Verify',
      type: 'item',
      url: '/register-verify',
      icon: icons.LoginIcon,
      target: true,
    },
    {
      id: 'passwordreset-request-1',
      title: 'Password Reset Request',
      type: 'item',
      url: '/password-reset/request',
      icon: icons.PasswordIcon,
      target: true,
    },
    {
      id: 'passwordreset-password-1',
      title: 'Password Reset Verify',
      type: 'item',
      url: '/password-reset/password',
      icon: icons.PasswordIcon,
      target: true,
    },
  ],
};

export default pages;
