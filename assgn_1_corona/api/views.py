#view.py-Consist of Various functions.
#Author-Gyan deep, (gd034281@gmail.com)
#Description-Backend programs for rendering visualizations.



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

# Define the directory containing all time series CSV files

DATA_DIR = " "

# Function to get time-series data of COVID-19 cases
def get_time_series_data(request):
    try:
        all_dataframes = []
        
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".csv"):
                file_path = os.path.join(DATA_DIR, filename)
                df = pd.read_csv(file_path, parse_dates=["Last_Update"], low_memory=False)
                all_dataframes.append(df)
        
        if not all_dataframes:
            return JsonResponse({"error": "No valid data files found."}, status=500)
        
        df = pd.concat(all_dataframes, ignore_index=True)
        
        # Convert to weekly data by summing cases within each week
        df["Last_Update"] = pd.to_datetime(df["Last_Update"])
        df["Week"] = df["Last_Update"].dt.to_period("W").apply(lambda r: r.start_time)

        time_series = df.groupby("Week").agg({
            "Confirmed": "sum",
            "Deaths": "sum",
            "Recovered": "sum"
        }).reset_index()

        data = time_series.to_dict(orient="records")
        return JsonResponse({"time_series": data}, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def line_chart_data(request):
    directory_path = " "

    # Get all CSV files in the cleaned directory
    all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".csv")]

    if not all_files:
        return JsonResponse({"error": "No CSV files found in the directory"}, status=500)

    # Load and combine all CSV files
    df_list = []
    for file in all_files:
        try:
            df_temp = pd.read_csv(file)
            if not df_temp.empty:
                df_list.append(df_temp)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not df_list:
        return JsonResponse({"error": "All CSV files are empty or corrupted"}, status=500)

    df = pd.concat(df_list, ignore_index=True)

    # Ensure required columns exist
    required_columns = ["Country_Region", "Confirmed", "Deaths"]
    if not all(col in df.columns for col in required_columns):
        return JsonResponse({"error": f"Missing required columns in CSV"}, status=400)

    # Convert Confirmed and Deaths to numeric, forcing errors to NaN
    df["Confirmed"] = pd.to_numeric(df["Confirmed"], errors="coerce")
    df["Deaths"] = pd.to_numeric(df["Deaths"], errors="coerce")

    # Drop rows where 'Confirmed' is NaN or 0 to avoid division issues
    df = df[df["Confirmed"] > 0]

    # Compute Case Fatality Ratio (CFR)
    df["CFR"] = (df["Deaths"] / df["Confirmed"]) * 100

    # Aggregate CFR by country
    country_cfr = df.groupby("Country_Region", as_index=False)["CFR"].mean()

    # Sort and get top 10 countries with highest CFR
    top_countries = country_cfr.sort_values(by="CFR", ascending=False).head(10)

    # Prepare response
    response_data = {
        "labels": top_countries["Country_Region"].tolist(),
        "cfr_values": top_countries["CFR"].tolist()
    }

    return JsonResponse(response_data)



"""
Returns COVID-19 data aggregated by country regions.
Used for plotting.
"""

# Directory where CSV files are stored
BASE_DIR = " "

# File names (picking the correct ones)
FILES = {
    "confirmed": "time_series_covid19_confirmed_global.csv",
    "deaths": "time_series_covid19_deaths_global.csv",
    "recovered": "time_series_covid19_recovered_global.csv",
}

def geographic_data(request):
    dataframes = {}

    # Load all datasets
    for key, filename in FILES.items():
        file_path = os.path.join(BASE_DIR, filename)
        try:
            dataframes[key] = pd.read_csv(file_path)
        except FileNotFoundError:
            return JsonResponse({"error": f"File not found: {filename}"}, status=404)

    # Ensure required columns exist
    required_columns = ["Country/Region", "Lat", "Long"]
    for key, df in dataframes.items():
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return JsonResponse({"error": f"Missing columns in {FILES[key]}: {missing_columns}"}, status=400)

    # Process each dataset
    for key in dataframes:
        date_columns = dataframes[key].columns[4:]  # Date columns start from 5th column
        dataframes[key]["Total"] = dataframes[key][date_columns].sum(axis=1, numeric_only=True)

        # Keep only necessary columns
        dataframes[key] = dataframes[key][["Country/Region", "Lat", "Long", "Total"]]

    # Merge datasets
    merged_df = dataframes["confirmed"].merge(
        dataframes["deaths"], on=["Country/Region", "Lat", "Long"], suffixes=("_confirmed", "_deaths")
    ).merge(
        dataframes["recovered"], on=["Country/Region", "Lat", "Long"], suffixes=("", "_recovered")
    )

    # Rename columns for clarity
    merged_df.rename(columns={"Total_confirmed": "Total_Confirmed", 
                              "Total_deaths": "Total_Deaths", 
                              "Total": "Total_Recovered"}, inplace=True)

    # Handle NaN values and ensure JSON serialization compatibility
    merged_df = merged_df.fillna(0)  # Replace NaN with 0
    response_data = merged_df.to_dict(orient="records")

    # Convert NumPy integers to standard Python integers
    for entry in response_data:
        for key in ["Total_Confirmed", "Total_Deaths", "Total_Recovered"]:
            entry[key] = int(entry[key]) if not np.isnan(entry[key]) else 0  # Ensure no NaN

    return JsonResponse(response_data, safe=False)

