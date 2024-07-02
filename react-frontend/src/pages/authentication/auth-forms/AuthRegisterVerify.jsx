import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';

// material-ui
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import LinearProgress from '@mui/material/LinearProgress';
import Alert from '@mui/material/Alert';

// ant design icons
import CheckOutlined from '@ant-design/icons/CheckOutlined';

// x-state
import { setup, fromPromise, assign } from 'xstate';
import { useMachine } from '@xstate/react';

const loginMachine = setup({
  actors: {
    loginRequest: fromPromise(async (args) => {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          axios
            .post(
              '/api/auth/verification',
              {},
              {
                params: {
                  token: args.input.context.requestData.token,
                },
              },
            )
            .then((response) => {
              resolve(response);
            })
            .catch((error) => {
              reject(error);
            });
        }, 2000);
      });
    }),
  },
  actions: {
    assignFromFetchToContext: assign(({ event }) => {
      // event.output contains the output of the loadTodos function
      // return a partial dictionary of the context will update the context
      return {
        requestData: {
          token: event.data.token,
        },
      };
    }),
    assignLoadinErrorMessage: assign(({ event }) => {
      const axiosError = event.error;
      if (
        'response' in axiosError &&
        'data' in axiosError.response &&
        typeof axiosError.response.data === 'object' && // check if data is an object
        'error' in axiosError.response.data
      ) {
        return {
          errorMessage: axiosError.response.data.error,
        };
      } else {
        return {
          errorMessage: 'An unknown error occured. Please try again later',
        };
      }
    }),
  },
}).createMachine({
  /** @xstate-layout N4IgpgJg5mDOIC5QAoC2BDAxgCwJYDswBKAOlwgBswBlAF3VrAGIAzMWnAUQDcx9aA2gAYAuolAAHAPaxctXFPziQAD0QBGAKyaSATiH79AJiPqhAZiFGANCACeiI0IAseoQDYjm55t0AOdXU-XU0AX1DbNCw8QlIKKXQIAig6BmYIRTAyfG4pAGssqJwCYhJ4xOTUxgQCXMwGBXxhEWblaVl5RWU1BE8ddWc-Z10Adm0RkZN1WwcEU10Scz8jPwNNcwGhIZHwyIxi2LKEpPwU+kYmMAAnK6krkgkKBhY71BIimNLyk7O0mpypPVOk1RK0kCB2nJGt1EO51AtzLo4YiRuY0atpvZEBsjCQXEZRpNUepUUjdiAPiVSNdblcqsw2BxsDw+IJRG0ZFCuuCes4rCQ4ZNEashC5NDNEINXMsQrp1EtPEJ4TtyfgpBA4MpKbEOR1oTzEABaIyuILrEYBIyI7S6CUIQIjEh8vqWTSTQXk7WlchUem6rlKA1zcwkALOTxBEbuFzOTGzE1+EjeTTwoQTELONHuT37T5xY6Vc5gf3AmEIWMh9wjeGmEa6QZDIZ22uh3xLczuYLrExGHPRKkkGl3P3gyGloN+Mah6PmcbuTQWTR+O0d9QkKOaaP18zOTNu7MRCm5gewACumEwcFgI8knPHoB6AUTs90iPcaLdpnczdjizbFuCeUhE3PxwnCIA */
  context: {
    requestData: {
      token: '',
    },
    errorMessage: '',
  },
  initial: 'idleState',
  states: {
    idleState: {
      on: {
        fetchEvent: {
          target: 'loadingState',
          actions: ['assignFromFetchToContext'],
        },
      },
    },
    loadingState: {
      invoke: {
        src: 'loginRequest',
        input: ({ context }) => ({ context }),
        onDone: {
          target: 'successState',
          actions: [],
        },
        onError: {
          target: 'errorState',
          actions: ['assignLoadinErrorMessage'],
        },
      },
    },
    errorState: {
      on: {
        fetchEvent: {
          target: 'loadingState',
          actions: ['assignFromFetchToContext'],
        },
      },
    },
    successState: {},
  },
});

// ============================|| JWT - LOGIN ||============================ //

export default function AuthRegisterVerify() {
  const [state, send] = useMachine(loginMachine);

  const [searchParams] = useSearchParams();

  useEffect(() => {
    const values = { token: searchParams.get('token') };
    send({ type: 'fetchEvent', data: values });
  }, []);

  return (
    <Grid container spacing={3}>
      {state.value === 'errorState' ? (
        <Grid item xs={12}>
          <Typography color="red">{state.context.errorMessage}</Typography>
        </Grid>
      ) : null}

      {state.value === 'successState' ? (
        <Grid item xs={12}>
          <Alert icon={<CheckOutlined fontSize="inherit" />} severity="success">
            You&apos;re account has been successfully verified.
          </Alert>
        </Grid>
      ) : null}

      {state.value === 'loadingState' ? (
        <Grid item xs={12}>
          <LinearProgress />
        </Grid>
      ) : null}
    </Grid>
  );
}

AuthRegisterVerify.propTypes = { isDemo: PropTypes.bool };
