#view.py-This is the main program and entrypoint of project.
#Author-Gyan deep, (gd034281@gmail.com)
#Description-We are doing data analysis and cleaning.



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from logger import setup_logger
import os
import logging



# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = " "
CLEANED_DIR = " "

def clean_data(df):
    if "Last_Update" in df.columns:
        df["Last_Update"] = pd.to_datetime(df["Last_Update"], errors="coerce")
    else:
        logger.warning("Skipping file: Missing 'Last_Update' column")
        return pd.DataFrame()  # Return empty DataFrame if column is missing

    logger.info(f"Columns in dataset: {df.columns.tolist()}")

    if "Country_Region" not in df.columns:
        logger.error("'Country_Region' column not found.")
        return pd.DataFrame()

    # Use global data instead of just US
    df.drop(columns=["Long_", "Lat"], errors="ignore", inplace=True)

    return df



def load_data(file_path, logger):
    """Loads a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded data from {file_path} with {len(df)} rows")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except pd.errors.ParserError:
        logger.error(f"Error reading CSV: {file_path}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return None


def save_cleaned_data(df, output_file, logger):
    """Saves the cleaned DataFrame to a new CSV file."""
    try:
        df.to_csv(output_file, index=False)
        logger.info(f"Saved cleaned data to {output_file} with {len(df)} rows")
    except Exception as e:
        logger.error(f"Failed to save cleaned data: {e}")


def process_all_files(input_dir, output_dir, logger):
    """Process all CSV files in the input directory and save cleaned data to output directory."""
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            logger.info(f"📂 Processing file: {file_path}")

            df = pd.read_csv(file_path)
            cleaned_df = clean_data(df)

            if not cleaned_df.empty:
                cleaned_file_path = os.path.join(output_dir, filename)
                cleaned_df.to_csv(cleaned_file_path, index=False)
                logger.info(f"✅ Saved cleaned file: {cleaned_file_path}")

if __name__ == "__main__":
    logger.info("🚀 Starting CSV cleaning process...")
    process_all_files(DATA_DIR, CLEANED_DIR, logger)  # ✅ Now correctly passing arguments
    logger.info("🎯 Cleaning process completed!")


if __name__ == "__main__":
    logger = setup_logger(log_level="DEBUG")

    input_directory = " "
    output_directory = " "

    logger.info("Starting batch processing for all CSV files...")
    process_all_files(input_directory, output_directory, logger)
    logger.info("Batch processing completed.")

"""
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
"""