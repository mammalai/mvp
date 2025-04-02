import { lazy } from 'react';

// project import
import Loadable from 'components/Loadable';
import Dashboard from 'layout/Dashboard';

const Typography = Loadable(lazy(() => import('pages/component-overview/typography')));

// render - sample page
// ==============================|| MAIN ROUTING ||============================== //

import { Navigate } from 'react-router-dom';
import { machineActor } from '../store';

import { useSelector } from '@xstate/react';

const ProtectedRoutes = () => {
  const machineActorState = useSelector(machineActor, (snapshot) => snapshot.value);

  if (machineActorState === 'AuthState') {
    return <Dashboard />;
  } else {
    return <Navigate to="/login" replace />;
  }
};

const ProtectedRoutesSet = {
  path: '/',
  element: <ProtectedRoutes />,
  children: [
    // an example of how to add a protected route
    // {
    //   path: '/typography',
    //   element: <Typography />,
    // },
  ]
};

export default ProtectedRoutesSet;
