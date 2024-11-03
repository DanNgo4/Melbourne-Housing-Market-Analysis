import { useState } from "react";

import { NavLink, Link } from "react-router-dom";
import { AppBar, Toolbar, IconButton, Typography, Button, Drawer, Box, ListItem, ListItemText, ListItemIcon, List, Divider, Switch } from "@mui/material";
import { Menu, Home, Info } from "@mui/icons-material";

const NavBar = () => {
    //Use states for drawer and darkmode
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [darkMode, setDarkMode] = useState(false);

    //Toggle drawer function
    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return;
        }

        setDrawerOpen(open);
    };

    //Dark mode on off toggler
    const handleDarkModeToggle = () => {
        setDarkMode(!darkMode);
    };

    const drawerContent = (
        <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)} onKeyDown={toggleDrawer(false)}>
            <List>
                <ListItem button component={Link} to="/">
                    <ListItemIcon><Home /></ListItemIcon>
                    <ListItemText primary="Home" />
                </ListItem>

                <ListItem button component={Link} to="/line">
                    <ListItemIcon><Info /></ListItemIcon>
                    <ListItemText primary="Line" />
                </ListItem>

                <ListItem button component={Link} to="/heat">
                    <ListItemIcon><Info /></ListItemIcon>
                    <ListItemText primary="Heat" />
                </ListItem>

                <ListItem button component={Link} to="/donut">
                    <ListItemIcon><Info /></ListItemIcon>
                    <ListItemText primary="Donut" />
                </ListItem>
            </List>
            <Divider />
            <List>
            <ListItem>
                <ListItemText primary="Dark Mode" />
                <Switch checked={darkMode} onChange={handleDarkModeToggle} />
            </ListItem>
            </List>
        </Box>
    );

    return (
        <div>
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" color="inherit" aria-label="menu" onClick={toggleDrawer(true)} >
                        <Menu />
                    </IconButton>

                    <Typography variant="h6" sx={{ flexGrow: 1 }}>
                        HD Hunters
                    </Typography>
                    <Box sx={{
                    display: { xs: 'none', md: 'block'}
                    }}>
                    <Button color="inherit" component={NavLink} to="/">Home</Button>
                    <Button color="inherit" component={NavLink} to="/line">Line</Button>
                    <Button color="inherit" component={NavLink} to="/heat">Heat</Button>
                    <Button color="inherit" component={NavLink} to="/donut">Donut</Button>
                    </Box>
                </Toolbar>
            </AppBar>

            <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
                {drawerContent}
            </Drawer>
        </div>
    );
};

export default NavBar;
