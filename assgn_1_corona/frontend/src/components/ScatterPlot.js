import React, { useEffect, useState } from "react";
import { Scatter } from "react-chartjs-2";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/scatter_plot/";

const ScatterPlot = () => {
    const [chartData, setChartData] = useState({ datasets: [] });

    useEffect(() => {
        fetchChartData();
    }, []);

    const fetchChartData = async () => {
        try {
            const response = await axios.get(API_URL);

            const { countries, incident_rates, cfr_values } = response.data;

            setChartData({
                labels: countries,
                datasets: [
                    {
                        label: "Incident Rate vs. Case Fatality Ratio",
                        data: countries.map((_, index) => ({
                            x: incident_rates[index],
                            y: cfr_values[index],
                        })),
                        backgroundColor: "rgba(75,192,192,0.6)",
                        borderColor: "rgba(75,192,192,1)",
                    },
                ],
            });
        } catch (error) {
            console.error("Error fetching scatter plot data:", error);
        }
    };

    return (
        <div style={{ width: "90%", maxWidth: "800px", height: "400px", margin: "auto" }}>
            <h3>Top 10 Countries: Incident Rate vs. Case Fatality Ratio</h3>
            <Scatter
                data={chartData}
                options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: { display: true, text: "Incident Rate" },
                        },
                        y: {
                            title: { display: true, text: "Case Fatality Ratio (%)" },
                        },
                    },
                }}
            />
        </div>
    );
};

export default ScatterPlot;
