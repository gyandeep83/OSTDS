import React, { useEffect, useState } from "react";
import { Scatter } from "react-chartjs-2";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/scatter_plot/";

const ScatterPlot = () => {
    const [chartData, setChartData] = useState({ labels: [], datasets: [] });

    useEffect(() => {
        fetchChartData();
    }, []);

    const fetchChartData = async () => {
        try {
            const response = await axios.get(API_URL);
            const { states, incident_rates, cfr_values } = response.data;

            setChartData({
                labels: states,
                datasets: [
                    {
                        label: "Mortality vs. Infection Rate",
                        data: states.map((state, index) => ({
                            x: incident_rates[index],
                            y: cfr_values[index],
                        })),
                        backgroundColor: "#FF6384",
                        pointRadius: 6,
                    },
                ],
            });
        } catch (error) {
            console.error("Error fetching scatter plot data:", error);
        }
    };

    return (
        <div style={{ width: "80%", height: "500px", margin: "auto" }}>
    <Scatter
        data={chartData}
        options={{
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: "Incident Rate" } },
                y: { title: { display: true, text: "Case Fatality Ratio (%)" } },
            },
        }}
    />
</div>

    );
};

export default ScatterPlot;
