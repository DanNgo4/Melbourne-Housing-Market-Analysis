import { Routes, Route } from "react-router-dom";

import Home from "./routes/HomePage";
import Model from "./routes/ModelPage";

import ScrollToTop from "./components/ScrollToTop";

const MainRoute = () => {
    return (
        <>
            <ScrollToTop />
            <Routes>
                <Route path="/"      element={<Home />} />
                <Route path="/model" element={<Model />} />
            </Routes>
        </>
    );
};

export default MainRoute;
