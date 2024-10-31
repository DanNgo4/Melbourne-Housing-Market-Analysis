import { useState, useEffect } from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import axios from "axios";

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const Donut = () => {
  const [layerInput, setLayerInput] = useState('');
  const [labelInput, setLabelInput] = useState('');
  const [highlightedData, setHighlightedData] = useState(null);
  const [dataset, setDataset] = useState([]); // Use state for dataset
  const [data, setData] = useState({
    labels: ["h", "t", "u"],
    datasets: [],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:8000/donut-data");
        const parsedData = JSON.parse(res.data); // Parse the string into a JSON object
        setDataset(parsedData); // Set the fetched data to state
      } catch (e) {
        console.error("Error fetching data for donut:", e);
      }
    };
    fetchData(); // Call the fetchData function
  }, []); // Empty dependency array ensures this runs once on mount

  const priceRanges = [
    { label: '$500,000 - $1,000,000', min: 500000, max: 1000000 },
    { label: '$1,000,000 - $2,000,000', min: 1000000, max: 2000000 },
    { label: '$2,000,000 - $3,000,000', min: 2000000, max: 3000000 },
    { label: '> $3,000,000', min: 3000000, max: Infinity },
  ];

  const colours = [
    "#FF6384", 
    "#36A2EB", 
    "#FFCE56"
  ];

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
        cutout: `${70 - i * 20}%`,
        radius: `${85 - i * 20}%`,
        datalabels: {
          anchor: 'center',
        },
      };
    });

    setData({ labels: ["h", "t", "u"], datasets }); // Update chart data
  }, [dataset]); // Run this effect when dataset changes

  const options = {
    plugins: {
      tooltip: {
        callbacks: {
          label: (tooltipItem) => `${tooltipItem.dataset.label}: ${tooltipItem.raw}%`,
        },
      },
      legend: {
        position: 'top',
      },
      datalabels: {
        display: (context) => context.dataset.data[context.dataIndex] > 0,
        font: {
          weight: 'bold',
        },
        padding: 6,
        formatter: Math.round,
      },
    },
    cutout: '20%',
    layout: {
      padding: 20,
    },
  };

  // Highlight function
  const handleHighlight = () => {
    const selectedLayerIndex = parseInt(layerInput, 10) - 1;
    const matchingLabels = labelInput ? [labelInput.toLowerCase()] : data.labels.map((label) => label.toLowerCase());

    // Clone data to avoid modifying the original
    const newData = { ...data, datasets: data.datasets.map((dataset, layerIndex) => ({
        ...dataset,
        backgroundColor: dataset.backgroundColor.map((color, labelIndex) => {
            const labelMatches = matchingLabels.includes(data.labels[labelIndex].toLowerCase());
            const isLayerMatch = selectedLayerIndex === layerIndex || layerInput === '';
            return labelMatches && isLayerMatch ? 'rgba(255, 0, 0, 0.7)' : color; // Red tint for highlight
        }),
        borderColor: dataset.backgroundColor.map((color, labelIndex) => {
            const labelMatches = matchingLabels.includes(data.labels[labelIndex].toLowerCase());
            const isLayerMatch = selectedLayerIndex === layerIndex || layerInput === '';
            return labelMatches && isLayerMatch ? 'rgba(0, 0, 0, 1)' : color; // Black border for highlight
        }),
        borderWidth: dataset.data.map((_, labelIndex) => {
            const labelMatches = matchingLabels.includes(data.labels[labelIndex].toLowerCase());
            const isLayerMatch = selectedLayerIndex === layerIndex || layerInput === '';
            return labelMatches && isLayerMatch ? 3 : 1; // Thicker border for highlight
        })
    })) };

    // Display highlighted info
    const highlighted = newData.datasets.flatMap((dataset, layerIndex) =>
        dataset.data
            .map((value, labelIndex) => {
                if (newData.datasets[layerIndex].backgroundColor[labelIndex] === 'rgba(255, 0, 0, 0.7)') {
                    return { layer: dataset.label, label: data.labels[labelIndex], value };
                }
                return null;
            })
            .filter(Boolean)
    );

    setHighlightedData(highlighted);
    setData(newData);  // Update the chart data with the highlighted segments
  };

  return (
    <div style={{ width: '800px', height: '800px' }}>
      <input
        type="number"
        placeholder="Enter layer number (1-4)"
        value={layerInput}
        onChange={(e) => setLayerInput(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter label name"
        value={labelInput}
        onChange={(e) => setLabelInput(e.target.value)}
      />
      <button onClick={() => handleHighlight()}>Highlight</button>

      <Doughnut data={data} options={options} />

      {highlightedData && (
        <div style={{ marginTop: '20px' }}>
          <h3>Highlighted Information</h3>
          {highlightedData.length > 0 ? (
            highlightedData.map((item, index) => (
              <p key={index}>
                Layer: {item.layer}, Label: {item.label}, Value: {item.value}
              </p>
            ))
          ) : (
            <p>No matches found</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Donut;
