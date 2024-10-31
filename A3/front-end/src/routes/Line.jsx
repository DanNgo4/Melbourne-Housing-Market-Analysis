import { React, useState, useEffect } from "react";
import { Box, TextField, Button, Typography, InputAdornment, Grid } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';

Chart.register(...registerables);

// Styles to apply to the two main boxes on this component
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

const LineChartComponent = () => {
    //Retrieving from session storage if already there, saves time on reloads
    const [predictedSquareMetres, setPredictedSquareMetres] = useState(() => {
        const storedData = sessionStorage.getItem('predictedSquareMetres');
        return storedData ? JSON.parse(storedData) : [];
    });

    const [predictedPrices, setPredictedPrices] = useState(() => {
        const storedData = sessionStorage.getItem('predictedPrices');
        return storedData ? JSON.parse(storedData) : [];
    });

    
    const [predictedValuesData, setPredictedValuesData] = useState([]);
    const [yourPredictedPrice, setYourPredictedPrice] = useState([]);

    // For useStates
    const [squareMetres, setSquareMetres] = useState("");
    const [distance, setDistance] = useState("");
    const [numOfCars, setCars] = useState("");
    const [propertyCount, setPropertyCount] = useState("");

    // Form Errors
    const [squareMetresError, setSquareMetresError] = useState(false);
    const [distanceError, setDistanceError] = useState(false);
    const [numOfCarsError, setCarsError] = useState(false);
    const [propertyCountError, setPropertyCountError] = useState(false);

    useEffect(() => {
        // Fetch predicted values data from the API
        axios.get('http://localhost:8000/predicted_values/')
            .then(response => {
                setPredictedValuesData(Object.values(response.data));
            })
            .catch(error => {
                console.error(error);
            });
    }, []);

    useEffect(() => {
        // Only fetch predictions if not already in session storage
        if (predictedValuesData.length > 0) {
            const newSquareMetres = [];
            Promise.all(
                predictedValuesData.map(dataRow => {
                    newSquareMetres.push(dataRow["Landsize"]);

                    return axios.get(`http://localhost:8000/predict/${dataRow["Landsize"]}/${dataRow["Car"]}/${dataRow["Distance"]}/${dataRow["Propertycount"]}/`)
                        .then(res => res.data.predicted_price);
                })
            ).then(predictedPrices => {
                const sortedSquareMetres = Array.from(newSquareMetres).sort((a, b) => b - a);
                setPredictedPrices(predictedPrices);
                setPredictedSquareMetres(sortedSquareMetres);

                // Save to session storage
                sessionStorage.setItem('predictedSquareMetres', JSON.stringify(sortedSquareMetres));
                sessionStorage.setItem('predictedPrices', JSON.stringify(predictedPrices));
            }).catch(error => console.error(error));
        }
    }, [predictedValuesData]);

    // Function to validate the form
    const validateForm = () => {
        handleSquareMetresChanged({ target: { value: squareMetres } });
        handleDistanceChanged({ target: { value: distance } });
        handleNumOfCarsChanged({ target: { value: numOfCars } });
        handlePropertyCountChanged({ target: { value: propertyCount } });
    };

    // Handle the form submit
    const handleSubmit = e => {
        e.preventDefault();
        validateForm();
        if (e.target.checkValidity()) {
            axios.get(`http://localhost:8000/predict/${squareMetres}/${numOfCars}/${distance}/${propertyCount}/`)
                .then(res => setYourPredictedPrice([{ x: squareMetres, y: res.data.predicted_price }]));
        }
    };

    // Handles input changes
    const handleSquareMetresChanged = e => {
        setSquareMetres(e.target.value);
        if (e.target.value === '') {
            setSquareMetresError("Please enter square footage of property!");
        } else if (!/^[0-9]+(\.[0-9]+)?$/.test(e.target.value)) {
            setSquareMetresError("Please enter a positive numerical value for square footage!");
        } else {
            setSquareMetresError(false);
        }
    };

    const handleDistanceChanged = e => {
        setDistance(e.target.value);
        if (e.target.value === '') {
            setDistanceError("Please enter distance from CBD!");
        } else if (!/^[0-9]+(\.[0-9]+)?$/.test(e.target.value)) {
            setDistanceError("Please enter a positive numerical value for distance from CBD!");
        } else {
            setDistanceError(false);
        }
    };

    const handleNumOfCarsChanged = e => {
        setCars(e.target.value);
        if (e.target.value === '') {
            setCarsError("Please enter number of car spaces!");
        } else if (!/^[0-9]+$/.test(e.target.value)) {
            setCarsError("Please enter a positive full number value for number of cars!");
        } else {
            setCarsError(false);
        }
    };

    const handlePropertyCountChanged = e => {
        setPropertyCount(e.target.value);
        if (e.target.value === '') {
            setPropertyCountError("Please enter distance from CBD!");
        } else if (!/^[0-9]+$/.test(e.target.value)) {
            setPropertyCountError("Please enter a positive full number value for property count!");
        } else {
            setPropertyCountError(false);
        }
    };

    // Line Chart Data and Options
    const data = {
        labels: predictedSquareMetres, // Y Axis
        datasets: [
            {
                label: 'Predicted Prices',
                data: predictedPrices,
                backgroundColor: 'rgba(80, 194, 194, 0.2)',
                borderColor: 'rgba(80, 194, 194, 1)',
                borderWidth: 2,
            },
            ...(yourPredictedPrice.length > 0 ? [{
                label: 'Your Prediction',
                data: yourPredictedPrice,
                backgroundColor: 'rgba(255, 176, 193, 0.6)',
                borderColor: 'rgba(255, 176, 193, 1)',
                borderWidth: 2,
                pointRadius: 10,
                pointHoverRadius: 8,
            }] : []),
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: true,
            },
            datalabels: {
                display: false,
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
                                    id="distance"
                                    label="Distance from CBD"
                                    value={distance}
                                    onChange={handleDistanceChanged}
                                    error={distanceError}
                                    helperText={distanceError ? distanceError : ""}
                                    slotProps={{
                                        input: {
                                            endAdornment: <InputAdornment position="end">km</InputAdornment>,
                                        },
                                    }}
                                    sx={{ flexGrow: 1 }}
                                />
                            </Grid>
                        </Grid>
                        <Grid container spacing={2} mb={2.5}>
                            <Grid item xs={12} sm={6} sx={{ display: 'flex', flexDirection: 'row' }}>
                                <TextField
                                    required
                                    id="numOfCars"
                                    label="Number of Cars"
                                    value={numOfCars}
                                    onChange={handleNumOfCarsChanged}
                                    error={numOfCarsError}
                                    helperText={numOfCarsError ? numOfCarsError : ""}
                                    slotProps={{
                                        input: {
                                            endAdornment: <InputAdornment position="end">spaces</InputAdornment>,
                                        },
                                    }}
                                    sx={{ flexGrow: 1 }}
                                />
                            </Grid>
                            <Grid item xs={12} sm={6} sx={{ display: 'flex', flexDirection: 'row' }}>
                                <TextField
                                    required
                                    id="propertyCount"
                                    label="Property Count"
                                    value={propertyCount}
                                    onChange={handlePropertyCountChanged}
                                    error={propertyCountError}
                                    helperText={propertyCountError ? propertyCountError : ""}
                                    slotProps={{
                                        input: {
                                            endAdornment: <InputAdornment position="end">properties</InputAdornment>,
                                        },
                                    }}
                                    sx={{ flexGrow: 1 }}
                                />
                            </Grid>
                        </Grid>
                        <Button variant="contained" type="submit" onClick={validateForm} sx={{ width: '100%', mt: 3 }}>
                            Submit
                        </Button>
                    </Box>
                </Box>
                <Box sx={boxStyles} mt={2}>
                    <Typography variant="h6" component="h2">
                        Line Chart
                    </Typography>
                    <Box sx={{ position: 'relative', width: '100%', height: '50vh' }}>
                        <Line data={data} options={options} />
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};

export default LineChartComponent;
