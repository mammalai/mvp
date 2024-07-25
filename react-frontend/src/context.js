import { setup, fromPromise, createActor } from 'xstate';

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
    logoutAction: () => {
      console.log('removing item');
      localStorage.removeItem('user');
    },
  },
}).createMachine({
  id: 'context',
  context: {
    user: null,
  },
  initial: 'UnAuthState',
  states: {
    // CheckLocalStorageTokenState: {
    //   invoke: {
    //     src: 'loginRequest',
    //     input: ({ context }) => ({ context }),
    //     onDone: {
    //       target: 'AuthState',
    //       actions: [],
    //     },
    //     onError: {
    //       target: 'UnAuthState',
    //       actions: [],
    //     },
    //   },
    // },
    AuthState: {
      on: {
        logout: 'UnAuthState',
        actions: [{ type: 'logoutAction' }],
      },
    },
    UnAuthState: {
      entry: () => console.log('HALLO'),
      on: {
        login: 'AuthState',
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
