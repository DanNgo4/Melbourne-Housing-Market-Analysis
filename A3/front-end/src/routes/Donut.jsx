import { useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const Donut = () => {
  const [layerInput, setLayerInput] = useState('');
  const [labelInput, setLabelInput] = useState('');
  const [highlightedData, setHighlightedData] = useState(null);

  const dataset = [
    { Type: "House", Price: 750000 },
    { Type: "House", Price: 1250000 },
    { Type: "House", Price: 2200000 },
    { Type: "House", Price: 3200000 },
    { Type: "House", Price: 890000 },
    { Type: "House", Price: 1780000 },
    { Type: "House", Price: 2600000 },
    { Type: "House", Price: 4000000 },
    { Type: "Townhouse", Price: 850000 },
    { Type: "Townhouse", Price: 1500000 },
    { Type: "Townhouse", Price: 2700000 },
    { Type: "Townhouse", Price: 3300000 },
    { Type: "Townhouse", Price: 930000 },
    { Type: "Townhouse", Price: 1450000 },
    { Type: "Townhouse", Price: 2100000 },
    { Type: "Townhouse", Price: 3050000 },
    { Type: "Townhouse", Price: 1250000 },
    { Type: "Unit", Price: 600000 },
    { Type: "Unit", Price: 1400000 },
    { Type: "Unit", Price: 2300000 },
    { Type: "Unit", Price: 3500000 },
    { Type: "Unit", Price: 710000 },
    { Type: "Unit", Price: 950000 },
    { Type: "Unit", Price: 1100000 },
    { Type: "Unit", Price: 1900000 },
    { Type: "Unit", Price: 2550000 },
    { Type: "Unit", Price: 4100000 },
    { Type: "House", Price: 510000 },
    { Type: "Townhouse", Price: 780000 },
    { Type: "Unit", Price: 680000 },
  ];
  

  const priceRanges = [
    { label: '$500,000 - $1,000,000', min: 5000000, max: 1000000 },
    { label: '$1,000,000 - $2,000,000', min: 1000000, max: 2000000 },
    { label: '$3,000,000 - $3,000,000', min: 2000000, max: 3000000 },
    { label: '> $3,000,000', min: 3000000, max: Infinity },
  ];

  const houseTypes = ["House", "Townhouse", "Unit"];

  const red = "#FF6384"
  const blue = '#36A2EB'
  const yellow = '#FFCE56'

  const colours = [
    [red, blue, yellow],
    [red, blue, yellow],
    [red, blue, yellow],
    [red, blue, yellow]
  ]

   // Dynamically calculate counts for each type within each price range
   const datasets = priceRanges.map((range, i) => {
    // Get total count within the price range
    const totalInRange = dataset.filter(
      (item) => item.Price >= range.min && item.Price < range.max
    ).length;
  
    // Calculate percentage of each type within the range
    const percentages = houseTypes.map((type) => {
      const countOfTypeInRange = dataset.filter(
        (item) => item.Type === type && item.Price >= range.min && item.Price < range.max
      ).length;
  
      // Calculate percentage
      return totalInRange > 0 ? (countOfTypeInRange / totalInRange) * 100 : 0;
    });

    return {
      label: range.label,
      data: percentages.map((percentage) => parseFloat(percentage.toFixed(2))),
      backgroundColor: colours[i],
      borderColor: colours[i],
      borderWidth: 1,
      cutout: `${70 - i * 20}%`,
      radius: `${85 - i * 20}%`,
      datalabels: {
        anchor: 'center',
      },
    };
  });

  const [data, setData] = useState({
    labels: houseTypes,
    datasets: datasets,
  });

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
        backgroundColor: (context) => context.dataset.backgroundColor,
        borderColor: 'white',
        borderRadius: 25,
        borderWidth: 2,
        color: 'white',
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
      <button onClick={handleHighlight}>Highlight</button>

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
