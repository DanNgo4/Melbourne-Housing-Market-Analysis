import {React, useState, useEffect  } from "react";
import { Box, TextField, Button, Typography, InputAdornment, Grid } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';

Chart.register(...registerables);

//Styles to apply to the two main boxes on this component
const boxStyles = {
    width: {
        xs: '90vw',
        sm: '75vw',
        md: '60vw',
        lg: '50vw',
        xl: '40vw',
    },
    padding: '2.5%',
    margin: '2.5%',
    boxShadow: 3,
};

// let yourPrice = new Array(predictedPrices.length).fill(null);
// const dummyPrice = 1200000;
// yourPrice[3] = dummyPrice;

const LineChartComponent = () => {
    const [predictedSquareMetres, setPredictedSquareMetres] = useState([]);
    const [predictedPrices, setPredictedPrices] = useState([]);
    const [predictedValuesData, setPredictedValuesData] = useState([]);
    const [squareMetres, setSquareMetres] = useState("")
    const [numOfBedrooms, setNumOfBedrooms] = useState("")
    const [squareMetresError, setSquareMetresError] = useState(false)
    const [numOfBedroomsError, setNumOfbedroomsError] = useState(false)

    useEffect(() => {
        axios.get('http://localhost:8000/predicted_values/')
          .then(response => {
            setPredictedValuesData(Object.values(response.data));
          })
          .catch(error => {
            console.error(error);
          });
    }, []);
    
    useEffect(() => {
        if (predictedValuesData.length > 0) {
            Promise.all(
                predictedValuesData.map(dataRow => {

                    predictedSquareMetres.push(dataRow["Landsize"]);
    
                    return axios.get(`http://localhost:8000/predict/${dataRow["Landsize"]}/${dataRow["Car"]}/${dataRow["Distance"]}/${dataRow["Propertycount"]}/`)
                        .then(res => res.data.predicted_price);
                })
            ).then(predictedPrices => {
                const sortedSquareMetres = predictedSquareMetres.sort((a, b) => b - a);
                setPredictedPrices(predictedPrices); 
                setSquareMetres(sortedSquareMetres)
            }).catch(error => console.error(error));
        }
    }, [predictedValuesData]);
        
    //Sends in the present value to display any errors after user has clicked submit
    //this is useful in the context that the user has not interacted with a required field it will display an error
    const validateForm = () => {
        handleSquareMetresChanged({ target: { value: squareMetres } });
        handleNumOfBedroomsChanged({ target: { value: numOfBedrooms } });
    }

    //Handle the form submit.
    const handleSubmit = e => {
        e.preventDefault();
        validateForm();
        if (e.target.checkValidity()) {

        }
    };

    //Handles when square footage input text has been changed
    const handleSquareMetresChanged = e => {
        setSquareMetres(e.target.value);
        //Ensure square foot is not empty
        if (e.target.value === '') {
            setSquareMetresError("Please enter square footage of property!");
        }
        //Ensure only positive floats/integers have been inputted
        else if (!/^[0-9]+(\.[0-9]+)?$/.test(e.target.value)) {
            setSquareMetresError("Please enter a positive numerical value for square footage!");
        }
        else {
            setSquareMetresError(false);
        }
    }

    //Handles when number of bedrooms input text has been changed
    const handleNumOfBedroomsChanged = e => {
        setNumOfBedrooms(e.target.value);
        //Ensure that number of bedrooms is not empty
        if (e.target.value === '') {
            setNumOfbedroomsError("Please enter number of bedrooms!");
        }
        //Ensure that only positive integers have been inputted
        else if (!/^[0-9]+$/.test(e.target.value)) {
            setNumOfbedroomsError("Please enter a positive full number value for number of bedrooms!");
        }
        else {
            setNumOfbedroomsError(false);
        }
    }

    //Line Chart Data and Options
    const data = {
        labels: predictedSquareMetres,
        datasets: [
            {
                label: 'Predicted Prices',
                data: predictedPrices,
                backgroundColor: 'rgba(80, 194, 194, 0.2)',
                borderColor: 'rgba(80, 194, 194, 1)',
                borderWidth: 2,
               // pointRadius: predictedPrices.map((_, index) => (index === 3 ? 0 : 5))
            },
            // {
            //     label: 'Your Prediction',
            //     data: yourPrice,
            //     backgroundColor: 'rgba(255, 176, 193, 0.6)',
            //     borderColor: 'rgba(255, 176, 193, 1)',
            //     borderWidth: 2,
            //     pointRadius: 10,
            //     pointHoverRadius: 8,
            // },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: true,
            },
            datalabels: {
                display: false,  // Disable data labels on points
            },
        },
        scales: {
            y: {
                type: 'linear',
                ticks: {
                    callback: (value) => `$${value}`
                },
            },
            x: {
                type: 'linear',
            },
        },
        maintainAspectRatio: false,
    };

    return (
        <Box
            width='100%'
            display="flex"
            flexDirection="column"
            justifyContent="center"
            alignItems="center"
        >
            <Box
                display="flex"
                flexDirection="column"
                justifyContent="center"
                alignItems="center"
                minHeight="90vh"
                mt={2}
                mb={2}
            >
                <Box
                    component="form"
                    noValidate
                    autoComplete='off'
                    sx={{
                        '& .MuiTextField-root': { m: 1, width: '25ch' },
                        ...boxStyles,
                        padding: '5%'
                    }}
                    onSubmit={handleSubmit}>
                    <Box
                        sx={{
                            width: '100%',
                        }}>
                        <Grid container spacing={2} mb={2.5}>
                            <Grid item xs={12} sm={6} sx={{ display: 'flex', flexDirection: 'row' }}>
                                <TextField
                                    required
                                    id="squareMetres"
                                    label="Square Metres"
                                    value={squareMetres}
                                    onChange={handleSquareMetresChanged}
                                    error={squareMetresError}
                                    helperText={squareMetresError ? squareMetresError : ""}
                                    slotProps={{
                                        input: {
                                            endAdornment: <InputAdornment position="end">metres</InputAdornment>,
                                        },
                                    }}
                                    sx={{ flexGrow: 1 }}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6} sx={{ display: 'flex', flexDirection: 'row' }}>
                                <TextField
                                    required
                                    id="numOfBedrooms"
                                    label="Number of Bedrooms"
                                    value={numOfBedrooms}
                                    onChange={handleNumOfBedroomsChanged}
                                    error={numOfBedroomsError}
                                    helperText={numOfBedroomsError ? numOfBedroomsError : ""}
                                    sx={{ flexGrow: 1 }}
                                />
                            </Grid>
                        </Grid>
                        <Button type="submit" sx={{ width: '100%', }} variant="contained">PREDICT PRICE</Button>
                    </Box>
                </Box>
                <Box sx={{ ...boxStyles }}>
                    <Typography variant="h4" sx={{
                        fontSize: { xs: '1rem', sm: '1.25rem', md: '1.5rem', lg: '1.75rem' },
                        mb: { sm: 1 },
                    }}>
                    {/* Predicted Price: ${dummyPrice} */}
                    </Typography>
                    <Typography variant="body1" sx={{
                        fontSize: '0.75rem',
                        fontWeight: 'bold',
                        textAlign: 'center',
                        color: 'grey',
                        mb: { sm: 2, lg: 5 },
                    }}>
                        Price Predictions by Square Footage
                    </Typography>
                    <Box sx={{
                        width: '100%',
                        height: { xs: '30vh', md: '40vh' },
                    }}>
                        <Line data={data} options={options} />
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};

export default LineChartComponent;
