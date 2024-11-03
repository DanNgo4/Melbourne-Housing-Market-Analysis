import { useState, useEffect } from "react";

import axios from "axios";

import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

import { Button, Typography, Box, Select, MenuItem, InputLabel, FormControl, TextField } from "@mui/material";

import InfoSection from "../components/DonutPage/InfoSection";

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const Donut = () => {
  const [priceRangeInput, setPriceRangeInput] = useState("");
  const [houseTypeInput, setHouseTypeInput] = useState("");
  const [highlightedData, setHighlightedData] = useState(null);
  const [dataset, setDataset] = useState([]); 
  const [squareMetres, setSquareMetres] = useState("");
  const [distance, setDistance] = useState("");
  const [rooms, setRooms] = useState("");
  const [cars, setCars] = useState("");
  const [predictedType, setPredictedType] = useState("");

  const typeMapping = {
    h: "House",
    t: "Townhouse",
    u: "Unit"
  };
  
  // Convert labels from ["h", "t", "u"] to ["House", "Townhouse", "Unit"]
  const mappedLabels = ["h", "t", "u"].map(label => typeMapping[label]);

  const [data, setData] = useState({
    labels: mappedLabels,
    datasets: [],
  });

  const priceRanges = [
    { label: "$500,000 - $1,000,000", min: 500000, max: 1000000 },
    { label: "$1,000,000 - $2,000,000", min: 1000000, max: 2000000 },
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
        console.error("Error fetching data for donut:", e);
      }
    };
    fetchData(); 
  }, []); 

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

            return totalInRange > 0 ? (countOfTypeInRange / totalInRange) * 100 : 0;
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
  }, [dataset]);

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
  
    const newData = { 
      ...data, 
      datasets: data.datasets.map((dataset, layerIndex) => ({
        ...dataset,
        backgroundColor: dataset.backgroundColor,
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
  
    const highlighted = newData.datasets.flatMap((dataset, layerIndex) =>
      dataset.data
        .map((value, labelIndex) => {
          if (newData.datasets[layerIndex].borderWidth[labelIndex] === 3) {
            return { layer: dataset.label, label: data.labels[labelIndex], value };
          }
          return null;
        })
        .filter(Boolean)
    );
  
    setHighlightedData(highlighted);
    setData(newData);
  };

  const clearHighlights = () => {
    setPriceRangeInput("");
    setHouseTypeInput("");
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

  const handlePredict = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/predict_type/${squareMetres}/${distance}/${rooms}/${cars}`);
      setPredictedType(res.data.predicted_type);
    } catch (error) {
      console.error("Error predicting house type:", error);
    }
  };
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 p-5">
      <InfoSection />

      <Box className="flex flex-col items-center w-full max-w-lg space-y-4 mx-auto">
        <Typography variant="h5" className="font-bold">
          Analyse House Types Distribution
        </Typography>

        <FormControl fullWidth variant="outlined" className="bg-white rounded">
          <InputLabel>Choose Price Range</InputLabel>

          <Select
            value={priceRangeInput}
            onChange={(e) => setPriceRangeInput(e.target.value)}
            label="Choose Price Range"
          >
            <MenuItem value="">All</MenuItem>

            {priceRanges.map((range, index) => (
              <MenuItem key={index} value={index + 1}>
                {range.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth variant="outlined" className="bg-white rounded">
          <InputLabel>Choose House Type</InputLabel>

          <Select
            value={houseTypeInput}
            onChange={(e) => setHouseTypeInput(e.target.value)}
            label="Choose House Type"
          >
            <MenuItem value="">All</MenuItem>

            {Object.entries(typeMapping).map(([key, value]) => (
              <MenuItem key={key} value={key}>
                {value}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button 
          variant="contained" 
          color="primary"
          onClick={() => handleHighlight()}
          className="w-full mt-2"
        >
          Highlight
        </Button>

        <Button 
          variant="contained" 
          color="secondary" 
          onClick={clearHighlights} 
          className="w-full mt-2"
        >
          Clear
        </Button>

        <div className="w-full max-w-xs md:max-w-lg lg:max-w-xl mt-5">
          <Doughnut data={data} options={options} width={800} height={800} />
        </div>

        {highlightedData && (
          <Box className="mt-5 w-auto p-4 bg-gray-100 rounded shadow">
            <Typography variant="h6" className="font-bold text-center mb-2">Highlighted Information</Typography>
            {highlightedData.length > 0 ? (
              highlightedData.map((item, index) => (
                <Typography key={index} className="text-sm">
                  Price Range: {item.layer}, House Type: {item.label}, Ratio: {item.value}%
                </Typography>
              ))
            ) : (
              <Typography className="text-sm text-center">No matches found</Typography>
            )}
          </Box>
        )}
      </Box>

      <Box className="col-span-1 p-4 bg-gray-100 rounded shadow max-w-md mx-auto">
        <Typography variant="h5" className="font-bold">Predict House Type</Typography>

        <form onSubmit={(e) => { e.preventDefault(); handlePredict(); }}>
          <TextField
            label="Square Metres"
            value={squareMetres}
            onChange={(e) => setSquareMetres(e.target.value)}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label="Distance"
            value={distance}
            onChange={(e) => setDistance(e.target.value)}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label="Rooms"
            value={rooms}
            onChange={(e) => setRooms(e.target.value)}
            fullWidth
            margin="normal"
            required
          />

          <TextField
            label="Cars"
            value={cars}
            onChange={(e) => setCars(e.target.value)}
            fullWidth
            margin="normal"
            required
          />

          <Button variant="contained" color="primary" type="submit" fullWidth>
            Predict Type
          </Button>
        </form>

        {predictedType && (
          <Typography className="mt-4">Predicted House Type: { `${predictedType} (${typeMapping[predictedType]})`}</Typography>
        )}
      </Box>
    </div>
  );
};

export default Donut;
