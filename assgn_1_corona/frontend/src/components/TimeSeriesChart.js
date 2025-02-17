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
                const labels = data.map(entry => new Date(entry.Last_Update).toLocaleDateString());
                const confirmedCases = data.map(entry => entry.Confirmed);
                const deaths = data.map(entry => entry.Deaths);
                const recovered = data.map(entry => entry.Recovered);

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
            {chartData ? <Line data={chartData} /> : <p>Loading...</p>}
        </div>
    );
};

export default TimeSeriesChart;
