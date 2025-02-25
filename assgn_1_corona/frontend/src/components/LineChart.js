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
                labels: response.data.labels, // Country names
                values: response.data.cfr_values, // CFR values
            });
        } catch (error) {
            console.error("Error fetching line chart data:", error);
        }
    };

    return (
        <div style={{ width: "90%", maxWidth: "800px", height: "400px", margin: "auto" }}>
            <h3>Top 10 Countries by Case Fatality Ratio (CFR)</h3>
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
                            tension: 0.3, // ✅ Slight curve for a smoother look
                        },
                    ],
                }}
                options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            ticks: {
                                maxRotation: 45, 
                                minRotation: 0,
                                autoSkip: true,
                                maxTicksLimit: 10,
                            },
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: "CFR (%)",
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: "top",
                        },
                        tooltip: {
                            callbacks: {
                                label: (context) => `${context.raw.toFixed(2)}%`,
                            },
                        },
                    },
                }}
            />
        </div>
    );
};

export default LineChart;
