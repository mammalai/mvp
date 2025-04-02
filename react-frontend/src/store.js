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
    })
  },
  actions: {
    logoutAction: assign(() => {
      // on logout we will simply remove the access token
      return {
        accessToken: null
      };
    }),
    assignAccessToken: assign(({ event }) => {
      return {
        accessToken: event.data.access_token
      };
    }),
    assignResponseData: assign(({ event }) => {
      return {
        fetchResponseBody: event.output.data
      };
    })
  }
}).createMachine({
  id: 'context',
  context: {
    user: null,
    accessToken: null
  },
  initial: 'UnAuthState',
  states: {
    AuthState: {
      on: {
        logout: {
          target: 'UnAuthState',
          actions: [{ type: 'logoutAction' }]
        }
      }
    },
    UnAuthState: {
      on: {
        login: {
          target: 'AuthState',
          actions: ['assignAccessToken']
        }
      }
    }
  }
});

const restoredState = JSON.parse(localStorage.getItem('contextMachine'));

export const machineActor = createActor(contextMachine, { snapshot: restoredState });

machineActor.subscribe((snapshot) => {
  const persistedState = machineActor.getPersistedSnapshot();
  localStorage.setItem('contextMachine', JSON.stringify(persistedState));
});
