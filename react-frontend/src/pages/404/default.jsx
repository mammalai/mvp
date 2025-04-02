import { Box, Button, Container, Typography, useTheme } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import { motion } from 'framer-motion';

const NotFound = () => {
  const theme = useTheme();
  const navigate = useNavigate();

  return (
    <Container
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        textAlign: 'center',
        py: 5
      }}
    >
      <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ duration: 0.5 }}>
        <ErrorOutlineIcon
          sx={{
            fontSize: '8rem',
            color: theme.palette.error.main,
            mb: 2
          }}
        />
      </motion.div>

      <motion.div initial={{ y: -50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2, duration: 0.8 }}>
        <Typography variant="h1" component="h1" gutterBottom>
          404
        </Typography>
      </motion.div>

      <motion.div initial={{ y: 50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.5, duration: 0.8 }}>
        <Typography variant="h4" gutterBottom>
          Page Not Found
        </Typography>

        <Typography variant="body1" color="textSecondary" paragraph sx={{ maxWidth: 480, mx: 'auto', mb: 4 }}>
          The page you're looking for doesn't exist or has been moved. We suggest you go back to the homepage.
        </Typography>

        <Box>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/')}
            sx={{
              px: 5,
              boxShadow: theme.customShadows?.primary,
              '&:hover': {
                transform: 'translateY(-2px)'
              },
              transition: 'transform 0.3s ease'
            }}
          >
            Go to Home
          </Button>
        </Box>
      </motion.div>
    </Container>
  );
};

export default NotFound;
