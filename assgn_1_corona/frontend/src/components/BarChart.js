import React, { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/bar_chart/";

const BarChart = () => {
    const [chartData, setChartData] = useState({
        labels: [],
        activeCases: [],
        recoveredCases: [],
    });

    useEffect(() => {
        fetchChartData();
    }, []);

    const fetchChartData = async () => {
        try {
            const response = await axios.get(API_URL);
            setChartData({
                labels: response.data.labels,
                activeCases: response.data.active_cases,
                recoveredCases: response.data.recovered_cases,
            });
        } catch (error) {
            console.error("Error fetching bar chart data:", error);
        }
    };

    return (
        <div style={{ width: "800px", height: "400px" }}>
        <Bar
            data={{
                labels: chartData.labels,
                datasets: [
                    {
                        label: "Active Cases",
                        data: chartData.activeCases,
                        backgroundColor: "rgba(255, 99, 132, 0.6)", // Red
                        maxBarThickness: 40, // Prevents overly wide bars
                    },
                ],
            }}
            options={{
                responsive: true,
                maintainAspectRatio: false,
                devicePixelRatio: 1, // Fixes high DPI scaling issue
            }}
        />
    </div>
    
    );
};

export default BarChart;
