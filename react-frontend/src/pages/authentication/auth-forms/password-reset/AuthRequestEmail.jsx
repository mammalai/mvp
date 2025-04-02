import PropTypes from 'prop-types';
import React from 'react';
import axios from 'axios';

// material-ui
import Button from '@mui/material/Button';
import FormHelperText from '@mui/material/FormHelperText';
import Grid from '@mui/material/Grid';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import LinearProgress from '@mui/material/LinearProgress';
import Alert from '@mui/material/Alert';

// ant design icons
import CheckOutlined from '@ant-design/icons/CheckOutlined';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

// project import
import AnimateButton from 'components/@extended/AnimateButton';

// x-state
import { setup, fromPromise, assign } from 'xstate';
import { useMachine } from '@xstate/react';

const loginMachine = setup({
  actors: {
    loginRequest: fromPromise(async (args) => {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          axios
            .post('/api/auth/password/reset', {
              email: args.input.context.userIdentity.email
            })
            .then((response) => {
              resolve(response);
            })
            .catch((error) => {
              reject(error);
            });
        }, 2000);
      });
    })
  },
  actions: {
    assignFromFetchToContext: assign(({ event }) => {
      // event.output contains the output of the loadTodos function
      // return a partial dictionary of the context will update the context
      return {
        userIdentity: {
          email: event.data.email
        }
      };
    }),
    assignLoadingErrorMessage: assign(({ event }) => {
      const axiosError = event.error;
      if (
        'response' in axiosError &&
        'data' in axiosError.response &&
        typeof axiosError.response.data === 'object' && // check if data is an object
        'error' in axiosError.response.data
      ) {
        return {
          errorMessage: axiosError.response.data.error
        };
      } else {
        return {
          errorMessage: 'An unknown error occured. Please try again later'
        };
      }
    })
  }
}).createMachine({
  /** @xstate-layout N4IgpgJg5mDOIC5QAoC2BDAxgCwJYDswBKAOlwgBswBlAF3VrAGIAzMWnAUQDcx9aA2gAYAuolAAHAPaxctXFPziQAD0QBGAKyaSATiH79AJiPqhAZiFGANCACeiI0IAseoQDYjm55t0AOdXU-XU0AX1DbNCw8QlIKKXQIAig6BmYIRTAyfG4pAGssqJwCYhJ4xOTUxgQCXMwGBXxhEWblaVl5RWU1BE8ddWc-Z10Adm0RkZN1WwcEU10Scz8jPwNNcwGhIZHwyIxi2LKEpPwU+kYmMAAnK6krkgkKBhY71BIimNLyk7O0mpypPVOk1RK0kCB2nJGt1EO51AtzLo4YiRuY0atpvZEBsjCQXEZRpNUepUUjdiAPiVSNdblcqsw2BxsDw+IJRG0ZFCuuCes4rCQ4ZNEashC5NDNEINXMsQrp1EtPEJ4TtyfgpBA4MpKbEOR1oTzEABaIyuILrEYBIyI7S6CUIQIjEh8vqWTSTQXk7WlchUem6rlKA1zcwkALOTxBEbuFzOTGzE1+EjeTTwoQTELONHuT37T5xY6Vc5gf3AmEIWMh9wjeGmEa6QZDIZ22uh3xLczuYLrExGHPRKkkGl3P3gyGloN+Mah6PmcbuTQWTR+O0d9QkKOaaP18zOTNu7MRCm5gewACumEwcFgI8knPHoB6AUTs90iPcaLdpnczdjizbFuCeUhE3PxwnCIA */
  context: {
    userIdentity: {
      email: ''
    },
    errorMessage: ''
  },
  initial: 'idleState',
  states: {
    idleState: {
      on: {
        fetchEvent: {
          target: 'loadingState',
          actions: ['assignFromFetchToContext']
        }
      }
    },
    loadingState: {
      invoke: {
        src: 'loginRequest',
        input: ({ context }) => ({ context }),
        onDone: {
          target: 'successState',
          actions: []
        },
        onError: {
          target: 'errorState',
          actions: ['assignLoadingErrorMessage']
        }
      }
    },
    errorState: {
      on: {
        fetchEvent: {
          target: 'loadingState',
          actions: ['assignFromFetchToContext']
        }
      }
    },
    successState: {}
  }
});

// ============================|| JWT - LOGIN ||============================ //

export default function AuthLogin() {
  const [state, send] = useMachine(loginMachine);

  const handleSubmit = (values) => {
    send({ type: 'fetchEvent', data: values });
  };

  return (
    <>
      <Formik
        initialValues={{
          email: '',
          submit: null
        }}
        validationSchema={Yup.object().shape({
          email: Yup.string().email('Must be a valid email').max(255).required('Email is required')
        })}
        onSubmit={handleSubmit}
      >
        {({ errors, handleBlur, handleChange, handleSubmit, touched, values }) => (
          <form noValidate onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Stack spacing={1}>
                  <InputLabel htmlFor="email-login">Email Address</InputLabel>
                  <OutlinedInput
                    id="email-login"
                    type="email"
                    value={values.email}
                    name="email"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    placeholder="Enter email address"
                    fullWidth
                    error={Boolean(touched.email && errors.email)}
                  />
                </Stack>
                {touched.email && errors.email && (
                  <FormHelperText error id="standard-weight-helper-text-email-login">
                    {errors.email}
                  </FormHelperText>
                )}
              </Grid>
              {errors.submit && (
                <Grid item xs={12}>
                  <FormHelperText error>{errors.submit}</FormHelperText>
                </Grid>
              )}

              {state.value === 'errorState' ? (
                <Grid item xs={12}>
                  <Typography color="red">{state.context.errorMessage}</Typography>
                </Grid>
              ) : null}

              {state.value === 'successState' ? (
                <Grid item xs={12}>
                  <Alert icon={<CheckOutlined fontSize="inherit" />} severity="success">
                    If the email address has an account, an email will be sent with a link to reset your password.
                  </Alert>
                </Grid>
              ) : (
                <Grid item xs={12}>
                  <AnimateButton>
                    <Button
                      disableElevation
                      disabled={state.value === 'loadingState'}
                      fullWidth
                      size="large"
                      type="submit"
                      variant="contained"
                      color="primary"
                    >
                      Reset Password
                    </Button>
                  </AnimateButton>
                </Grid>
              )}

              {state.value === 'loadingState' ? (
                <Grid item xs={12}>
                  <LinearProgress />
                </Grid>
              ) : null}
            </Grid>
          </form>
        )}
      </Formik>
    </>
  );
}

AuthLogin.propTypes = { isDemo: PropTypes.bool };
