import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/line_chart/";

const LineChart = () => {
    const [chartData, setChartData] = useState({ labels: [], values: [] });

    useEffect(() => {
        fetchChartData();
    }, []);

    const fetchChartData = async () => {
        try {
            const response = await axios.get(API_URL);
            setChartData({
                labels: response.data.labels,
                values: response.data.cfr_values,
            });
        } catch (error) {
            console.error("Error fetching line chart data:", error);
        }
    };

    return (
        <div style={{ width: "90%", maxWidth: "800px", height: "400px", margin: "auto" }}> {/* ✅ Fix for canvas size */}
            <h3>Top 10 States by Case Fatality Ratio (CFR)</h3>
            <Line
                data={{
                    labels: chartData.labels,
                    datasets: [
                        {
                            label: "CFR (%)",
                            data: chartData.values,
                            borderColor: "#FF6384",
                            backgroundColor: "rgba(255, 99, 132, 0.2)",
                            fill: true,
                        },
                    ],
                }}
                options={{
                    responsive: true,
                    maintainAspectRatio: false, 
                    scales: {
                        x: {
                            ticks: {
                                maxRotation: 45, // ✅ Prevents overlapping labels
                                minRotation: 0,
                                autoSkip: true, // ✅ Skips some labels to reduce clutter
                                maxTicksLimit: 10, // ✅ Limits labels shown
                            },
                        },
                        y: {
                            beginAtZero: true,
                        },
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: "top",
                        },
                    },
                }}
            />
        </div>
    );
};

export default LineChart;

