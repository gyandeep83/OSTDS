import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import TimeSeriesChart from "./components/TimeSeriesChart";
import Heatmap from "./components/Heatmap";
import PieChart from "./components/PieChart";
import GeographicMap from "./components/GeographicMap";
import BarChart from "./components/BarChart";
import LineChart from "./components/LineChart";
import ScatterPlot from "./components/ScatterPlot";

function App() {
  return (
    <Router>
      <div style={{ fontFamily: "Arial, sans-serif" }}>
        <style>
          {`
            .nav-container {
              background-color: #f8f9fa;
              padding: 1rem;
              box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .nav-list {
              list-style: none;
              padding: 0;
              margin: 0;
              display: flex;
              gap: 1.5rem;
              flex-wrap: wrap;
            }
            
            .nav-link {
              text-decoration: none;
              color: #333;
              font-weight: 500;
              padding: 0.5rem 1rem;
              border-radius: 4px;
              transition: all 0.3s ease;
            }
            
            .nav-link:hover {
              background-color: #e2e6ea;
              color: #0056b3;
            }
            
            .nav-spacer {
              height: 2rem;
              border-bottom: 2px solid #eee;
              margin-bottom: 2rem;
            }
            
            h1 {
              color: #2c3e50;
              text-align: center;
              margin-bottom: 2rem;
              font-size: 2.5rem;
            }
          `}
        </style>

        <h1>COVID-19 Dashboard</h1>
        
        <nav className="nav-container">
          <ul className="nav-list">
            <li><Link className="nav-link" to="/">Time Series</Link></li>
            <li><Link className="nav-link" to="/heatmap">Heatmap</Link></li>
            <li><Link className="nav-link" to="/piechart">Pie Chart</Link></li>
            <li><Link className="nav-link" to="/geographic-map">Geographic Spread</Link></li>
            <li><Link className="nav-link" to="/bar-chart">Bar Chart</Link></li>
            <li><Link className="nav-link" to="/linechart">Case Fatality Ratio</Link></li>
            <li><Link className="nav-link" to="/scatter-plot">Scatter Plot</Link></li>
          </ul>
        </nav>
        
        <div className="nav-spacer" />

        <div style={{ padding: "0 2rem" }}>
          <Routes>
            <Route path="/" element={<TimeSeriesChart />} />
            <Route path="/heatmap" element={<Heatmap />} />
            <Route path="/piechart" element={<PieChart />} />
            <Route path="/geographic-map" element={<GeographicMap />} />
            <Route path="/bar-chart" element={<BarChart />} />
            <Route path="/linechart" element={<LineChart />} />
            <Route path="/scatter-plot" element={<ScatterPlot />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;