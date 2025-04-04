import { Link } from 'react-router-dom';

// material-ui
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material/styles';

// project import
import AuthWrapper from '../AuthWrapper';
import AuthRequestEmail from '../auth-forms/password-reset/AuthRequestEmail';

// ================================|| LOGIN ||================================ //

export default function Login() {
  const theme = useTheme();

  return (
    <AuthWrapper>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Stack direction="row" justifyContent="space-between" alignItems="baseline" sx={{ mb: { xs: -0.5, sm: 0.5 } }}>
            <Typography variant="h3">Request Password Reset</Typography>
            <Typography component={Link} to="/login" variant="body1" sx={{ textDecoration: 'none' }} color={theme.palette.m3.primary}>
              Login
            </Typography>
          </Stack>
        </Grid>
        <Grid item xs={12}>
          <AuthRequestEmail />
        </Grid>
      </Grid>
    </AuthWrapper>
  );
}
