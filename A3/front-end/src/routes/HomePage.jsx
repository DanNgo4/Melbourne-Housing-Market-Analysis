import { Typography, Grid, Box } from '@mui/material';

const Home = () => {
    return (
        <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
            <Box sx={{ width: '90vw', boxShadow: 3, padding: '2%', margin: '2.5%' }}>
                <Grid container spacing={5} mb={2.5}>
                    <Grid item xs={12}>
                        <Typography variant="h4" component="h4">
                            Project Introduction:
                        </Typography>
                        <Typography variant="p" component="p">
                            For this project we had to choose between four different topics which were civil aviation, weather analysis, air quality and health and housing market. After discussions, we have chosen the housing market because our team lives in Melbourne, Australia where the price of houses have been very high and continue to rise so we consider this an important and timely topic for ourselves and users of our project.

                            This project will be conducted over twelve weeks and require the collection of Melbourne housing prices data along with their attributes such as their location and type of housing (Unit, House etc) which will then be trained by an Artificial Intelligence (AI) model in Python. FastAPI will be used in Python to create a backend connection to our frontend web application created in ReactJS to visualise the data so users can interact with an AI in a fun and effective way to keep them engaged.
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
                        <Typography variant="p" component="p">
                        I am a 23 year old second year student doing a Bachelor of Computer Science majoring in Software Development at Swinburne University hawthorn campus and I am the Team lead in this project. I have a passion for software development and have strong knowledge of backend and frontend development in various programming languages. I have experience building full stack applications with a database, API and a frontend single page application. I am keen to lead this project to success in meeting all the criteria.
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <Typography variant="h5" component="h5">
                            Dan Ngo
                        </Typography>
                        <Typography variant="p" component="p">
                        19-year-old Vietnamese second year, second semester doing Bachelor of Computer Science (Software Development & Data Science Majors). Currently most skilled in Web Development using React and Node.js.
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        <Typography variant="h5" component="h5">
                            Indu Seth
                        </Typography>
                        <Typography variant="p" component="p">
                        I am Indu Seth, a student pursuing a Bachelor of Computer Science. In this assignment for our team, I am responsible for the scope management and closure plan. With my background in computer science, I will apply my skills in problem solving, machine learning and web design to contribute to the team’s final project. I am enthusiastic about leveraging my technical skills to advance this project and collaborate effectively with my team.
                        </Typography>
                    </Grid>
                </Grid>
            </Box>
        </Box>
    );
};

export default Home;
