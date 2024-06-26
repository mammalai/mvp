import { useEffect, useState } from 'react';
import axios from 'axios';

// material-ui
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';
import Grid from '@mui/material/Grid';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

// project import
import AnimateButton from 'components/@extended/AnimateButton';
import { strengthColor, strengthIndicator } from 'utils/password-strength';

// x-state
import { setup, fromPromise, assign } from 'xstate';
import { useMachine } from '@xstate/react';

// assets
import EyeOutlined from '@ant-design/icons/EyeOutlined';
import EyeInvisibleOutlined from '@ant-design/icons/EyeInvisibleOutlined';

const registerMachine = setup({
  actors: {
    loginRequest: fromPromise(async (args) => {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          axios
            .post('/api/auth/emailregistration', {
              email: args.input.context.loginCredentials.email,
              password: args.input.context.loginCredentials.password,
            })
            .then((response) => {
              resolve(response);
            })
            .catch((error) => {
              reject(error);
            });
        }, 1000);
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
      if (axiosError.message === 'Request failed with status code 500') {
        return {
          errorMessage: 'An unknown error occured. Please try again later.',
        };
      } else if (axiosError?.response?.data?.error) {
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

// ============================|| JWT - REGISTER ||============================ //

export default function AuthRegister() {
  const [state, send] = useMachine(registerMachine);

  const [level, setLevel] = useState();
  const [showPassword, setShowPassword] = useState(false);
  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  // shows pass word strength level
  const changePassword = (value) => {
    const temp = strengthIndicator(value);
    setLevel(strengthColor(temp));
  };
  // set the initial word strength level
  useEffect(() => {
    changePassword('');
  }, []);

  const handleSubmit = (values) => {
    send({ type: 'fetchEvent', data: values });
  };

  return (
    <>
      {state.value === 'successState' ? (
        <Grid container spacing={3}>
          <Grid item xs={12} md={12}>
            Please check your email and click the link to verify your account.
          </Grid>
        </Grid>
      ) : (
        <Formik
          initialValues={{
            // firstname: 'Salar',
            // lastname: 'Satti',
            email: 'salarsattiss@gmail.com',
            // company: '',
            password: '6PINEapplesfoo!!',
            submit: null,
          }}
          validationSchema={Yup.object().shape({
            // firstname: Yup.string().max(255).required('First Name is required'),
            // lastname: Yup.string().max(255).required('Last Name is required'),
            // email: Yup.string().email('Must be a valid email').max(255).required('Email is required'),
            email: Yup.string().matches(``),
            password: Yup.string().max(255).required('Password is required'),
          })}
          onSubmit={handleSubmit}
        >
          {({ errors, handleBlur, handleChange, handleSubmit, touched, values }) => (
            <form noValidate onSubmit={handleSubmit}>
              <Grid container spacing={3}>
                {/* <Grid item xs={12} md={6}>
                  <Stack spacing={1}>
                    <InputLabel htmlFor="firstname-signup">First Name*</InputLabel>
                    <OutlinedInput
                      id="firstname-login"
                      type="firstname"
                      value={values.firstname}
                      name="firstname"
                      onBlur={handleBlur}
                      onChange={handleChange}
                      placeholder="John"
                      fullWidth
                      error={Boolean(touched.firstname && errors.firstname)}
                    />
                  </Stack>
                  {touched.firstname && errors.firstname && (
                    <FormHelperText error id="helper-text-firstname-signup">
                      {errors.firstname}
                    </FormHelperText>
                  )}
                </Grid>
                <Grid item xs={12} md={6}>
                  <Stack spacing={1}>
                    <InputLabel htmlFor="lastname-signup">Last Name*</InputLabel>
                    <OutlinedInput
                      fullWidth
                      error={Boolean(touched.lastname && errors.lastname)}
                      id="lastname-signup"
                      type="lastname"
                      value={values.lastname}
                      name="lastname"
                      onBlur={handleBlur}
                      onChange={handleChange}
                      placeholder="Doe"
                      inputProps={{}}
                    />
                  </Stack>
                  {touched.lastname && errors.lastname && (
                    <FormHelperText error id="helper-text-lastname-signup">
                      {errors.lastname}
                    </FormHelperText>
                  )}
                </Grid> */}
                {/* <Grid item xs={12}>
                  <Stack spacing={1}>
                    <InputLabel htmlFor="company-signup">Company</InputLabel>
                    <OutlinedInput
                      fullWidth
                      error={Boolean(touched.company && errors.company)}
                      id="company-signup"
                      value={values.company}
                      name="company"
                      onBlur={handleBlur}
                      onChange={handleChange}
                      placeholder="Demo Inc."
                      inputProps={{}}
                    />
                  </Stack>
                  {touched.company && errors.company && (
                    <FormHelperText error id="helper-text-company-signup">
                      {errors.company}
                    </FormHelperText>
                  )}
                </Grid> */}
                <Grid item xs={12}>
                  <Stack spacing={1}>
                    <InputLabel htmlFor="email-signup">Email Address</InputLabel>
                    <OutlinedInput
                      fullWidth
                      error={Boolean(touched.email && errors.email)}
                      id="email-login"
                      type="email"
                      value={values.email}
                      name="email"
                      onBlur={handleBlur}
                      onChange={handleChange}
                      placeholder="demo@company.com"
                      inputProps={{}}
                    />
                  </Stack>
                  {touched.email && errors.email && (
                    <FormHelperText error id="helper-text-email-signup">
                      {errors.email}
                    </FormHelperText>
                  )}
                </Grid>
                <Grid item xs={12}>
                  <Stack spacing={1}>
                    <InputLabel htmlFor="password-signup">Password</InputLabel>
                    <OutlinedInput
                      fullWidth
                      error={Boolean(touched.password && errors.password)}
                      id="password-signup"
                      type={showPassword ? 'text' : 'password'}
                      value={values.password}
                      name="password"
                      onBlur={handleBlur}
                      onChange={(e) => {
                        handleChange(e);
                        changePassword(e.target.value);
                      }}
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
                      placeholder="******"
                      inputProps={{}}
                    />
                  </Stack>
                  {touched.password && errors.password && (
                    <FormHelperText error id="helper-text-password-signup">
                      {errors.password}
                    </FormHelperText>
                  )}
                  <FormControl fullWidth sx={{ mt: 2 }}>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item>
                        <Box sx={{ bgcolor: level?.color, width: 85, height: 8, borderRadius: '7px' }} />
                      </Grid>
                      <Grid item>
                        <Typography variant="subtitle1" fontSize="0.75rem">
                          {level?.label}
                        </Typography>
                      </Grid>
                    </Grid>
                  </FormControl>
                </Grid>
                {/* <Grid item xs={12}>
                  <Typography variant="body2">
                    By Signing up, you agree to our &nbsp;
                    <Link variant="subtitle2" component={RouterLink} to="#">
                      Terms of Service
                    </Link>
                    &nbsp; and &nbsp;
                    <Link variant="subtitle2" component={RouterLink} to="#">
                      Privacy Policy
                    </Link>
                  </Typography>
                </Grid> */}
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
                      Create Account
                    </Button>
                  </AnimateButton>
                </Grid>
                {state.value === 'loadingState' ? (
                  <Grid item xs={12}>
                    <LinearProgress />
                  </Grid>
                ) : null}
              </Grid>
            </form>
          )}
        </Formik>
      )}
    </>
  );
}
