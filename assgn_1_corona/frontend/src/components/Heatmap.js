import React, { useState, useEffect } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const availableColumns = ["FIPS", "Confirmed", "Deaths", "Recovered", "Active", "Incident_Rate", "Case_Fatality_Ratio"];

const Heatmap = () => {
  const [imageSrc, setImageSrc] = useState("");
  const [selectedColumns, setSelectedColumns] = useState(["Confirmed", "Deaths", "Active"]);
  const [startDate, setStartDate] = useState(new Date("2021-01-01"));
  const [endDate, setEndDate] = useState(new Date("2021-12-31"));

  // Function to fetch heatmap
  const fetchHeatmap = () => {
    const columnParams = selectedColumns.map(col => `columns[]=${col}`).join("&");
    const url = `http://127.0.0.1:8000/api/correlation-heatmap/?${columnParams}&start_date=${startDate.toISOString().split("T")[0]}&end_date=${endDate.toISOString().split("T")[0]}`;

    fetch(url)
      .then(response => response.blob())
      .then(blob => {
        const imgUrl = URL.createObjectURL(blob);
        setImageSrc(imgUrl);
      })
      .catch(error => console.error("Error loading heatmap:", error));
  };

  useEffect(() => {
    fetchHeatmap();
  }, [selectedColumns, startDate, endDate]);

  // Handle checkbox selection
  const handleColumnChange = (column) => {
    setSelectedColumns(prev =>
      prev.includes(column) ? prev.filter(col => col !== column) : [...prev, column]
    );
  };

  return (
    <div>
      <h2>Dynamic Correlation Matrix Heatmap</h2>

      {/* Date Filters */}
      <div>
        <label>Start Date:</label>
        <DatePicker selected={startDate} onChange={date => setStartDate(date)} />
        <label>End Date:</label>
        <DatePicker selected={endDate} onChange={date => setEndDate(date)} />
      </div>

      {/* Column Selection */}
      <div>
        <h4>Select Columns:</h4>
        {availableColumns.map(column => (
          <label key={column} style={{ marginRight: "10px" }}>
            <input
              type="checkbox"
              checked={selectedColumns.includes(column)}
              onChange={() => handleColumnChange(column)}
            />
            {column}
          </label>
        ))}
      </div>

      {/* Display Heatmap */}
      {imageSrc ? <img src={imageSrc} alt="Correlation Heatmap" /> : <p>Loading heatmap...</p>}
    </div>
  );
};

export default Heatmap;
