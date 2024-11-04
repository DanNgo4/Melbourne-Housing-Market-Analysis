import { Routes, Route } from "react-router-dom";

import Home from "./routes/HomePage";
import Line from "./routes/Line";
import Donut from "./routes/Donut";
import Heat from "./routes/Heat";

import ScrollToTop from "./components/ScrollToTop";

const MainRoute = () => {
    return (
        <>
            <ScrollToTop />
            <Routes>
                <Route path="/"       element={<Home />} />
                <Route path="/line"   element={<Line />} />
                <Route path="/heat"   element={<Heat />} />
                <Route path="/donut"  element={<Donut />} />
            </Routes>
        </>
    );
};

export default MainRoute;
