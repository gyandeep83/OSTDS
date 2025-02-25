import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/bar_chart/";

const BarChart = () => {
    const [chartData, setChartData] = useState({ labels: [], values: [] });

    useEffect(() => {
        fetchChartData();
    }, []);

    const fetchChartData = async () => {
        try {
            const response = await axios.get(API_URL);

            setChartData({
                labels: response.data.labels,
                values: response.data.active_cases,
            });
        } catch (error) {
            console.error("Error fetching bar chart data:", error);
        }
    };

    return (
        <div style={{ width: "90%", maxWidth: "800px", height: "400px", margin: "auto" }}>
            <h3>Top 10 Countries by Active Cases</h3>
            <Bar
                data={{
                    labels: chartData.labels,
                    datasets: [
                        {
                            label: "Active Cases",
                            data: chartData.values,
                            backgroundColor: "rgba(54, 162, 235, 0.6)",
                            borderColor: "rgba(54, 162, 235, 1)",
                            borderWidth: 1,
                        },
                    ],
                }}
                options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 10,
                            },
                        },
                        y: {
                            beginAtZero: true,
                        },
                    },
                    plugins: {
                        legend: { display: true, position: "top" },
                    },
                }}
            />
        </div>
    );
};

export default BarChart;
