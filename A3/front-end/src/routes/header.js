import React from 'react';

const Header = () => {
  return (
    <header style={{ backgroundColor: '#4CAF50', color: 'white', padding: '10px 20px', textAlign: 'center', position: 'fixed', top: 0, left: 0, width: '100%', zIndex: 1000 }}>
      <h1 style={{ margin: '0' }}>Melbourne Real Estate Heatmap</h1>
      <p style={{ margin: '5px 0' }}>Explore median property prices in your area</p>
    </header>
  );
};

export default Header;

