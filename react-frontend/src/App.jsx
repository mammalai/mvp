import { RouterProvider } from 'react-router-dom';

// project import
import router from 'routes';
import ThemeCustomization from 'themes';

import ScrollTop from 'components/ScrollTop';

import { machineActor, SomeMachineContext } from './context';
// import { useActor } from '@xstate/react';
// import { useEffect } from 'react';

// ==============================|| APP - THEME, ROUTER, LOCAL ||============================== //

export default function App() {
  // const [state, send, service] = useActor(machineActor);
  // const machine = [state, send, service];

  // useEffect(() => {
  //   console.log('FROM APP.JSX - YO MOFAKA');
  //   console.log('Machine state:', state);
  // }, [state]);

  machineActor.start();

  return (
    <SomeMachineContext.Provider value={machineActor}>
      <ThemeCustomization>
        <ScrollTop>
          <RouterProvider router={router} />
        </ScrollTop>
      </ThemeCustomization>
    </SomeMachineContext.Provider>
  );
}
