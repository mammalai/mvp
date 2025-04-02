import { createBrowserRouter } from 'react-router-dom';
import { Navigate } from 'react-router-dom';
// project import
import ProtectedRoutes from './ProtectedRoutes';
import LoginRoutes from './LoginRoutes';
import OpenRoutes from './OpenRoutes';
import AuthLayout from 'layout/Auth';
import NotFound from 'pages/404/default';

// ==============================|| ROUTING RENDER ||============================== //

// const router = createBrowserRouter([MainRoutes, LoginRoutes], { basename: import.meta.env.VITE_APP_BASE_NAME });
const router = createBrowserRouter(
  [
    OpenRoutes,
    LoginRoutes,
    ProtectedRoutes,
    {
      path: '*',
      // element: <Navigate to="/404" replace />,
      element: <NotFound />
      // element: <div>NOT FOUND</div>
    }
  ],
  { basename: import.meta.env.VITE_APP_BASE_NAME }
);

export default router;
