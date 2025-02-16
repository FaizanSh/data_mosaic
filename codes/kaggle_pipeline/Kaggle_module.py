import kaggle
import zipfile
import os
import glob
import pandas as pd

# Define dataset parameters
DATASET_NAME = "sudalairajkumar/cryptocurrencypricehistory"
DOWNLOAD_PATH = "../dataset/raw/crypto_data_1"


def download_kaggle_dataset(dataset_name, download_path):
    """
    Downloads and extracts the dataset from Kaggle.
    """
    os.makedirs(download_path, exist_ok=True)
    kaggle.api.dataset_download_files(dataset_name, path=download_path, unzip=True)
    print("Download complete. Files are:", os.listdir(download_path))

def clean_data(download_path):
    """
    Reads and cleans cryptocurrency data from CSV files.
    Returns the cleaned DataFrame.
    """
    # Find all CSV files
    files = glob.glob(os.path.join(download_path, "coin*.csv"))
    
    if not files:
        print("No matching CSV files found!!!")
        return None

    df_list = [pd.read_csv(file) for file in files]
    merged_df = pd.concat(df_list, ignore_index=True)
    print("Initial Dataset Info:")
    merged_df.info()
    merged_df = merged_df[(merged_df["Volume"] > 0.0) & (merged_df["Marketcap"] > 0.0)]
    merged_df["Date"] = pd.to_datetime(merged_df["Date"])
    merged_df["Price Change"] = merged_df["Close"] - merged_df["Open"]
    merged_df["Volatility"] = merged_df["High"] - merged_df["Low"]
    print("Cleaned Dataset Summary:")
    merged_df.info()
    return merged_df

def analyze_data(df):
    """
    Performs statistical analysis and saves results as CSV files.
    """
    if df is None:
        print("No data to analyze!")
        return

    # stats
    stats_price_change = df.groupby("Name")["Price Change"].agg(["mean", "min", "max"])
    stats_volatility = df.groupby("Name")["Volatility"].agg(["mean", "min", "max"])
    stats_price_change.to_csv("../analysis/Price_Change_Analysis.csv")
    stats_volatility.to_csv("../analysis/Volatility_Analysis.csv")
    print("Analysis saved as CSV files!")

# Main Entry Point
def kaggle_parser():
    """
    Main function to download, clean, and analyze Kaggle cryptocurrency data.
    """
    download_kaggle_dataset(DATASET_NAME, DOWNLOAD_PATH)
    cleaned_df = clean_data(DOWNLOAD_PATH)
    analyze_data(cleaned_df)

