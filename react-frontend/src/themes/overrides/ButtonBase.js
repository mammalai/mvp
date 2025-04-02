// ==============================|| OVERRIDES - BUTTON ||============================== //
// TO DO: add a faster button ripple animation based on m3 spec
import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';

export default function ButtonBase(theme) {
  return {
    MuiButtonBase: {
      defaultProps: {
        disableRipple: false
      }
    }
  };
}
