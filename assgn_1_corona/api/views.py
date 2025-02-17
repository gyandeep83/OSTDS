from django.shortcuts import render

# Create your views here.
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
import os
import numpy as np
from django.http import HttpResponse
import io

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

# Load the CSV file
DATA_PATH = "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"

# Function to get time-series data of COVID-19 cases
def get_time_series_data(request):
    try:
        df = pd.read_csv(DATA_PATH, parse_dates=["Last_Update"])

        # Group by date and sum cases
        time_series = df.groupby("Last_Update").agg({
            "Confirmed": "sum",
            "Deaths": "sum",
            "Recovered": "sum"
        }).reset_index()

        data = time_series.to_dict(orient="records")
        return JsonResponse({"time_series": data}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Function to generate a correlation heatmap of selected COVID-19 metrics
def correlation_heatmap(request):
    try:
        # Load dataset from CSV
        file_path = "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"
        df = pd.read_csv(file_path)

        # Rename column for consistency
        df.rename(columns={"Last_Update": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"])  # Convert to datetime

        # Get filter parameters from frontend
        selected_columns = request.GET.getlist("columns[]")  # Example: ["Confirmed", "Deaths", "Active"]
        start_date = request.GET.get("start_date", "2021-01-01")
        end_date = request.GET.get("end_date", "2021-12-31")

        # Convert filter values to datetime
        start_date = pd.to_datetime(start_date, errors="coerce")
        end_date = pd.to_datetime(end_date, errors="coerce")

        # Validate start_date and end_date
        if start_date is pd.NaT or end_date is pd.NaT:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Filter based on date range
        df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

        # Default columns for correlation if none are selected
        default_columns = ["Confirmed", "Deaths", "Recovered", "Active", "Incident_Rate", "Case_Fatality_Ratio"]

        # Filter only selected columns, fallback to default if none selected
        if selected_columns:
            selected_columns = [col for col in selected_columns if col in df.columns]
        else:
            selected_columns = default_columns

        # Ensure there are valid columns to process
        if not selected_columns:
            return JsonResponse({"error": "No valid columns selected"}, status=400)

        df = df[selected_columns]

        # Compute correlation matrix
        correlation_matrix = df.corr()

        # Generate Heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)

        # Explicitly render the figure
        fig.canvas.draw()

        # Save image in memory
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)  # Ensure figure is closed to free memory

        buf.seek(0)
        return HttpResponse(buf.getvalue(), content_type="image/png")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def line_chart_data(request):
    file_path = "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = ["Province_State", "Confirmed", "Deaths"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return JsonResponse({"error": f"Missing columns in CSV: {missing_columns}"}, status=400)

    # Replace zero confirmed cases to avoid division by zero
    df["Confirmed"].replace(0, pd.NA, inplace=True)

    # Compute Case Fatality Ratio (CFR)
    df["CFR"] = (df["Deaths"] / df["Confirmed"]) * 100

    # Aggregate CFR by state
    state_cfr = df.groupby("Province_State")["CFR"].mean().reset_index()

    # Sort and get top 10 states with highest CFR
    top_states = state_cfr.sort_values(by="CFR", ascending=False).head(10)

    # Prepare response
    response_data = {
        "labels": top_states["Province_State"].tolist(),
        "cfr_values": top_states["CFR"].tolist()
    }

    return JsonResponse(response_data)


# Hardcoded US state coordinates used for geographic visualizations
us_state_coordinates = {
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
}


"""
Returns COVID-19 data aggregated by US state along with their coordinates.
The data includes total confirmed cases and deaths.
"""
def geographic_data(request):
    file_path = "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)
    
    # Ensure relevant columns exist
    required_columns = ["Province_State", "Confirmed", "Deaths"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return JsonResponse({"error": f"Missing columns in CSV: {missing_columns}"}, status=400)

    # Group by state to aggregate confirmed cases and deaths
    state_data = df.groupby("Province_State")[["Confirmed", "Deaths"]].sum().reset_index()

    # Prepare JSON response
    response_data = []

    # Iterate over all states and add data (even if missing from CSV)
    for state, coordinates in us_state_coordinates.items():
        row = state_data[state_data["Province_State"] == state]
        confirmed = int(row["Confirmed"].sum()) if not row.empty else 0
        deaths = int(row["Deaths"].sum()) if not row.empty else 0

        response_data.append({
            "state": state,
            "latitude": coordinates[0],
            "longitude": coordinates[1],
            "confirmed": confirmed,
            "deaths": deaths
        })
    
    return JsonResponse(response_data, safe=False)


"""
Returns data for a pie chart showing the top 10 states with the highest confirmed cases or deaths.
The metric (confirmed cases or deaths) is determined from the request.
"""
def pie_chart_data(request):
    file_path = "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = ["Province_State", "Confirmed", "Deaths"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return JsonResponse({"error": f"Missing columns in CSV: {missing_columns}"}, status=400)

    # Get metric from request (default to 'confirmed')
    metric = request.GET.get("metric", "confirmed")
    if metric not in ["confirmed", "deaths"]:
        return JsonResponse({"error": "Invalid metric"}, status=400)

    # Aggregate by state
    state_data = df.groupby("Province_State")[["Confirmed", "Deaths"]].sum().reset_index()

    # Sort and get top 10 states
    sorted_data = state_data.sort_values(by="Confirmed" if metric == "confirmed" else "Deaths", ascending=False).head(10)

    # Prepare response
    response_data = {
        "labels": sorted_data["Province_State"].tolist(),
        "values": sorted_data["Confirmed" if metric == "confirmed" else "Deaths"].tolist()
    }

    return JsonResponse(response_data)


"""
Returns data for a bar chart displaying the top 10 states with the highest number of active cases.
"""
def bar_chart_data(request):
    file_path = "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)

    # Ensure required columns exist
    if "Province_State" not in df.columns or "Active" not in df.columns:
        return JsonResponse({"error": "Missing required columns in CSV"}, status=400)

    # Aggregate Active cases by state
    state_data = df.groupby("Province_State")["Active"].sum().reset_index()

    # Sort and get top 10 states by Active cases
    sorted_data = state_data.sort_values(by="Active", ascending=False).head(10)

    # Prepare response
    response_data = {
        "labels": sorted_data["Province_State"].tolist(),
        "active_cases": sorted_data["Active"].tolist()
    }

    return JsonResponse(response_data)


"""
Returns data for a scatter plot comparing the incident rate and case fatality ratio (CFR) for the top 10 states.
"""
def scatter_plot_data(request):
    file_path = "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"

    # Load CSV
    df = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = ["Province_State", "Incident_Rate", "Case_Fatality_Ratio"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return JsonResponse({"error": f"Missing columns in CSV: {missing_columns}"}, status=400)

    # Drop rows with missing values in required columns
    df = df.dropna(subset=required_columns)

    # Sort by highest incident rate and get top 10 states
    sorted_data = df.sort_values(by="Incident_Rate", ascending=False).head(10)

    # Prepare response
    response_data = {
        "states": sorted_data["Province_State"].tolist(),
        "incident_rates": sorted_data["Incident_Rate"].tolist(),
        "cfr_values": sorted_data["Case_Fatality_Ratio"].tolist(),
    }

    return JsonResponse(response_data)
