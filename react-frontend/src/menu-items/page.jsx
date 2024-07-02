// assets
import { LoginOutlined, ProfileOutlined } from '@ant-design/icons';

// icons
const icons = {
  LoginOutlined,
  ProfileOutlined,
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
      icon: icons.LoginOutlined,
      target: true,
    },
    {
      id: 'register1',
      title: 'Register',
      type: 'item',
      url: '/register',
      icon: icons.ProfileOutlined,
      target: true,
    },
    {
      id: 'register-verify-1',
      title: 'Register',
      type: 'item',
      url: '/register-verify',
      icon: icons.ProfileOutlined,
      target: true,
    },
    {
      id: 'passwordreset-request-1',
      title: 'Password Reset',
      type: 'item',
      url: '/password-reset/request',
      icon: icons.ProfileOutlined,
      target: true,
    },
    {
      id: 'passwordreset-password-1',
      title: 'Password Reset',
      type: 'item',
      url: '/password-reset/password',
      icon: icons.ProfileOutlined,
      target: true,
    },
  ],
};

export default pages;
