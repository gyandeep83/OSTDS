import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from logger import setup_logger
import os


def clean_data(df, logger):
    df.dropna(inplace=True)
    df["Last_Update"] = pd.to_datetime(df["Last_Update"])

    logger.info(f"Columns in the dataset: {df.columns.tolist()}")

    if "Country_Region" not in df.columns:
        logger.error("'Country_Region' column not found.")
        return pd.DataFrame()

    df = df[df["Country_Region"] == "US"]
    df.drop(columns=["Long_", "Lat"], errors="ignore", inplace=True)

    return df


def load_data(file_path):
    try:
        data = pd.read_csv(
            "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2021.csv"
        )
        logger.info("Data successfully loaded")
        return data
    except FileNotFoundError:
        logger.error(
            f"File not found at path: {file_path}. Please check the file path."
        )
    except pd.errors.ParserError:
        logger.error("Error reading the CSV file. It may be malformed.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return None


def save_cleaned_data(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        logger.info(f"Cleaned data saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save cleaned data: {e}")


def analyze_data(cleaned_data):
    if cleaned_data.empty:
        logger.warning("No data available for analysis.")
        return

    if "Province_State" in cleaned_data.columns:
        statewise_summary = cleaned_data.groupby("Province_State").describe()
        print(statewise_summary)

    if {"Deaths", "Confirmed"}.issubset(cleaned_data.columns):
        cleaned_data["Case_Fatality_Ratio"] = cleaned_data.apply(
            lambda row: (row["Deaths"] / row["Confirmed"] * 100)
            if row["Confirmed"] > 0
            else 0,
            axis=1,
        )
        plot_case_fatality_ratio(cleaned_data["Case_Fatality_Ratio"])
        plot_correlation_matrix(cleaned_data)


def plot_case_fatality_ratio(case_fatality_ratio):
    plt.figure(figsize=(10, 6))
    sns.histplot(case_fatality_ratio, kde=True)
    plt.title("Distribution of Case Fatality Ratio")
    plt.xlabel("Case Fatality Ratio (%)")
    plt.show()


def plot_correlation_matrix(cleaned_data):
    numeric_data = cleaned_data.select_dtypes(include=["float64", "int64"])
    correlation = numeric_data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()


if __name__ == "__main__":
    logger = setup_logger(log_level="DEBUG")

    base_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(
        base_dir,
        "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2021.csv",
        "data",
        "01-01-2021.csv",
    )
    processed_file_path = os.path.join(
        base_dir,
        "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv",
    )

    logger.warning("Running analysis on single file only")
    logger.info(f"Attempting to load data from: {csv_file_path}")

    df = load_data(
        "/Users/gyandeep/OSTDS/assgn_1_corona/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/processed_data.csv"
    )

    if df is not None:
        cleaned_data = clean_data(df, logger)
        if not cleaned_data.empty:
            save_cleaned_data(cleaned_data, processed_file_path)
            analyze_data(cleaned_data)
        else:
            logger.error("Cleaned data is empty. Exiting the script.")
    else:
        logger.error("Data loading failed. Exiting the script.")