"""
Returns data for a pie chart showing the top 10 states with the highest confirmed cases or deaths.
The metric (confirmed cases or deaths) is determined from the request.
"""
def pie_chart_data(request):
    directory_path = " "

    # Read all CSV files in the directory
    all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".csv")]

    # Load and combine CSVs
    df_list = [pd.read_csv(file) for file in all_files]
    df = pd.concat(df_list, ignore_index=True)

    # Ensure required columns exist
    required_columns = ["Country_Region", "Confirmed", "Deaths"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return JsonResponse({"error": f"Missing columns in CSV: {missing_columns}"}, status=400)

    # Get metric from request (default to 'confirmed')
    metric = request.GET.get("metric", "confirmed").lower()
    if metric not in ["confirmed", "deaths"]:
        return JsonResponse({"error": "Invalid metric"}, status=400)

    # Aggregate by country
    country_data = df.groupby("Country_Region")[["Confirmed", "Deaths"]].sum().reset_index()

    # Sort and get top 10 countries based on the selected metric
    sorted_data = country_data.sort_values(by=metric.capitalize(), ascending=False).head(10)

    # Prepare response
    response_data = {
        "labels": sorted_data["Country_Region"].tolist(),
        "values": sorted_data[metric.capitalize()].tolist()
    }

    return JsonResponse(response_data)

"""
Returns data for a bar chart displaying the top 10 states with the highest number of active cases.
"""
def bar_chart_data(request):
    directory = " "

    # Read all CSV files in the directory
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]
    if not csv_files:
        return JsonResponse({"error": "No CSV files found in directory"}, status=400)

    # Load all CSVs into a single DataFrame
    df_list = [pd.read_csv(file) for file in csv_files]
    df = pd.concat(df_list, ignore_index=True)

    # Ensure required columns exist
    if "Country_Region" not in df.columns or "Active" not in df.columns:
        return JsonResponse({"error": "Missing required columns in CSV"}, status=400)

    # Aggregate Active cases by country
    country_data = df.groupby("Country_Region")["Active"].sum().reset_index()

    # Sort and get top 10 countries by Active cases
    sorted_data = country_data.sort_values(by="Active", ascending=False).head(10)

    # Prepare response
    response_data = {
        "labels": sorted_data["Country_Region"].tolist(),
        "active_cases": sorted_data["Active"].tolist()
    }

    return JsonResponse(response_data)

"""
Returns data for a scatter plot comparing the incident rate and case fatality ratio (CFR) for the top 10 states.
"""
def scatter_plot_data(request):
    directory = " "

    # Read all CSV files in the directory
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".csv")]
    if not csv_files:
        return JsonResponse({"error": "No CSV files found in directory"}, status=400)

    # Load all CSVs into a single DataFrame
    df_list = [pd.read_csv(file) for file in csv_files]
    df = pd.concat(df_list, ignore_index=True)

    # Ensure required columns exist
    required_columns = ["Country_Region", "Incident_Rate", "Case_Fatality_Ratio"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return JsonResponse({"error": f"Missing columns in CSV: {missing_columns}"}, status=400)

    # Drop rows with missing values in required columns
    df = df.dropna(subset=required_columns)

    # Aggregate by country and calculate average values
    country_data = df.groupby("Country_Region")[["Incident_Rate", "Case_Fatality_Ratio"]].mean().reset_index()

    # Sort by highest incident rate and get top 10 countries
    sorted_data = country_data.sort_values(by="Incident_Rate", ascending=False).head(10)

    # Prepare response
    response_data = {
        "countries": sorted_data["Country_Region"].tolist(),
        "incident_rates": sorted_data["Incident_Rate"].tolist(),
        "cfr_values": sorted_data["Case_Fatality_Ratio"].tolist(),
    }

    return JsonResponse(response_data)
    return JsonResponse(response_data)
