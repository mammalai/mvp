import { useState,useEffect } from 'react';

import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import CssBaseline from '@mui/material/CssBaseline';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import StarIcon from '@mui/icons-material/Star';
import DraftsIcon from '@mui/icons-material/Drafts';
import DeleteIcon from '@mui/icons-material/Delete';

const drawerWidth = 240;

import { alpha } from '@mui/material/styles';
import { blend } from '@mui/system';

import { useTheme } from '@mui/material/styles';
import { fontWeight } from '@mui/system';




export default function NavigationDrawerView() {

  const [selectedItem, setSelectedItem] = useState(1);

  const theme = useTheme();

  useEffect(() => {

  }, []);

  
  return (
    <Box bgcolor="#FFFFFF" width="100%" height="100%" sx={{p:5}}>
      <Box sx={{ 
          overflow: 'auto',
          width: drawerWidth,
          backgroundColor:
          theme.palette.m3.surfaceContainerLow,
          borderTopRightRadius: 16,
          borderBottomRightRadius: 16,
        }}
      >
        <List>
          {[
            { id:0, type: 'category', title: 'Overview', icon: <InboxIcon /> },
            { id:1, type: 'item', title: 'Inbox', icon: <InboxIcon /> },
            { id:2, type: 'item', title: 'Starred', icon: <StarIcon /> },
            { id:3, type: 'item', title: 'Send email', icon: <MailIcon /> },
            { id:4, type: 'divider', title: 'none', icon: <DraftsIcon /> },
            { id:5, type: 'category', title: 'Drafts', icon: <DraftsIcon /> },
            { id:6, type: 'item', title: 'Trash', icon: <DeleteIcon /> }
          ].map(({ id, type, title, icon }, index) => (
            <>
              {type == 'category' ? (
                // for the category - which can't be selected or hovered
                <ListItem key={title} disablePadding>
                  <ListItemButton
                    sx={{
                      pointerEvents: "none", // Prevents interaction & cursor change
                      marginLeft: 1,
                      marginRight: 1,
                    }}
                  >
                    <ListItemText primary={
                      <Typography 
                        variant="labelLarge"
                        sx={{
                          color: theme.palette.m3.onSurfaceVariant,
                        }}
                      >
                        {title}
                      </Typography>
                    } />
                  </ListItemButton>
                </ListItem>
              ) : (type == 'divider') ? (
                <>
                  <Divider 
                    sx={{ 
                      my: '8px',
                      mx: '2px',
                      backgroundColor: theme.palette.m3.outlineVariant,
                      height:'2px' 
                    }} />
                </>
              ) : (
                // for the selectable buttons
                <ListItem key={title} disablePadding>
                  <ListItemButton
                    onClick={() => setSelectedItem(id)}
                    sx={{
                      ...(id === selectedItem 
                        ? {
                            backgroundColor: theme.palette.m3.secondaryContainer,
                            '&:hover': {
                              backgroundColor: blend(theme.palette.m3.secondaryContainer, theme.palette.m3.onSecondaryContainer, 0.08),
                            }
                          }
                        : {
                            backgroundColor: 'transparent',
                            '&:hover': {
                              backgroundColor: alpha(theme.palette.m3.onSurface, 0.08),
                            }
                          }),
                      marginLeft: 1,
                      marginRight: 1,
                      borderRadius: 28
                    }}
                  >
                    <ListItemIcon sx={{marginRight: 2}}>
                      {icon && (
                        <Box sx={{ 
                          color: id === selectedItem 
                            ? theme.palette.m3.onSecondaryContainer 
                            : theme.palette.m3.onSurfaceVariant,
                          marginBottom: -0.6
                        }}>
                          {React.cloneElement(icon, { fontSize: 'small' })}
                        </Box>
                      )}
                    </ListItemIcon>
                    <ListItemText primary={
                      <Typography 
                        variant="labelLarge"
                        sx={ (id == selectedItem) ? {
                          color: theme.palette.m3.onSecondaryContainer,
                          fontWeight: 500
                        } : {
                          color: theme.palette.m3.onSurfaceVariant
                        }}
                      >
                        {title}
                      </Typography>
                    } />
                  </ListItemButton>
                </ListItem>
              )}
            </>
          ))}
        </List>

      </Box>
    </Box>
    
  );
}
