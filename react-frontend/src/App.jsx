import { RouterProvider } from 'react-router-dom';

// project import
import router from 'routes';
import ThemeCustomization from 'themes';

import ScrollTop from 'components/ScrollTop';

import { MachineContext, contextMachine } from './context';
import { useMachine } from '@xstate/react';
import { useEffect } from 'react';

// ==============================|| APP - THEME, ROUTER, LOCAL ||============================== //

export default function App() {
  const [state, send, service] = useMachine(contextMachine);
  const machine = [state, send, service];

  useEffect(() => {
    console.log('FROM APP.JSX - YO MOFAKA');
    console.log('Machine state:', state);
  }, [state]);

  return (
    <MachineContext.Provider value={machine}>
      <ThemeCustomization>
        <ScrollTop>
          <RouterProvider router={router} />
        </ScrollTop>
      </ThemeCustomization>
    </MachineContext.Provider>
  );
}
