import { setup, fromPromise, createActor, assign } from 'xstate';

export const contextMachine = setup({
  actors: {
    checkLocalStorageActor: fromPromise(async () => {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (localStorage.getItem('user') !== null) {
            resolve();
          } else {
            reject();
          }
        }, 2000);
      });
    }),
  },
  actions: {
    logoutAction: assign(() => {
      console.log('LOGOUT ACTION');
      // localStorage.removeItem('snapshot');
      return {
        accessToken: null,
      };
    }),
    assignAccessToken: assign(({ event }) => {
      return {
        accessToken: event.data.access_token,
      };
    }),
    assignResponseData: assign(({ event }) => {
      console.log('EVENTY', event);
      return {
        fetchResponseBody: event.output.data,
      };
    }),
  },
}).createMachine({
  id: 'context',
  context: {
    user: null,
    accessToken: null,
  },
  initial: 'UnAuthState',
  states: {
    AuthState: {
      on: {
        logout: {
          target: 'UnAuthState',
          actions: [{ type: 'logoutAction' }],
        },
      },
    },
    UnAuthState: {
      entry: () => console.log('HALLO'),
      on: {
        login: {
          target: 'AuthState',
          actions: ['assignAccessToken'],
        },
      },
    },
  },
});

const restoredState = JSON.parse(localStorage.getItem('contextMachine'));

export const machineActor = createActor(contextMachine, { snapshot: restoredState });

machineActor.subscribe((snapshot) => {
  console.log('snapshot', snapshot);
  const persistedState = machineActor.getPersistedSnapshot();
  localStorage.setItem('contextMachine', JSON.stringify(persistedState));
});
