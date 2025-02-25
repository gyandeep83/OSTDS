import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import axios from "axios";

// API Endpoint
const API_URL = "http://127.0.0.1:8000/api/geographic/";

// Custom marker icon
const customIcon = new L.Icon({
    iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
    shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
});

const GeographicMap = () => {
    const [geoData, setGeoData] = useState([]);

    useEffect(() => {
        axios.get(API_URL)
            .then((res) => {
                console.log("Fetched Data:", res.data);
                setGeoData(res.data);
            })
            .catch((error) => console.error("Error fetching data:", error));
    }, []);

    return (
        <MapContainer center={[20, 0]} zoom={2} style={{ height: "500px", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {geoData.map((item, index) => (
                <Marker
                    key={index}
                    position={[item.Lat, item.Long]}
                    icon={customIcon}
                >
                    <Popup>
                        <strong>{item["Country/Region"]}</strong><br />
                        Confirmed: {item.Total_Confirmed}<br />
                        Deaths: {item.Total_Deaths}<br />
                        Recovered: {item.Total_Recovered}
                    </Popup>
                </Marker>
            ))}
        </MapContainer>
    );
};

export default GeographicMap;
