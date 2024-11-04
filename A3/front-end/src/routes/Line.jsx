import { React, useState, useEffect } from "react";
import { Box, TextField, Typography, InputAdornment, Grid, CircularProgress } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CustomButton from "../components/CustomButton";
import useErrorLog from "../hooks/useErrorLog";
import useFormInput from "../hooks/useFormInput";

Chart.register(...registerables);

//The standard styles for the two main boxes on this component
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
    //Predicted Square metres
    const [predictedSquareMetres, setPredictedSquareMetres] = useState([]);

    //All predicted prices
    const [predictedPrices, setPredictedPrices] = useState([]);

    //All predicted values
    const [predictedValuesData, setPredictedValuesData] = useState([]);

    //The price predicted from user input
    const [yourPredictedPrice, setYourPredictedPrice] = useState(false);
    const [yourPredictedPriceIndex, setYourPredictedPriceIndex] = useState(false);

    //Loading for the chart
    const [loading, setLoading] = useState(true);

    //use states for the form
    const { values, handleChange, _ } = useFormInput(); 
    const { squareMetres, distance, rooms, cars } = values;

    //use state errors for the form
    const [squareMetresError, setSquareMetresError] = useState(false);
    const [distanceError, setDistanceError] = useState(false);
    const [roomsError, setRoomsError] = useState(false);
    const [carsError, setCarsError] = useState(false);

    // Custom hook for logging errors
    const errorLog = useErrorLog();

    useEffect(() => {
        if (predictedValuesData.length === 0) {
            axios.get('http://localhost:8000/predicted_values/')
                .then(response => {
                    const sortedData = Object.values(response.data).sort((a, b) => a.Landsize - b.Landsize);
                    setPredictedValuesData(sortedData);
                })
                .catch(error => errorLog(error, "Getting prediceted_values"));
        }
    }, [errorLog, predictedValuesData]);

    useEffect(() => {
        if (predictedValuesData.length > 0 && predictedPrices.length === 0) {
            Promise.all(
                predictedValuesData.map(dataRow => {
                    predictedSquareMetres.push(dataRow["Landsize"]);
                    const url = `http://localhost:8000/predict_price/${dataRow["Landsize"]}/${dataRow["Distance"]}/${dataRow["Room"]}/${dataRow["Car"]}/`;
                    return axios.get(url).then(res => res.data.predicted_price);
                })
            ).then(predictedPrices => {
                setPredictedPrices(predictedPrices);
                setLoading(false)
            }).catch(error => errorLog(error, "Predicting House Price"));
        }
    }, [predictedValuesData, errorLog, predictedPrices, predictedSquareMetres]);

    const validateForm = () => {
        handleSquareMetresChanged({ target: { value: squareMetres } });
        handleDistanceChanged({ target: { value: distance } });
        handleRoomsChanged({ target: { value: rooms } });
        handleCarsChanged({ target: { value: cars } });
    };

    //Handles the submission of the form
    const handleSubmit = e => {
        //Prevent the default reload page behavior
        e.preventDefault();
        //Validates form
        validateForm();
        if (!squareMetresError && !distanceError && !roomsError && !carsError) {
            //Gets the new prediction
            axios.get(`http://localhost:8000/predict_price/${squareMetres}/${distance}/${rooms}/${cars}/`)
                .then(res => {
                    //Sets the prediction
                    setYourPredictedPrice([{ x: squareMetres, y: res.data.predicted_price }]);
                    addNewPrediction(res.data.predicted_price);
                }).catch(error => errorLog(error, "Submitting entry for new house price prediction"));
        }
    };

    //Saves the current prediction
    const saveCurrentPrediction = () => {
        //Resets the your predicted prices usestates
        setYourPredictedPriceIndex(false)
        setYourPredictedPrice(false)

        //Posts new row
        let new_values = { Landsize: parseFloat(squareMetres), Distance: parseFloat(distance), Room: parseInt(rooms), Car: parseInt(cars) }
        axios.post('http://localhost:8000/add-predicted-values/', new_values)
            .then(response => {
                console.log("new values added successfully:", response.data);
            })
            .catch(error => errorLog(error, "Adding new values"));
    }

    //Adds a temporary prediction to the line graph
    const addNewPrediction = (price) => {
        //Removes old temp prediction
        if (yourPredictedPriceIndex !== undefined) {
            predictedValuesData.splice(yourPredictedPriceIndex, 1)
            predictedSquareMetres.splice(yourPredictedPriceIndex, 1)
            predictedPrices.splice(yourPredictedPriceIndex, 1)
        }
        //Adds a new one, sorts and sets it 
        predictedValuesData.push({ Landsize: squareMetres, Distance: distance, Room: rooms, Car: cars })
        const sortedData = Object.values(predictedValuesData).sort((a, b) => a.Landsize - b.Landsize);
        setPredictedValuesData(sortedData)

        //Resorts where it should be in metres
        const newPredictedSquareMetres = []
        sortedData.map(dataRow => {
            newPredictedSquareMetres.push(dataRow["Landsize"]);
        })
        setPredictedSquareMetres(newPredictedSquareMetres);

        //Inserts the temporary prediction in prices
        predictedPrices.splice(newPredictedSquareMetres.indexOf(squareMetres), 0, price);

        //Sets the relvant index to be removed next time
        setYourPredictedPriceIndex(newPredictedSquareMetres.indexOf(squareMetres));
    };

    //Validates Square metres
    const handleSquareMetresChanged = e => {
        handleChange("squareMetres")(e);
        if (e.target.value === '') {
            setSquareMetresError("Please enter square footage of property!");
        } else if (!/^[1-9][0-9]*(\.[0-9]+)?$/.test(e.target.value)) {
            setSquareMetresError("Please enter a numerical value greater than 0 for square footage!");
        } else {
            setSquareMetresError(false);
        }
    };

    //Validates distance
    const handleDistanceChanged = e => {
        handleChange("distance")(e);
        if (e.target.value === '') {
            setDistanceError("Please enter distance from CBD!");
        } else if (!/^[0-9]+(\.[0-9]+)?$/.test(e.target.value)) {
            setDistanceError("Please enter a numerical value 0 or greater for distance from CBD!");
        } else {
            setDistanceError(false);
        }
    };

    //Validates rooms changed
    const handleRoomsChanged = e => {
        handleChange("rooms")(e);
        if (e.target.value === '') {
            setRoomsError("Please enter rooms!");
        } else if (!/^(10|[1-9])$/.test(e.target.value)) {
            setRoomsError("Please enter 1 - 10 for rooms!");
        } else {
            setRoomsError(false);
        }
    };

    //Validates cars changed
    const handleCarsChanged = e => {
        handleChange("cars")(e);
        if (e.target.value === '') {
            setCarsError("Please enter cars!");
        } else if (!/^[1-5]$/.test(e.target.value)) {
            setCarsError("Please enter 1 - 5 for cars!");
        } else {
            setCarsError(false);
        }
    };

    //Dynamic point radius's for the line graph dependent on screen size
    const pointRadius = window.innerWidth < 600 ? 3 : 5;
    const yourPredictedPointRadius = window.innerWidth < 600 ? 5 : 8;

    //Dynamic size for circular progress
    const progressSize = window.innerWidth < 600 ? 150 : 300;

    // Line Chart Data and Options
    const data = {
        labels: predictedSquareMetres,
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

    //options for the line chart
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
                    <Box sx={{ width: '100%' }}>
                        <ThemeProvider theme={noErrorHeightTheme}>
                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6} mb={4} sx={{ display: 'flex', flexDirection: 'row' }}>
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
                                
                                <Grid item xs={12} sm={6} mb={4} sx={{ display: 'flex', flexDirection: 'row' }}>
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

                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6} mb={4} sx={{ display: 'flex', flexDirection: 'row' }}>
                                    <TextField
                                        required
                                        id="rooms"
                                        label="Rooms"
                                        value={rooms}
                                        onChange={handleRoomsChanged}
                                        error={roomsError}
                                        helperText={roomsError ? roomsError : ""}
                                        sx={{ flexGrow: 1 }}
                                    />
                                </Grid>
                                <Grid item xs={12} sm={6} mb={4} sx={{ display: 'flex', flexDirection: 'row' }}>
                                    <TextField
                                        required
                                        id="cars"
                                        label="car"
                                        value={cars}
                                        onChange={handleCarsChanged}
                                        error={carsError}
                                        helperText={carsError ? carsError : ""}
                                        sx={{ flexGrow: 1 }}
                                    />
                                </Grid>
                            </Grid>
                        </ThemeProvider>

                        <div className="mt-3">
                            <CustomButton onClick={validateForm} type="submit">
                                Predict Price
                            </CustomButton>
                        </div>

                        <div className="mt-3">
                            <CustomButton disabled={typeof yourPredictedPrice === "boolean"} onClick={saveCurrentPrediction}>
                                Save predicted values
                            </CustomButton>
                        </div>
                    </Box>
                </Box>

                <Box sx={boxStyles} mt={2}>
                    <Typography variant="h6" component="h2">
                        Line Chart
                    </Typography>
                    <Box sx={{ position: 'relative', width: '100%', height: { xs: '35vh', md: '50vh' } }}>
                        {loading ? (
                            <CircularProgress size={progressSize} sx={{ position: 'absolute', top: '25%', left: '25%', transform: 'translate(-50%, -50%)' }} ></CircularProgress>
                        ) : (
                            <Line data={data} options={options} />
                        )}
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};

export default LineChartComponent;
