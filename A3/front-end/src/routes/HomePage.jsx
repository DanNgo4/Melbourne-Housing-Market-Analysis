import { Typography, Grid, Box, Button, Card, CardContent } from "@mui/material";
import { Link } from "react-router-dom";

const Home = () => {
    return (
        <Box sx={{ width: "100%", display: "flex", justifyContent: "center" }}>
            <Box sx={{ width: "90vw", boxShadow: 3, padding: "2%", margin: "2.5%" }}>
                <Grid container spacing={5} mb={2.5}>
                    <Grid item xs={12}>
                        <Typography variant="h4" component="h4">
                            Project Introduction:
                        </Typography>
                        <Typography variant="body1" component="p">
                            For this project, we had to choose between four different topics: civil aviation, weather analysis, air quality and health, and the housing market. After discussions, we chose the housing market as our focus since we live in Melbourne, Australia, where house prices have been high and continue to rise. This is an important and timely topic for us and users of our project.
                        </Typography>
                        <Typography variant="body1" component="p" mt={2}>
                            This project will be conducted over twelve weeks and requires the collection of Melbourne housing prices data along with attributes like location and type (e.g., Unit, House). The data will be used to train an Artificial Intelligence (AI) model in Python. We’ll connect the backend, built with FastAPI, to our React-based frontend web application to visualize data in a fun and engaging way.
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Typography variant="h4" component="h4">
                            Team Members:
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <Typography variant="h5" component="h5">
                            Mitchell Henry
                        </Typography>
                        <Typography variant="body2">
                            I am a 23-year-old second-year student in Bachelor of Computer Science majoring in Software Development. I am the Team Lead for this project and have a passion for full-stack development. I look forward to guiding this project to success.
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <Typography variant="h5" component="h5">
                            Dan Ngo
                        </Typography>
                        <Typography variant="body2">
                            19-year-old Vietnamese second-year student majoring in Software Development & Data Science. Skilled in Web Development using React and Node.js, excited to work on the data analysis aspects of this project.
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <Typography variant="h5" component="h5">
                            Indu Seth
                        </Typography>
                        <Typography variant="body2">
                            I am Indu, a Computer Science student passionate about using technology to tackle real-world challenges. This application harnesses machine learning to provide accurate property price predictions for the Greater Melbourne area. Explore the features, input your property details, and gain valuable insights to navigate the housing market!
                        </Typography>
                    </Grid>

                    <Grid item xs={12}>
                        <Typography variant="h4" component="h4" mt={4} mb={2}>
                            Explore Our Features
                        </Typography>
                    </Grid>

                    <Grid item xs={12} sm={4}>
                        <Card sx={{ boxShadow: 2, padding: 2 }}>
                            <CardContent>
                                <Typography variant="h5" component="div">
                                    Line Chart Analysis
                                </Typography>
                                <Typography variant="body2" color="text.secondary" mt={1}>
                                    Dive into our Line Chart to view housing price trends over time. This visualization offers insights into how different factors affect the market.
                                </Typography>
                                <Button 
                                    variant="contained" 
                                    color="primary" 
                                    component={Link} 
                                    to="/line" 
                                    sx={{ mt: 2 }}
                                >
                                    Go to Line Page
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={4}>
                        <Card sx={{ boxShadow: 2, padding: 2 }}>
                            <CardContent>
                                <Typography variant="h5" component="div">
                                    Heatmap
                                </Typography>
                                <Typography variant="body2" color="text.secondary" mt={1}>
                                The chart provides a geographic visualisation of median house prices, allowing users to explore price variations across different council areas in Melbourne.
                                </Typography>
                                <Button 
                                    variant="contained" 
                                    color="success" 
                                    component={Link} 
                                    to="/heat" 
                                    sx={{ mt: 2 }}
                                >
                                    Go to Heatmap Page
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={4}>
                        <Card sx={{ boxShadow: 2, padding: 2 }}>
                            <CardContent>
                                <Typography variant="h5" component="div">
                                    Donut Chart Distribution
                                </Typography>
                                <Typography variant="body2" color="text.secondary" mt={1}>
                                    Our Donut Chart shows the distribution of house types across price ranges, helping you visualize how different categories compare in the housing market.
                                </Typography>
                                <Button 
                                    variant="contained" 
                                    color="secondary" 
                                    component={Link} 
                                    to="/donut" 
                                    sx={{ mt: 2 }}
                                >
                                    Go to Donut Page
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>
            </Box>
        </Box>
    );
};

export default Home;
