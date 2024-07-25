import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

// material-ui
import Button from '@mui/material/Button';
import FormHelperText from '@mui/material/FormHelperText';
import Grid from '@mui/material/Grid';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import LinearProgress from '@mui/material/LinearProgress';
import { useNavigate } from 'react-router-dom';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

// project import
import AnimateButton from 'components/@extended/AnimateButton';

// x-state
import { setup, fromPromise, assign } from 'xstate';
import { useMachine } from '@xstate/react';

// assets
import EyeOutlined from '@ant-design/icons/EyeOutlined';
import EyeInvisibleOutlined from '@ant-design/icons/EyeInvisibleOutlined';

// state
import { machineActor } from '../../../context';

const loginMachine = setup({
  actors: {
    loginRequest: fromPromise(async (args) => {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          axios
            .post('/api/auth/login', {
              email: args.input.context.loginCredentials.email,
              password: args.input.context.loginCredentials.password,
            })
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
        loginCredentials: {
          email: event.data.email,
          password: event.data.password,
        },
      };
    }),
    assignLoadinErrorMessage: assign(({ event }) => {
      const axiosError = event.error;
      if ('response' in axiosError && 'data' in axiosError.response && 'error' in axiosError.response.data) {
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
  /** @xstate-layout N4IgpgJg5mDOIC5QAoC2BDAxgCwJYDswBKAOlwgBswBlAF3VrAGIAzMWnAUQDcx9aA2gAYAuolAAHAPaxctXFPziQAD0QAmdQHYSADi3qhAZgCMugJwA2Y+aMBWADQgAnoiPmALCUuX1J9ebaWh52Rh4AvuFOaFh4hKQUUugQBFB0DMwQimBk+NxSANY5MTgExCSJyanpjAgE+ZgMCvjCIq3K0rLyispqCJa66npCJp7qHupGlh5a5k6uCAC0Jl5aunYG-kK6ppaeRpHRGKXxFUkp+Gn0jExgAE53UnckEhQMLE+oJCVx5ZUXVwydTyUka3RaonaSBAnTkzV6biE5hIo2MRmMIxWjhciEWRh0Wl8YV0ug8RimfnUhxAPzKpHujzuNWYbA42B4fEEog6MjhPWhfRMWjsJHMJPshNMoSmRnmiH8QxJA22dg2wo2kSiIHwUggcGUtPiPK68IFiDsJj0Rl0lncKpWxjlSz8yOtgQ8I3U1kGQks1MN5XIVGZxr5SjNCBMQi8Fp2qo2JOM6ydASEJCEdnMwqRmaFvv9x1+CXO1WuYFD4IRCA8ujTCq0JiMkxMJmmcxxCCsJC0BiE6nWQgbpmFBdidJIDKeIehsMrEfMyJ2Nrt6wdso7y1bJFV+PMdksdjJ7hWo5O5VgAFdMJg4LBp5JeXPQH09mmDD30epD9opk7lqY9AsSZ3Q8VsqU1IA */
  context: {
    loginCredentials: {
      email: '',
      password: '',
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

export default function AuthLogin() {
  const [state, send] = useMachine(loginMachine);

  // form validation hooks
  const [showInvalidError] = React.useState(false);
  const [isSub] = React.useState(false);

  // react-router navigate hook
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = React.useState(false);
  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleSubmit = (values) => {
    send({ type: 'fetchEvent', data: values });
  };

  useEffect(() => {
    if (state.value === 'successState') {
      machineActor.send({ type: 'login' });
      navigate('/');
    }
  }, [state]);

  return (
    <>
      <Formik
        initialValues={{
          email: 'salarsattiss@gmail.com',
          password: 'Stongassword12345!!',
          submit: null,
        }}
        validationSchema={Yup.object().shape({
          email: Yup.string().email('Must be a valid email').max(255).required('Email is required'),
          password: Yup.string().max(255).required('Password is required'),
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
              <Grid item xs={12}>
                <Stack spacing={1}>
                  <InputLabel htmlFor="password-login">Password</InputLabel>
                  <OutlinedInput
                    fullWidth
                    error={Boolean(touched.password && errors.password)}
                    id="-password-login"
                    type={showPassword ? 'text' : 'password'}
                    value={values.password}
                    name="password"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    endAdornment={
                      <InputAdornment position="end">
                        <IconButton
                          aria-label="toggle password visibility"
                          onClick={handleClickShowPassword}
                          onMouseDown={handleMouseDownPassword}
                          edge="end"
                          color="secondary"
                        >
                          {showPassword ? <EyeOutlined /> : <EyeInvisibleOutlined />}
                        </IconButton>
                      </InputAdornment>
                    }
                    placeholder="Enter password"
                  />
                </Stack>
                {touched.password && errors.password && (
                  <FormHelperText error id="standard-weight-helper-text-password-login">
                    {errors.password}
                  </FormHelperText>
                )}
              </Grid>
              <Grid item xs={12} sx={{ mt: -1 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="right" spacing={2}>
                  {/* <FormControlLabel
                    control={
                      <Checkbox
                        checked={checked}
                        onChange={(event) => setChecked(event.target.checked)}
                        name="checked"
                        color="primary"
                        size="small"
                      />
                    }
                    label={<Typography variant="h6">Keep me sign in</Typography>}
                  /> */}
                  <div></div>
                  <Typography
                    component={Link}
                    to="/forgot-password/request"
                    variant="body1"
                    sx={{ textDecoration: 'none' }}
                    color="primary"
                  >
                    Forgot password?
                  </Typography>
                </Stack>
              </Grid>
              {errors.submit && (
                <Grid item xs={12}>
                  <FormHelperText error>{errors.submit}</FormHelperText>
                </Grid>
              )}
              {showInvalidError ? (
                <Grid item xs={12}>
                  <Typography color="red">This email and password does not exist.</Typography>
                </Grid>
              ) : null}

              {state.value === 'errorState' ? (
                <Grid item xs={12}>
                  <Typography color="red">{state.context.errorMessage}</Typography>
                </Grid>
              ) : null}

              <Grid item xs={12}>
                <AnimateButton>
                  <Button disableElevation disabled={isSub} fullWidth size="large" type="submit" variant="contained" color="primary">
                    Login
                  </Button>
                </AnimateButton>
              </Grid>

              {/* <Grid item xs={12}>
                <Divider>
                  <Typography variant="caption"> Login with</Typography>
                </Divider>
              </Grid>
              <Grid item xs={12}>
                <FirebaseSocial />
              </Grid> */}

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
