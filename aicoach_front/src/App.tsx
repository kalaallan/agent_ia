import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Appzone from "./pages/Appzone";
import Login from "./pages/Login";
import Register from "./pages/Register";

const App = () => {
  return (
    <Router>
      <div className="">
        <Routes>
          <Route path="/" element={<Appzone />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;