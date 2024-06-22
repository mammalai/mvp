import PropTypes from 'prop-types';
import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';

// material-ui
import Button from '@mui/material/Button';
import Checkbox from '@mui/material/Checkbox';
import Divider from '@mui/material/Divider';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormHelperText from '@mui/material/FormHelperText';
import Grid from '@mui/material/Grid';
import Link from '@mui/material/Link';
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
import { setup, createMachine, fromPromise, assign } from 'xstate';
import { useMachine } from '@xstate/react';

// assets
import EyeOutlined from '@ant-design/icons/EyeOutlined';
import EyeInvisibleOutlined from '@ant-design/icons/EyeInvisibleOutlined';

import FirebaseSocial from './FirebaseSocial';
import { set } from 'lodash';

const wait = (ms) => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

/** @xstate-layout N4IgpgJg5mDOIC5QAoC2BDAxgCwJYDswBKAOlwgBswBiWAVwCNVcAXAbQAYBdRUABwD2sVrgH5eIAB6IAjABYAHCQDsCmR3XKOCgExydynQBoQAT0QBOAGwqOOnVZlWOHAMyu7OgL5eTaLHiEpLiwAMqMzCwsBFDUEGJgZPgAbgIA1on+OATEZGERrNH4UAgEqZjo0WKcXDUSgsJV4khSiK7yJFYOFhYArK5WPb0yDibmCCM2vUN2rjoWila9vT5+GNlBeeFMhTHUYABOBwIHJHwUlQBmJ6gkWYG5IduRRSVlAhVNNXUtDSJiEmkCFc1hIcgsHF6OkhOmmHGsY0QOlcvRIA36FmUcmWClxVlcPl8IHwAggcAk9xyRHqQn+zVAQIAtFZEQhmSQXJzoU5tL0sSsiZTNuQqDTGqJ6a0EPpWQoLCQnFYllDVGpYcpViAhY98jsojExXTAYhcRyFFiDCNVEsFqyZLoSL1OXY5IN3DjNdrSPRMJg4PBfrSmsaECqOSCOI4+Qp3MYzCaZGCej0FK65PpzXJPesHqRLuhcBQ6AcwIbgy0gWG3BCo6pY3b9EmesonfblINYYSvEA */
const loginMachine = setup({
  actors: {
    handleSubmit: fromPromise(async ({ input }) => {
      // const user = await fetchUser(input.userId);
      console.log(input);
      // console.log(user);
      // console.log(password);
      return {data:'vasdf'};
    })
  }
}).createMachine({
  initial: 'idle',
  states: {
    idle: { // entering details in the login form
      on: {
        submit: {
          target: 'isSubmitting',
        }
      }
    },
    isSubmitting: { // submitting the form and waiting for the response
      invoke: {
        input: ({ context, event }) => ({ user: event.user, password: event.password }),
        src: 'handleSubmit',
        onDone: {
          target: 'success',
          actions: assign({ user: ({ event }) => event.output })
        },
        onError: {
          target: 'failure',
          actions: assign({ error: ({ event }) => event.error })
        }
      }
    }, 
    success: { // successfully logged in
      type: 'final'
    }, 
    failure: {  // failed to login
      type: 'final'
    },
  }
});
  
  

// ============================|| JWT - LOGIN ||============================ //

export default function AuthLogin({ isDemo = false }) {

  const [checked, setChecked] = React.useState(false);

  const [state, send] = useMachine(loginMachine);

  // form validation hooks
  const [showLoadIcon, setShowLoadIcon] = React.useState(false);
  const [showInvalidError, setShowInvalidError] = React.useState(false);
  const [isSub, setIsSub] = React.useState(false);
  const [showUnkownError, setShowUnkownError] = React.useState(false);

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
    const waitForSeconds = async () => {
      setIsSub(true);
      setShowInvalidError(false);
      setShowLoadIcon(true);
      await wait(1000); // Wait for 1 seconds
      axios.post('/api/auth/login', {'email': values.email, 'password': values.password})
        .then(response => {
          console.log(response);
          console.log(response.status === 200)
          // navigate to the home page
          navigate('/');
        })
        .catch(error => {
          console.log(error);
          // represent and invalid email and password
          if (error.response.status === 401) {
            // show error message
            setShowInvalidError(true);
          // something else has gone wrong
          } else {
            setShowUnkownError(true);
          }
          // allow to submit again
          setIsSub(false);
          
        });
      setShowLoadIcon(false);
    };
    waitForSeconds();

  }

  if (state.value === 'idle') {
    //show form
  } elif (state.value === 'loading') {
    //show spinny thing
  } elif (state.value === 'success') {
    //redirect to home page
  } elif (state.value === 'failure') {
    //show error message from context
    //set formik isubmitting to false
  }


  return (
    <>
      <Formik
        initialValues={{
          email: 'salarsattiss@gmail.com',
          password: 'Stongassword12345!',
          submit: null
        }}
        validationSchema={Yup.object().shape({
          email: Yup.string().email('Must be a valid email').max(255).required('Email is required'),
          password: Yup.string().max(255).required('Password is required')
        })}
        onSubmit={(values) => send({ type: 'submit', user: values.email, password: values.password })}
      >
        {({ errors, handleBlur, handleChange, handleSubmit, isSubmitting, touched, values }) => (
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
              {showInvalidError ?
              <Grid item xs={12}>
                <Typography color='red'>
                  This email and password does not exist.
                </Typography>
              </Grid>
              : null}

              {showUnkownError ?
              <Grid item xs={12}>
                <Typography color='red'>
                  Something went wrong. Please try again later.
                </Typography>
              </Grid>
              : null}

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
              
              {showLoadIcon ? 
              <Grid item xs={12}>
                <LinearProgress />
              </Grid>
              :
              null}
             

            </Grid>
            <div>
              {JSON.stringify(state)}
            </div>
          </form>
        )}
      </Formik>
    </>
  );
}

AuthLogin.propTypes = { isDemo: PropTypes.bool };
