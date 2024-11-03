import { BrowserRouter } from "react-router-dom";

import MainRoute from "./MainRoute";

import NavBar from "./components/NavBar";
import ErrorBoundary from "./components/ErrorBoundary";

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <div>
          <NavBar />
          <MainRoute />
        </div>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
