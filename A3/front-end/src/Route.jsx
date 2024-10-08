import { Routes, Route } from "react-router-dom";

import Home from "./routes/HomePage";
import PolyRegression from "./routes/PolyRegression";
import RFRegression from "./routes/RFRegression";
import XGBClassification from "./routes/XGBClassification";
import RFClassification from "./routes/RFClassification";

import ScrollToTop from "./components/ScrollToTop";

const Route = () => {
    return (
        <>
            <ScrollToTop />
            <Routes>
                <Route path="/"                             element={<Home />} />
                <Route path="/polynomial-regression"        element={<PolyRegression />} />
                <Route path="/random-forest-regression"     element={<RFRegression />} />
                <Route path="/random-forest-classification" element={<RFClassification />} />
                <Route path="/xgboost-classification"       element={<XGBClassification />} />
            </Routes>
        </>
    );
};

export default Route;
