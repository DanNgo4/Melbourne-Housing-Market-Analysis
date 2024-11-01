import { useState, useEffect } from "react";

import axios from "axios";

import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

import { Button, Typography, Box, Select, MenuItem, InputLabel, FormControl } from "@mui/material";

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const Donut = () => {
  const [priceRangeInput, setPriceRangeInput] = useState("");
  const [houseTypeInput, setHouseTypeInput] = useState("");
  const [highlightedData, setHighlightedData] = useState(null);
  const [dataset, setDataset] = useState([]); 
  const [queryHistory, setQueryHistory] = useState([]);

  const typeMapping = {
    h: "House",
    t: "Townhouse",
    u: "Unit"
  };
  
  // Convert labels from ["h", "t", "u"] to ["House", "Townhouse", "Unit"]
  const mappedLabels = ["h", "t", "u"].map(label => typeMapping[label]);

  const priceRanges = [
    { label: "$500,000 - $1,000,000", min: 500000, max: 1000000 },
    { label: "$1,000,000 - $2,000,000", min: 1000000, max: 2000000 },
    { label: "$2,000,000 - $3,000,000", min: 2000000, max: 3000000 },
    { label: "> $3,000,000", min: 3000000, max: Infinity },
  ];

  const colours = ["#FF6384", "#36A2EB", "#FFCE56"];

  const [data, setData] = useState({
      labels: mappedLabels,
      datasets: [],
  });

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

    const fetchHistory = async () => {
      try {
        const res = await axios.get("http://localhost:8000/query-history");
        setQueryHistory(res.data || []);  // Set initial history as an array if undefined
      } catch (e) {
        console.error("Error fetching query history:", e);
      }
    };
    fetchHistory();
  }, []); 

  useEffect(() => {
    const datasets = priceRanges.map((range, i) => {
        const totalInRange = dataset.filter(
            (item) => item.Price >= range.min && item.Price < range.max
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
            cutout: `${50 - i * 12}%`, 
            radius: `${70 - i * 10}%`, 
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
  
    const queryDetails = {
      priceRange: priceRangeInput || "All",
      houseType: houseTypeInput || "All",
      highlighted
    };
  
    try {
      await axios.post("http://localhost:8000/save-query", queryDetails);
      console.log("Query saved successfully:", queryDetails);  // Add this line for debugging

      setQueryHistory((prev) => [...(prev || []), queryDetails]);  // Ensure prev is an array
    } catch (e) {
      console.error("Error saving query:", e);
    }
  };

  useEffect(() => {
    console.log("Current query history:", queryHistory);
  }, [queryHistory]);
  
  return (
    <div className="grid grid-cols-3 gap-5 p-5">
      {/* Left: Description */}
      <Box className="col-span-1 p-4 bg-gray-100 rounded shadow">
        <Typography variant="h5" className="font-bold">About This Chart</Typography>
        <Typography className="mt-3">
          This chart displays the percentage distribution of house types across price ranges.
          Use the controls to filter and highlight specific segments based on your selections.
        </Typography>
      </Box>

      <Box className="flex flex-col items-center w-full max-w-lg space-y-4">
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

      <div className="w-full max-w-xl mt-5">
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

      <Box className="col-span-1 p-4 bg-gray-100 rounded shadow">
        <Typography variant="h5" className="font-bold">Query History</Typography>
        <div className="mt-3 space-y-2">
          {queryHistory.length > 0 ? (
            queryHistory.map((query, index) => (
              <Typography key={index} className="text-sm">
                Price Range: {query.priceRange}, House Type: {query.houseType}, 
                Highlighted: {query.highlighted.map((item) => `${item.label} (${item.value}%)`).join(", ")}
              </Typography>
            ))
          ) : (
            <Typography className="text-sm text-center">No query history available.</Typography>
          )}
        </div>
      </Box>
    </div>
  );
};

export default Donut;
