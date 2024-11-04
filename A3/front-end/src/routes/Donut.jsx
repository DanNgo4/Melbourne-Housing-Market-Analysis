import { useState, useEffect } from "react";

import axios from "axios";

import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

import { Typography, Box, TextField, InputAdornment } from "@mui/material";

import CustomButton from "../components/CustomButton";
import InfoSection from "../components/DonutPage/InfoSection";
import DropdownInput from "../components/DonutPage/DropdownInput";

import useErrorLog from "../hooks/useErrorLog";
import useFormInput from "../hooks/useFormInput";

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const Donut = () => {
  const [highlightedData, setHighlightedData] = useState(null);
  const [predictedType, setPredictedType] = useState("");

  // Hook to manage data fetched from server
  const [dataset, setDataset] = useState([]); 

  const { values, handleChange, resetForm } = useFormInput();
  const {
    priceRangeInput,
    houseTypeInput,
    squareMetres,
    distance,
    rooms,
    cars,
  } = values;

  const [squareMetresError, setSquareMetresError] = useState("");
  const [distanceError, setDistanceError] = useState("");
  const [roomsError, setRoomsError] = useState("");
  const [carsError, setCarsError] = useState("");

  const errorLog = useErrorLog();

  const typeMapping = {
    h: "House",
    t: "Townhouse",
    u: "Unit"
  };
  // Convert labels from ["h", "t", "u"] to ["House", "Townhouse", "Unit"]
  const mappedLabels = ["h", "t", "u"].map(label => typeMapping[label]);
  // Hook to manage processed data to the donut chart
  const [data, setData] = useState({
    labels: mappedLabels,
    datasets: [],
  });

  const priceRanges = [
    { label: "$500,000 - $1,000,000", min: 500000, max: 800000 },
    { label: "$1,000,000 - $2,000,000", min: 800000, max: 2000000 },
    { label: "$2,000,000 - $3,000,000", min: 2000000, max: 3000000 },
    { label: "> $3,000,000", min: 3000000, max: Infinity },
  ];

  const colours = ["#FF6384", "#36A2EB", "#FFCE56"];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:8000/donut-data");
        const parsedData = JSON.parse(res.data); 
        setDataset(parsedData); 
      } catch (e) {
        errorLog(e, "Fetching data for donut chart");
      }
    };
    fetchData(); 
  }, [errorLog]); 

  useEffect(() => {
    const datasets = priceRanges.map((range, i) => {
        const totalInRange = dataset.filter((item) => 
          (item.Price >= range.min) && (item.Price < range.max)
        ).length;

        const percentages = ["h", "t", "u"].map((type) => {
            const countOfTypeInRange = dataset.filter(
                (item) => item.Type === type &&
                item.Price >= range.min &&
                item.Price < range.max
            ).length;

            return (totalInRange > 0) 
              ? ((countOfTypeInRange / totalInRange) * 100) 
              : 0;
        });

        return {
            label: range.label,
            data: percentages.map((percentage) => parseFloat(percentage.toFixed(2))),
            backgroundColor: colours,
            borderColor: colours,
            borderWidth: 1,
            cutout: `${60 - i * 5}%`, 
            radius: `${100 - i * 10}%`, 
            datalabels: {
                anchor: "center",
            },
        };
    });

    setData({ labels: mappedLabels, datasets }); 
  }, [dataset, mappedLabels]);

  const options = {
    plugins: {
      tooltip: {
        callbacks: {
          label: (tooltipItem) => `${tooltipItem.dataset.label}: ${tooltipItem.raw}%`,
        },
      },
      legend: {
        position: "top",
      },
      datalabels: {
        display: (context) => context.dataset.data[context.dataIndex] > 0,
        font: {
          weight: "bold",
        },
        padding: 6,
        formatter: Math.round,
      },
    },
    cutout: "20%",
    layout: {
      padding: 20,
    },
  };

  // Highlight function
  const handleHighlight = async () => {
    const selectedLayerIndex = parseInt(priceRangeInput, 10) - 1;

    const matchingLabels = houseTypeInput 
      ? [typeMapping[houseTypeInput]] 
      : data.labels;
  
    // Generate new data to overwrite the old, un-highlighted one
    const newData = { 
      ...data, 

      datasets: data.datasets.map((dataset, layerIndex) => ({
        ...dataset,

        backgroundColor: dataset.backgroundColor,

        // Set border colour and width for matched layers/segments
        borderColor: dataset.backgroundColor.map((color, labelIndex) => {
          const labelMatches = matchingLabels.includes(data.labels[labelIndex]);
          const isLayerMatch = selectedLayerIndex === layerIndex || priceRangeInput === "";
          return labelMatches && isLayerMatch ? "rgba(0, 0, 0, 1)" : color;
        }),

        borderWidth: dataset.data.map((_, labelIndex) => {
          const labelMatches = matchingLabels.includes(data.labels[labelIndex]);
          const isLayerMatch = selectedLayerIndex === layerIndex || priceRangeInput === "";
          return labelMatches && isLayerMatch ? 3 : 1;
        })
      })) 
    };
  
    // Generate an array of highlighted data points for displaying in-text underneath
    const highlighted = newData.datasets.flatMap((dataset, layerIndex) =>
      dataset.data
        .map((value, labelIndex) => {
          if (newData.datasets[layerIndex].borderWidth[labelIndex] === 3) {
            return { 
              layer: dataset.label, 
              label: data.labels[labelIndex], 
              value 
            };
          }
          
          return null;
        })
        .filter(Boolean)
    );
  
    setHighlightedData(highlighted);
    setData(newData);
  };

  // Reset the chart to normal with no highlights
  const clearHighlights = () => {
    resetForm(["priceRangeInput", "houseTypeInput"]);
    setHighlightedData([]);
    
    const resetData = {
      ...data,
      datasets: data.datasets.map((dataset) => ({
        ...dataset,
        borderColor: dataset.backgroundColor,
        borderWidth: dataset.data.map(() => 1),
      }))
    };
    
    setData(resetData);
  };

  // Validate form inputs for client-side validation
  const validateInputs = () => {
    let isValid = true;

    if (!squareMetres || isNaN(squareMetres) || squareMetres <= 0 || !Number.isInteger(parseFloat(squareMetres))) {
      setSquareMetresError("Enter a valid number for square metres.");
      isValid = false;
    } else {
      setSquareMetresError("");
    }

    if (!distance || isNaN(distance) || distance <= 0 || !Number.isInteger(parseFloat(distance))) {
      setDistanceError("Enter a valid number for distance.");
      isValid = false;
    } else {
      setDistanceError("");
    }

    if (!rooms || isNaN(rooms) || rooms <= 0 || !Number.isInteger(parseFloat(rooms))) {
      setRoomsError("Enter a valid integer for rooms.");
      isValid = false;
    } else {
      setRoomsError("");
    }

    if (cars === "" || isNaN(cars) || cars < 0 || !Number.isInteger(parseFloat(cars))) {
      setCarsError("Enter a valid integer for cars.");
      isValid = false;
    } else {
      setCarsError("");
    }

    return isValid;
  };

  const handlePredict = async () => {
    if (!validateInputs()) return;

    try {
      const res = await axios.get(`http://localhost:8000/predict_type/${squareMetres}/${distance}/${rooms}/${cars}`);
      setPredictedType(res.data.predicted_type);
    } catch (e) {
      errorLog(e, "Predicting House Type");
    }
  };
  
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-5 p-5">
      <InfoSection />

      <Box className="flex flex-col items-center w-full max-w-lg space-y-4 mx-auto">
        <Typography variant="h5" className="font-bold">
          Analyse House Types Distribution
        </Typography>

        <DropdownInput
          label="Choose Price Range"
          value={priceRangeInput}
          onChange={handleChange("priceRangeInput")}
          options={priceRanges.map((range, index) => ({ 
            label: range.label, 
            value: index + 1 
          }))}
        />

        <DropdownInput
          label="Choose House Type"
          value={houseTypeInput}
          onChange={handleChange("houseTypeInput")}
          options={Object.entries(typeMapping).map(([key, value]) => ({ 
            label: value, 
            value: key 
          }))}
        />

        <CustomButton color="primary" onClick={handleHighlight}>
          Highlight
        </CustomButton>

        <CustomButton color="secondary" onClick={clearHighlights}>
          Clear
        </CustomButton>

        <div className="w-full max-w-xs md:max-w-lg lg:max-w-xl mt-5">
          <Doughnut data={data} options={options} width={800} height={800} />
        </div>

        {highlightedData && (
          <Box className="mt-5 w-auto p-4 bg-gray-100 rounded shadow">
            <Typography variant="h6" className="font-bold text-center mb-2">Highlighted Information</Typography>
            {highlightedData.length > 0 
              ? (
                highlightedData.map((item, index) => (
                  <Typography key={index} className="text-sm">
                    Price Range: {item.layer}, House Type: {item.label}, Ratio: {item.value}%
                  </Typography>
                ))
              ) 
              : (
                <Typography className="text-sm text-center">No matches found</Typography>
              )
            }
          </Box>
        )}
      </Box>

      <Box className="col-span-1 p-4 bg-gray-100 rounded shadow max-w-md mx-auto">
        <Typography variant="h5" className="font-bold">Predict House Type</Typography>

        <form onSubmit={(e) => { 
          e.preventDefault(); 
          handlePredict(); 
        }}>
          <TextField
            label="Square Metres"
            value={squareMetres}
            onChange={handleChange("squareMetres")}
            error={!!squareMetresError}
            helperText={squareMetresError ? squareMetresError : ""}
            fullWidth
            margin="normal"
            slotProps={{
              input: {
                  endAdornment: <InputAdornment position="end">metres</InputAdornment>,
              },
            }}
          />

          <TextField
            label="Distance"
            value={distance}
            onChange={handleChange("distance")}
            error={!!distanceError}
            helperText={distanceError ? distanceError : ""}
            fullWidth
            margin="normal"
            slotProps={{
              input: {
                  endAdornment: <InputAdornment position="end">km</InputAdornment>,
              },
            }}
          />

          <TextField
            label="Rooms"
            value={rooms}
            onChange={handleChange("rooms")}
            error={!!roomsError}
            helperText={roomsError ? roomsError : ""}
            fullWidth
            margin="normal"
          />

          <TextField
            label="Cars"
            value={cars}
            onChange={handleChange("cars")}
            error={!!carsError}
            helperText={carsError ? carsError : ""}
            fullWidth
            margin="normal"
          />

          <CustomButton color="primary" type="submit">
            Predict Type
          </CustomButton>
        </form>

        {predictedType && (
          <Typography className="mt-4">
            Predicted House Type: { `${predictedType} (${typeMapping[predictedType]})`}
          </Typography>
        )}
      </Box>
    </div>
  );
};

export default Donut;
