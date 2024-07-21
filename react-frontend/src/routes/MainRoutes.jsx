import { lazy, useContext, useEffect } from 'react';

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

import { MachineContext } from '../context';

const ProtectedRoutes = () => {
  /* eslint-disable */
  {
    /* 
  if (localStorage.getItem("token")) {
    return <Dashboard />;
  } 
  */
  }

  // localStorageToken = localStorage.getItem("token");
  // if (localStorageToken) {
  //   // send to machine
  // }
  // console.log("YO MOFAKA")
  const [state, send, service] = useContext(MachineContext);

  useEffect(() => {
    console.log('ROUTER: YO MOFAKA');
    console.log('Machine state:', state);
  }, [state]);

  // const localStorageToken = true; //localStorage.getItem("token");
  // return localStorageToken ? <Dashboard /> : <Navigate to="/login" replace />;

  // return (state.value === 'AuthState' ? <Dashboard /> : <Navigate to="/login" replace />);

  if (state.value === 'AuthState') {
    return <Dashboard />;
  } else {
    return <Navigate to="/login" replace />;
  }

  /* eslint-enable */
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
