import { Routes, Route } from "react-router-dom";

import Home from "./routes/HomePage";
import Model from "./routes/ModelPage";
import Line from "./routes/Line";
import Heat from "./routes/Heat";
import Donut from "./routes/Donut";

import ScrollToTop from "./components/ScrollToTop";

const MainRoute = () => {
    return (
        <>
            <ScrollToTop />
            <Routes>
                <Route path="/"       element={<Home />} />
                <Route path="/model"  element={<Model />} />
                <Route path="/line"   element={<Line />} />
                <Route path="/heat"   element={<Heat />} />
                <Route path="/donut"  element={<Donut />} />
            </Routes>
        </>
    );
};

export default MainRoute;
