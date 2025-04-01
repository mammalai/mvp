import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

// component display imports
import ButtonView from 'pages/component-overview/button.jsx';
import CardView from 'pages/component-overview/card.jsx';
import TableView from 'pages/component-overview/table.jsx';
import OverviewView from 'pages/component-overview/overview.jsx';
import TabsView from 'pages/component-overview/tabs.jsx';
import NavigationDrawerView from 'pages/component-overview/navigation-drawer.jsx';


function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Box
      role="tabpanel"
      hidden={value !== index}
      id={`vertical-tabpanel-${index}`}
      aria-labelledby={`vertical-tab-${index}`}
      {...other}
      sx={{ width: '100%', height: '100%' }}
    >
      {value === index && (
        <Box>
          {children}
        </Box>
      )}
    </Box>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `vertical-tab-${index}`,
    'aria-controls': `vertical-tabpanel-${index}`,
  };
}

export default function VerticalTabs() {
  const [value, setValue] = React.useState(5);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box
      sx={{ flexGrow: 1, bgcolor: 'background.paper', display: 'flex' }}
    >
      <Tabs
        orientation="vertical"
        variant="scrollable"
        value={value}
        onChange={handleChange}
        aria-label="Vertical tabs example"
        sx={{  borderColor: 'divider', minWidth: 180, borderRadius: 0 }}

      >
        <Tab label="Overview" {...a11yProps(0)} />
        <Tab label="Button" {...a11yProps(1)} />
        <Tab label="Card" {...a11yProps(2)} />
        <Tab label="Table" {...a11yProps(3)} />
        <Tab label="Tabs" {...a11yProps(4)} />
        <Tab label="Navigation Drawer" {...a11yProps(5)} />
        <Tab label="Item Seven" {...a11yProps(6)} />
      </Tabs>
      <TabPanel value={value} index={0}>
        <OverviewView />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <ButtonView />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <CardView />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <TableView />
      </TabPanel>
      <TabPanel value={value} index={4}>
        <TabsView />
      </TabPanel>
      <TabPanel value={value} index={5}>
        <NavigationDrawerView />
      </TabPanel>
      { /*<TabPanel value={value} index={6}>
        Item Seven
      </TabPanel> */}
    </Box>
  );
}
