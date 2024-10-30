import { useState } from "react";
import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const MultiLayerDoughnutChart = () => {
  const [layerInput, setLayerInput] = useState('');
  const [labelInput, setLabelInput] = useState('');
  const [highlightedData, setHighlightedData] = useState(null);

  const [data, setData] = useState({
    labels: ["House", "Townhouse", "Unit"],
    datasets: [
      {
        label: 'Layer 1',
        data: Array.from({ length: 3 }, () => Math.floor(Math.random() * 100)),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
        borderColor: ['#FF6384', '#36A2EB', '#FFCE56'],
        borderWidth: 1,
        cutout: '60%',
        radius: '85%',
      },
      {
        label: 'Layer 2',
        data: Array.from({ length: 3 }, () => Math.floor(Math.random() * 100)),
        backgroundColor: ['#FF9F40', '#4BC0C0', '#9966FF'],
        borderColor: ['#FF9F40', '#4BC0C0', '#9966FF'],
        borderWidth: 1,
        cutout: '50%',
        radius: '70%',
      },
      {
        label: 'Layer 3',
        data: Array.from({ length: 3 }, () => Math.floor(Math.random() * 100)),
        backgroundColor: ['#66FF66', '#99CCFF', '#FF6666'],
        borderColor: ['#66FF66', '#99CCFF', '#FF6666'],
        borderWidth: 1,
        cutout: '30%',
        radius: '55%',
      },
      {
        label: 'Layer 4',
        data: Array.from({ length: 3 }, () => Math.floor(Math.random() * 100)),
        backgroundColor: ['#CCCCFF', '#FF99FF', '#66B2FF'],
        borderColor: ['#CCCCFF', '#FF99FF', '#66B2FF'],
        borderWidth: 1,
        cutout: '20%',
        radius: '40%',
      },
    ],
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

export default MultiLayerDoughnutChart;
