import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet.heat';

const Heatmap = ({ geojsonData }) => {
  const map = useMap();
  const [selectedYear, setSelectedYear] = useState("2017");

  useEffect(() => {
    // Clear existing layers before adding new ones
    map.eachLayer((layer) => {
      if (layer instanceof L.heatLayer || layer instanceof L.GeoJSON) {
        map.removeLayer(layer);
      }
    });

    // Prepare heatmap data
    const heatmapData = geojsonData.features
      .map(feature => {
        const coords = JSON.parse(feature.properties.geo_point_2d);
        const price = feature.properties[`${selectedYear} Median Price`];
        if (price) {
          return [coords.lat, coords.lon, price];
        }
        return null;
      })
      .filter(point => point !== null);

    let heatLayer;
    if (heatmapData.length > 0) {
      heatLayer = L.heatLayer(heatmapData, { radius: 25 }).addTo(map);
    }

    const geojsonLayer = L.geoJSON(geojsonData, {
      style: function (feature) {
        const price = feature.properties[`${selectedYear} Median Price`] || 0;
        return {
          color: '#000',
          weight: 2,
          fillColor: getColor(price),
          fillOpacity: 0.5,
        };
      },
      onEachFeature: (feature, layer) => {
        const cityNameArray = JSON.parse(feature.properties.lga_name_long);
  const cityName = cityNameArray[0];
        const price = feature.properties[`${selectedYear} Median Price`];
        const popupContent = `City Council: ${cityName}<br/>Median Price: $${price}`;
        layer.bindPopup(popupContent);
        layer.on('click', () => {
          layer.openPopup();
        });
      }
    }).addTo(map);

    return () => {
      map.removeLayer(heatLayer);
      map.removeLayer(geojsonLayer);
    };
  }, [geojsonData, map, selectedYear]);

  function getColor(price) {
    return price > 1000000 ? '#FF0000' : 
           price > 800000  ? '#FF7F00' : 
           price > 600000  ? '#FFFF00' : 
           price > 400000  ? '#7FFF00' : 
           price > 200000  ? '#00FF00' : 
                             '#808080'; // Default color for undefined or low prices
  }

  return (
    <>
      <div style={{ position: 'absolute', bottom: 100, right: 10, zIndex: 1000, background: 'white', padding: '10px', borderRadius: '5px' }}>
        <h4>Price Legend</h4>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ backgroundColor: '#FF0000', width: '20px', height: '20px', marginRight: '5px' }}></div>
            <span> &gt; $1,000,000</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ backgroundColor: '#FF7F00', width: '20px', height: '20px', marginRight: '5px' }}></div>
            <span> $800,000 - $1,000,000</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ backgroundColor: '#FFFF00', width: '20px', height: '20px', marginRight: '5px' }}></div>
            <span> $600,000 - $800,000</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ backgroundColor: '#7FFF00', width: '20px', height: '20px', marginRight: '5px' }}></div>
            <span> $400,000 - $600,000</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ backgroundColor: '#00FF00', width: '20px', height: '20px', marginRight: '5px' }}></div>
            <span> $200,000 - $400,000</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ backgroundColor: '#808080', width: '20px', height: '20px', marginRight: '5px' }}></div>
            <span> Undefined / Low Price</span>
          </div>
        </div>
      </div>
      <div style={{ position: 'absolute', top: 100, right: 10, zIndex: 1000, background: 'white', padding: '10px', borderRadius: '5px' }}>
        <label htmlFor="yearSelector">Select Year: </label>
        <select id="yearSelector" value={selectedYear} onChange={(e) => setSelectedYear(e.target.value)}>
          <option value="2016">2016</option>
          <option value="2017">2017</option>
          <option value="2018">2018</option>
        </select>
      </div>
    </>
  );
};

const HeatmapMap = ({ geojsonData }) => {
  return (
    <MapContainer center={[-38, 145.0]} zoom={9} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <Heatmap geojsonData={geojsonData} />
    </MapContainer>
  );
};

export default HeatmapMap;
