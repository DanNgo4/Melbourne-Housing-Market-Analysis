import { BrowserRouter } from "react-router-dom";

import logo from './logo.svg';
import './App.css';

import MainRoute from "./MainRoute";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p className="text-red-500">
            This is HD Hunters
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    </BrowserRouter>
    
  );
}

export default App;
