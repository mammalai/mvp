import { lazy } from 'react';
import { Navigate } from 'react-router-dom';

// project import
import Loadable from 'components/Loadable';
import Dashboard from 'layout/Dashboard';

const Color = Loadable(lazy(() => import('pages/component-overview/color')));
const Typography = Loadable(lazy(() => import('pages/component-overview/typography')));
const Shadow = Loadable(lazy(() => import('pages/component-overview/shadows')));
const DashboardDefault = Loadable(lazy(() => import('pages/dashboard/default')));
const ComponentOverview = Loadable(lazy(() => import('pages/component-overview/default')));
const NotFound = Loadable(lazy(() => import('pages/404/default')));
// render - sample page
const SamplePage = Loadable(lazy(() => import('pages/extra-pages/sample-page')));
// ==============================|| MAIN ROUTING ||============================== //


const DefaultHome = () => {

  return <Navigate to="dashboard/default/" replace />;
  
};

const OpenRoutes = {
  path: '/',
  element: <Dashboard />,
  children: [
    {
      path: '/',
      element: <DefaultHome />,
    },
    {
      path: 'component-overview',
      element: <ComponentOverview />,
    },
    {
      path: '404',
      element: <NotFound />,
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

export default OpenRoutes;
