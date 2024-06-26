import PropTypes from 'prop-types';
import React, { useEffect } from 'react';
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
    consoleLogFetch: ({ event }) => {
      console.log('Action to print fetch event');
      console.log(event);
      // console.log(event.output)
    },
    assignFromFetchToContext: assign(({ event }) => {
      console.log('Function to print and assign username and password');
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
      console.log('ASSIGN LOADING ERROR');
      const axiosError = event.error;
      if ('response' in axiosError && 'data' in axiosError.response && 'error' in axiosError.response.data) {
        console.log('ASSIGNING BAKCEND MESSAGE');
        console.log(axiosError.response.data.error);
        return {
          errorMessage: axiosError.response.data.error,
        };
      } else {
        console.log('ASSIGNING UNKNOWN ERROR');
        return {
          errorMessage: 'An unknown error occured. Please try again later',
        };
      }
    }),
    consoleLogLoading: ({ context, event }) => {
      console.log('Action to print loading');
      console.log(context);
      console.log(event);
    },
  },
}).createMachine({
  /** @xstate-layout N4IgpgJg5mDOIC5QAoC2BDAxgCwJYDswBKAOlwgBswBlAF3VrAGIAzMWnAUQDcx9aA2gAYAuolAAHAPaxctXFPziQAD0QBGAKyaSATiH79AJiPqhAZiFGANCACeiI0IAseoQDYjm55t0AOdXU-XU0AX1DbNCw8QlIKKXQIAig6BmYIRTAyfG4pAGssqJwCYhJ4xOTUxgQCXMwGBXxhEWblaVl5RWU1BE8ddWc-Z10Adm0RkZN1WwcEU10Scz8jPwNNcwGhIZHwyIxi2LKEpPwU+kYmMAAnK6krkgkKBhY71BIimNLyk7O0mpypPVOk1RK0kCB2nJGt1EO51AtzLo4YiRuY0atpvZEBsjCQXEZRpNUepUUjdiAPiVSNdblcqsw2BxsDw+IJRG0ZFCuuCes4rCQ4ZNEashC5NDNEINXMsQrp1EtPEJ4TtyfgpBA4MpKbEOR1oTzEABaIyuILrEYBIyI7S6CUIQIjEh8vqWTSTQXk7WlchUem6rlKA1zcwkALOTxBEbuFzOTGzE1+EjeTTwoQTELONHuT37T5xY6Vc5gf3AmEIWMh9wjeGmEa6QZDIZ22uh3xLczuYLrExGHPRKkkGl3P3gyGloN+Mah6PmcbuTQWTR+O0d9QkKOaaP18zOTNu7MRCm5gewACumEwcFgI8knPHoB6AUTs90iPcaLdpnczdjizbFuCeUhE3PxwnCIA */
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
          actions: ['consoleLogFetch', 'assignFromFetchToContext'],
        },
      },
    },
    loadingState: {
      invoke: {
        src: 'loginRequest',
        input: ({ context }) => ({ context }),
        onDone: {
          target: 'successState',
          actions: ['consoleLogLoading'],
        },
        onError: {
          target: 'errorState',
          actions: ['consoleLogLoading', 'assignLoadinErrorMessage'],
        },
      },
    },
    errorState: {
      on: {
        fetchEvent: {
          target: 'loadingState',
          actions: ['consoleLogFetch', 'assignFromFetchToContext'],
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
    console.log(values);
    send({ type: 'fetchEvent', data: values });
  };

  useEffect(() => {
    console.log('MACHINE STATE:', state.value);
    console.log(state);

    if (state.value === 'successState') {
      navigate('/');
    }
  }, [state]);

  return (
    <>
      <Formik
        initialValues={{
          email: 'salarsattiss@gmail.com',
          password: '6PINEapplesfoo!!',
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

              {/* <Grid item xs={12} sx={{ mt: -1 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={2}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={checked}
                        onChange={(event) => setChecked(event.target.checked)}
                        name="checked"
                        color="primary"
                        size="small"
                      />
                    }
                    label={<Typography variant="h6">Keep me signed in</Typography>}
                  />
                  <Link variant="h6" component={RouterLink} color="text.primary">
                    Forgot Password?
                  </Link>
                </Stack>
              </Grid> */}
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
