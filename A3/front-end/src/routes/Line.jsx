import { React, useState, useEffect } from "react";
import { Box, TextField, Button, Typography, InputAdornment, Grid } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';
import { ThemeProvider, createTheme } from '@mui/material/styles';

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

//Removes height and margins on the input errors
const noErrorHeightTheme = createTheme({
    components: {
        MuiFormHelperText: {
            styleOverrides: {
                root: {
                    marginTop: 0,
                    height: 0,
                },
            },
        },
    },
});

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


    const [predictedValuesData, setPredictedValuesData] = useState(() => {
        const storedData = sessionStorage.getItem('predictedValuesData');
        return storedData ? JSON.parse(storedData) : [];
    });

    //Predicted price
    const [yourPredictedPrice, setYourPredictedPrice] = useState([]);
    const [yourPredictedPriceIndex, setYourPredictedPriceIndex] = useState();

    // For useStates
    const [squareMetres, setSquareMetres] = useState("");
    const [distance, setDistance] = useState("");
    const [propertyCount, setPropertyCount] = useState("");

    // Form Errors
    const [squareMetresError, setSquareMetresError] = useState(false);
    const [distanceError, setDistanceError] = useState(false);
    const [propertyCountError, setPropertyCountError] = useState(false);

    useEffect(() => {
        if (predictedValuesData.length == 0) {
            // Fetch predicted values data from the API
            axios.get('http://localhost:8000/predicted_values/')
                .then(response => {
                    const sortedData = Object.values(response.data).sort((a, b) => a.Landsize - b.Landsize);
                    setPredictedValuesData(sortedData);
                    sessionStorage.setItem('predictedValuesData', JSON.stringify(sortedData));
                })
                .catch(error => {
                    console.error(error);
                });
        }
    }, []);

    useEffect(() => {
        // Only fetch predictions if not already in session storage
        if (predictedValuesData.length > 0 && predictedPrices.length == 0) {
            Promise.all(
                predictedValuesData.map(dataRow => {
                    predictedSquareMetres.push(dataRow["Landsize"]);

                    const url = `http://localhost:8000/predict/${dataRow["Landsize"]}/${dataRow["Distance"]}/${dataRow["Propertycount"]}/`;

                    return axios.get(url)
                        .then(res => res.data.predicted_price);
                })
            ).then(predictedPrices => {
                setPredictedPrices(predictedPrices);
                // Save to session storage
                sessionStorage.setItem('predictedSquareMetres', JSON.stringify(predictedSquareMetres));
                sessionStorage.setItem('predictedPrices', JSON.stringify(predictedPrices));
            }).catch(error => console.error(error));
        }
    }, [predictedValuesData]);

    // Function to validate the form
    const validateForm = () => {
        handleSquareMetresChanged({ target: { value: squareMetres } });
        handleDistanceChanged({ target: { value: distance } });
        handlePropertyCountChanged({ target: { value: propertyCount } });
    };

    // Handle the form submit
    const handleSubmit = e => {
        e.preventDefault();
        validateForm();
        if (e.target.checkValidity()) {
            axios.get(`http://localhost:8000/predict/${squareMetres}/${distance}/${propertyCount}/`)
                .then(res => {
                    setYourPredictedPrice([{ x: squareMetres, y: res.data.predicted_price }])
                    addNewPrediction(res.data.predicted_price)});
                });
        }
    };

    //Add the next prediction
    const addNewPrediction = (price) => {
        if (yourPredictedPriceIndex != undefined) {
            predictedValuesData.splice(yourPredictedPriceIndex, 1)
            predictedSquareMetres.splice(yourPredictedPriceIndex, 1)
            predictedPrices.splice(yourPredictedPriceIndex, 1)
        }

        predictedValuesData.push({Landsize: squareMetres, Distance: distance, Propertycount: propertyCount })

        const sortedData = Object.values(predictedValuesData).sort((a, b) => a.Landsize - b.Landsize);
        setPredictedValuesData(sortedData)
        const newPredictedSquareMetres = []
        sortedData.map(dataRow => {
            newPredictedSquareMetres.push(dataRow["Landsize"]);
        })
        setPredictedSquareMetres(newPredictedSquareMetres)
        predictedPrices.splice(newPredictedSquareMetres.indexOf(squareMetres), 0, price);
        setYourPredictedPriceIndex(newPredictedSquareMetres.indexOf(squareMetres))
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

    const pointRadius = window.innerWidth < 600 ? 3 : 5;
    const yourPredictedPointRadius = window.innerWidth < 600 ? 5 : 8;

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
                pointRadius: predictedPrices.map((_, index) => (index === yourPredictedPriceIndex ? 0 : pointRadius))
            },
            ...(yourPredictedPrice.length > 0 ? [{
                label: 'Your Prediction',
                data: yourPredictedPrice,
                backgroundColor: 'rgba(255, 176, 193, 0.6)',
                borderColor: 'rgba(255, 176, 193, 1)',
                borderWidth: 2,
                pointRadius: yourPredictedPointRadius,
                pointHoverRadius: yourPredictedPointRadius * 0.8,
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
                sx={{
                    display: "flex",
                    flexDirection: { xs: "column", lg: "row" },
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "90vh"
                }}
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
                                    id="propertyCount"
                                    label="Property Count"
                                    value={propertyCount}
                                    onChange={handlePropertyCountChanged}
                                    error={propertyCountError}
                                    helperText={propertyCountError ? propertyCountError : ""}
                                    sx={{ flexGrow: 1 }}
                                />
                            </Grid>
                        </ThemeProvider>
                        <Button variant="contained" type="submit" onClick={validateForm} sx={{ width: '100%', mt: 3 }}>
                            Submit
                        </Button>
                    </Box>
                </Box>
                <Box sx={boxStyles} mt={2}>
                    <Typography variant="h6" component="h2">
                        Line Chart
                    </Typography>
                    <Box sx={{ position: 'relative', width: '100%', height: { xs: '35vh', md: '50vh' } }}>
                        <Line data={data} options={options} />
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};

export default LineChartComponent;
