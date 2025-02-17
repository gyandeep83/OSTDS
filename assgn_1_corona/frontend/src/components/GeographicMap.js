import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import markerIconPng from "leaflet/dist/images/marker-icon.png";
import markerShadowPng from "leaflet/dist/images/marker-shadow.png";
import axios from "axios";

// Define the custom marker icon
const customIcon = new L.Icon({
    iconUrl: markerIconPng,
    shadowUrl: markerShadowPng,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
});

// Hardcoded US state coordinates
const usStateCoordinates = {
    "Alabama": [32.8067, -86.7911],
    "Alaska": [61.3707, -152.4044],
    "Arizona": [33.7298, -111.4312],
    "Arkansas": [34.7465, -92.2896],
    "California": [36.7783, -119.4179],
    "Colorado": [39.5501, -105.7821],
    "Connecticut": [41.6032, -73.0877],
    "Delaware": [38.9108, -75.5277],
    "Florida": [27.9944, -81.7603],
    "Georgia": [32.1656, -82.9001],
    "Hawaii": [20.7967, -156.3319],
    "Idaho": [44.0682, -114.742],
    "Illinois": [40.6331, -89.3985],
    "Indiana": [40.2672, -86.1349],
    "Iowa": [41.878, -93.0977],
    "Kansas": [39.0119, -98.4842],
    "Kentucky": [37.8393, -84.270],
    "Louisiana": [30.9843, -91.9623],
    "Maine": [45.2538, -69.4455],
    "Maryland": [39.0458, -76.6413],
    "Massachusetts": [42.4072, -71.3824],
    "Michigan": [44.3148, -85.6024],
    "Minnesota": [46.7296, -94.6859],
    "Mississippi": [32.3547, -89.3985],
    "Missouri": [37.9643, -91.8318],
    "Montana": [46.8797, -110.3626],
    "Nebraska": [41.4925, -99.9018],
    "Nevada": [38.8026, -116.4194],
    "New Hampshire": [43.1939, -71.5724],
    "New Jersey": [40.0583, -74.4057],
    "New Mexico": [34.5199, -105.8701],
    "New York": [40.7128, -74.006],
    "North Carolina": [35.7596, -79.0193],
    "North Dakota": [47.5515, -101.002],
    "Ohio": [40.4173, -82.9071],
    "Oklahoma": [35.4676, -97.5164],
    "Oregon": [43.8041, -120.5542],
    "Pennsylvania": [41.2033, -77.1945],
    "Rhode Island": [41.5801, -71.4774],
    "South Carolina": [33.8361, -81.1637],
    "South Dakota": [44.2998, -99.4388],
    "Tennessee": [35.5175, -86.5804],
    "Texas": [31.9686, -99.9018],
    "Utah": [39.3209, -111.0937],
    "Vermont": [44.5588, -72.5778],
    "Virginia": [37.4316, -78.6569],
    "Washington": [47.7511, -120.7401],
    "West Virginia": [38.5976, -80.4549],
    "Wisconsin": [43.7844, -88.7879],
    "Wyoming": [43.07597, -107.2903]
};

const API_URL = "http://127.0.0.1:8000/api/geographic/";

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
        <MapContainer center={[37.0902, -95.7129]} zoom={4} style={{ height: "500px", width: "100%" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {geoData.map((item, index) => {
                const state = item.state?.trim();
                if (state && usStateCoordinates[state]) {
                    return (
                        <Marker key={index} position={usStateCoordinates[state]} icon={customIcon}>
                            <Popup>
                                <strong>{state}</strong><br />
                                Confirmed: {item.confirmed}<br />
                                Deaths: {item.deaths}
                            </Popup>
                        </Marker>
                    );
                } else {
                    console.warn(`Missing coordinates for state: ${state}`);
                    return null;
                }
            })}
        </MapContainer>
    );
};

export default GeographicMap;
