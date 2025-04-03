import { lazy } from 'react';

// project import
import Loadable from 'components/Loadable';
import AuthLayout from 'layout/Auth';

// render - login
const AuthLogin = Loadable(lazy(() => import('pages/authentication/login')));
const AuthRegister = Loadable(lazy(() => import('pages/authentication/register')));
const AuthRegisterVerify = Loadable(lazy(() => import('pages/authentication/register-verify')));
const AuthRequestEmail = Loadable(lazy(() => import('pages/authentication/password-reset/request-email')));
const AuthNewPassword = Loadable(lazy(() => import('pages/authentication/password-reset/new-password')));
// ==============================|| AUTH ROUTING ||============================== //

const LoginRoutes = {
  path: '/',
  element: <AuthLayout />,
  children: [
    {
      path: '/login',
      element: <AuthLogin />
    },
    {
      path: '/register',
      element: <AuthRegister />
    },
    {
      path: '/register-verify',
      element: <AuthRegisterVerify />
    },
    {
      path: '/password-reset/request',
      element: <AuthRequestEmail />
    },
    {
      path: '/password-reset/password',
      element: <AuthNewPassword />
    }
  ]
};

export default LoginRoutes;
