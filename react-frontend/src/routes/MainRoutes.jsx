import { lazy } from 'react';

// project import
import Loadable from 'components/Loadable';
import Dashboard from 'layout/Dashboard';

const Color = Loadable(lazy(() => import('pages/component-overview/color')));
const Typography = Loadable(lazy(() => import('pages/component-overview/typography')));
const Shadow = Loadable(lazy(() => import('pages/component-overview/shadows')));
const DashboardDefault = Loadable(lazy(() => import('pages/dashboard/index')));

// render - sample page
const SamplePage = Loadable(lazy(() => import('pages/extra-pages/sample-page')));
// ==============================|| MAIN ROUTING ||============================== //

import { Navigate } from 'react-router-dom';
import { machineActor } from '../context';

const ProtectedRoutes = () => {
  if (machineActor.getSnapshot().matches('AuthState')) {
    return <Dashboard />;
  } else {
    return <Navigate to="/login" replace />;
  }
};

const MainRoutes = {
  path: '/',
  element: <ProtectedRoutes />,
  children: [
    {
      path: '/',
      element: <DashboardDefault />,
    },
    {
      path: 'color',
      element: <Color />,
    },
    {
      path: 'dashboard',
      children: [
        {
          path: 'default',
          element: <DashboardDefault />,
        },
      ],
    },
    {
      path: 'sample-page',
      element: <SamplePage />,
    },
    {
      path: 'shadow',
      element: <Shadow />,
    },
    {
      path: 'typography',
      element: <Typography />,
    },
  ],
};

export default MainRoutes;
