import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const TimeSeriesChart = () => {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/time-series/")
            .then(response => {
                const data = response.data.time_series;

                // Format week dates for better readability
                const labels = data.map(entry => new Date(entry.Week).toLocaleDateString("en-US", { 
                    year: "numeric", month: "short", day: "numeric"
                }));

                const confirmedCases = data.map(entry => entry.Confirmed || 0);
                const deaths = data.map(entry => entry.Deaths || 0);
                const recovered = data.map(entry => entry.Recovered || 0);

                setChartData({
                    labels,
                    datasets: [
                        {
                            label: "Confirmed Cases",
                            data: confirmedCases,
                            borderColor: "blue",
                            fill: false
                        },
                        {
                            label: "Deaths",
                            data: deaths,
                            borderColor: "red",
                            fill: false
                        },
                        {
                            label: "Recovered",
                            data: recovered,
                            borderColor: "green",
                            fill: false
                        }
                    ]
                });
            })
            .catch(error => console.error("Error fetching data:", error));
    }, []);

    return (
        <div>
            <h2>COVID-19 Time Series Data</h2>
            {chartData ? <Line 
                data={chartData} 
                options={{
                    scales: {
                        x: {
                            ticks: {
                                maxTicksLimit: 10, // Limit number of labels
                                autoSkip: true // Skip labels if too many
                            }
                        }
                    }
                }}
            /> : <p>Loading...</p>}
        </div>
    );
};

export default TimeSeriesChart;
