// project imports
import Navigation from './Navigation';
import SimpleBar from 'components/third-party/SimpleBar';
import { useGetMenuMaster } from 'api/menu';
import { useTheme } from '@mui/material/styles';
import { borderRadius } from '@mui/system';
// ==============================|| DRAWER CONTENT ||============================== //

export default function DrawerContent() {
  const { menuMaster } = useGetMenuMaster();
  const drawerOpen = menuMaster.isDashboardDrawerOpened;
  const theme = useTheme();

  return (
    <>
      <SimpleBar
        sx={{
          '& .simplebar-content': { display: 'flex', flexDirection: 'column' },
          backgroundColor: theme.palette.m3.surfaceContainerLow,
          borderTopRightRadius: 16,
          borderBottomRightRadius: 16
        }}
      >
        <Navigation />
      </SimpleBar>
    </>
  );
}
