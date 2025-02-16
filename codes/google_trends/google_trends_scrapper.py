import time
import pandas as pd
import os
from pytrends.request import TrendReq

def initialize_pytrends(hl='en-US', tz=360):
    """
    Initializes and returns a pytrends request object.
    """
    return TrendReq(hl=hl, tz=tz)

def fetch_trends_data(pytrends, keywords, timeframe, geo='SG'):
    """
    Builds the payload and fetches interest over time data for the given timeframe.
    """
    pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
    return pytrends.interest_over_time()

def process_trends_data(df):
    """
    Processes the trends data by:
      - Resetting the index to include the date.
      - Extracting the most frequent year from the 'date' column.
      - Renaming columns for clarity.
    """
    # Reset the index to include the date column
    df.reset_index(inplace=True)
    # Extract the most frequent year in the data
    extracted_year = df["date"].dt.year.mode()[0]
    
    # Rename columns for clarity
    df.rename(columns={
        'date': 'date/time',
        'Bitcoin': 'Bitcoin_interest_score',
        'Crypto': 'Crypto_interest_score'
    }, inplace=True)
    
    return df, extracted_year

def save_trends_data(df, month, year):
    """
    Saves the processed trends data to a CSV file with a dynamic filename in the ../dataset/raw/ folder.
    """
    # Define the dataset directory relative to the current working directory
    dataset_dir = "../dataset/raw"
    
    # Create the directory if it doesn't exist
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Build the filename and complete file path
    filename = f"crypto_trends_{month.lower()}_{year}.csv"
    filepath = os.path.join(dataset_dir, filename)
    
    # Save the DataFrame as a CSV to the specified filepath
    df.to_csv(filepath, index=False)
    print(f"Data for {month} saved as {filepath}")


# Main Entry Point
def get_monthly_data(keywords, months, geo='SG'):
    """
    Orchestrates the process of fetching, processing, and saving Google Trends data on a monthly basis.
    """
    pytrends = initialize_pytrends()
    
    for month, (start_date, end_date) in months.items():
        timeframe = f"{start_date} {end_date}"
        print(f"\nFetching data for {month} ({timeframe})...")
        
        # Fetch data for the current month
        trends_df = fetch_trends_data(pytrends, keywords, timeframe, geo)
        
        # Process the fetched data
        processed_df, extracted_year = process_trends_data(trends_df)
        
        # Save the processed data to a CSV file
        save_trends_data(processed_df, month, extracted_year)
        
        # Wait 3 minutes before fetching the next month
        print(f"Waiting for 3 minutes before fetching next month...")
        time.sleep(180)
    
    print("\nAll data extraction completed successfully!")
    print("Goodbye!")
