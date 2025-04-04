// assets
import DashboardIcon from '@mui/icons-material/Dashboard';
import GridViewIcon from '@mui/icons-material/GridView';

// icons
const icons = {
  DashboardIcon,
  GridViewIcon
};

// ==============================|| MENU ITEMS - DASHBOARD ||============================== //

const dashboard = {
  id: 'group-dashboard',
  title: 'Navigation',
  type: 'group',
  children: [
    {
      id: 'dashboard',
      title: 'Dashboard',
      type: 'item',
      url: '/dashboard/default',
      icon: icons.DashboardIcon,
      breadcrumbs: false
    },
    {
      id: 'component-overview',
      title: 'Components Overview',
      type: 'item',
      url: '/component-overview',
      icon: icons.GridViewIcon,
      breadcrumbs: false
    }
  ]
};

export default dashboard;
