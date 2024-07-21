// import { setup, fromPromise, assign } from 'xstate';
// import axios from 'axios';

// // import { useMachine } from '@xstate/react';

// const AuthMachine = setup({
//   actors: {
//     loginRequest: fromPromise(async (args) => {
//       return new Promise((resolve, reject) => {
//         setTimeout(() => {
//           axios
//             .post('/api/auth/login', {
//               email: args.input.context.loginCredentials.email,
//               password: args.input.context.loginCredentials.password,
//             })
//             .then((response) => {
//               resolve(response);
//             })
//             .catch((error) => {
//               reject(error);
//             });
//         }, 2000);
//       });
//     }),
//   },
//   actions: {
//     assignFromFetchToContext: assign(({ event }) => {
//       // event.output contains the output of the loadTodos function
//       // return a partial dictionary of the context will update the context
//       return {
//         loginCredentials: {
//           email: event.data.email,
//           password: event.data.password,
//         },
//       };
//     }),
//     assignLoadinErrorMessage: assign(({ event }) => {
//       const axiosError = event.error;
//       if ('response' in axiosError && 'data' in axiosError.response && 'error' in axiosError.response.data) {
//         return {
//           errorMessage: axiosError.response.data.error,
//         };
//       } else {
//         return {
//           errorMessage: 'An unknown error occured. Please try again later',
//         };
//       }
//     }),
//   },
// }).createMachine({
//   /** @xstate-layout N4IgpgJg5mDOIC5QAoC2BDAxgCwJYDswBKAOgGFsxMBrAFQHtqx8BlAF3TbAGIJ7CSBAG6MwJNFjyFSFKnVGsOXBMPqZOufgG0ADAF1dexKAAO9WLjab8xkAA9EAWgCMAFgBsJAJwBmZwCYvL3cAnR93AHYADgAaEABPRH8SKOiI91cff38AVgj-CK8cnIBfEriJHAJickoaBiZFTh4wACdW+laSEwAbTgAzTtRxDCrpWrkG5nZmlXwRdSttfUNbMwslmyR7Jxz-HRIdHJ9XHOcc9zznKNc4xIQTiJJXIJ0InSLcqPcvMvKQfD0CBwWyVKTENbmSzWWwOBCOC5RQ7HU7nS4Ra63BJOG4kdz+AK5H4+KIfCI+MoVUbgmR1eSNGZcSEbGHbOGOVz5EiBVw6QLBXJvZx3RDuA4+Xwk5wRF4nZwU-5g6qkACq+AAggBXNiUfBWRaQRlgZnQ-iwpyBZLOdzfMLON5nLwihDFZwpHJeXlRHKuKJ+H6UkBK8ZanXMfXNCBGk2bc0IZyekgejGpHwXCUJrH3a1IrxRfYeNyuAvOP4lIA */
//   context: {
//     loginCredentials: {
//       email: '',
//       password: '',
//     },
//     errorMessage: '',
//   },
//   initial: 'CheckTokenState',
//   states: {
//     CheckTokenState: {
//       invoke: {
//         src: 'validateTokenRequest',
//         input: ({ context }) => ({ context }),
//         onDone: {
//           target: 'AuthenticatedState',
//           actions: [],
//         },
//         onError: {
//           target: 'UnAuthenticatedState',
//           actions: ['assignLoadinErrorMessage'],
//         },
//       },
//     },
//     // Check token passed - delete the token and user data - send to login page
//     UnAuthenticatedState: {},
//     // Check token passed - set storage with the user data - send to home page
//     AuthenticatedState: {},
//   },
// });

// export default AuthMachine;

import React from 'react';
import { setup, fromPromise } from 'xstate';

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
      on: {
        login: 'AuthState',
      },
    },
  },
});

export const MachineContext = React.createContext(null);
