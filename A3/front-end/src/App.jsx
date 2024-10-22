import { BrowserRouter } from "react-router-dom";

import MainRoute from "./MainRoute";

import NavBar from "./components/NavBar";
import Footer from "./components/Footer";

function App() {
  return (
    <BrowserRouter>
      <div className="">
        <NavBar />
        <MainRoute />
        <Footer />
      </div>
    </BrowserRouter>
    
  );
}

export default App;
