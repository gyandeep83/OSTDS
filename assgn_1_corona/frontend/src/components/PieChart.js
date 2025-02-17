import React, { useEffect, useState } from "react";
import { Pie } from "react-chartjs-2";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/pie_chart/";

const PieChart = () => {
    const [chartData, setChartData] = useState({ labels: [], values: [] });
    const [metric, setMetric] = useState("confirmed"); // Default to confirmed cases

    useEffect(() => {
        fetchChartData();
    }, [metric]); // Fetch data when metric changes

    const fetchChartData = async () => {
        try {
            const response = await axios.get(API_URL, { params: { metric } });

            // Ensure exactly 10 states are returned
            setChartData({
                labels: response.data.labels.slice(0, 10),
                values: response.data.values.slice(0, 10),
            });
        } catch (error) {
            console.error("Error fetching pie chart data:", error);
        }
    };

    return (
        <div style={{ maxWidth: "500px", margin: "auto", textAlign: "center" }}>
            <h3>Top 10 States by {metric === "confirmed" ? "Confirmed Cases" : "Deaths"}</h3>

            {/* Dropdown for switching between Confirmed Cases and Deaths */}
            <select 
                onChange={(e) => setMetric(e.target.value)} 
                value={metric} 
                style={{ marginBottom: "10px", padding: "5px" }}
            >
                <option value="confirmed">Confirmed Cases</option>
                <option value="deaths">Deaths</option>
            </select>

            {/* Render Pie Chart in a fixed-size container */}
            <div style={{ width: "400px", height: "400px", margin: "auto" }}>
                <Pie
                    data={{
                        labels: chartData.labels,
                        datasets: [
                            {
                                data: chartData.values,
                                backgroundColor: [
                                    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
                                    "#9966FF", "#FF9F40", "#FFCD56", "#C9CBCF",
                                    "#FF6666", "#33FF99"
                                ],
                            },
                        ],
                    }}
                    options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: "top" },
                        },
                        layout: { padding: 10 },
                    }}
                />
            </div>
        </div>
    );
};

export default PieChart;
