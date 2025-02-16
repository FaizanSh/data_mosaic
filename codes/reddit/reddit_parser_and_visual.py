import glob
import pandas as pd
import plotly.express as px
import os

def find_reddit_csv_files(pattern="*reddit*.csv"):
    """
    Finds CSV files matching the provided pattern.
    """
    # files = glob.glob(pattern)
    dataset_folder = os.path.join("..", "dataset")  # Path to dataset folder
    files = glob.glob(os.path.join(dataset_folder, pattern))  # Search in dataset folder
    return files

def load_reddit_data(file_path):
    """
    Loads Reddit CSV data from the given file.
    """
    return pd.read_csv(file_path)

def process_reddit_data(df, resample_interval="2h"):
    """
    Processes the Reddit data for visualization by:
    - Converting the 'Date' column to datetime.
    - Setting 'Date' as the index.
    - Resampling the data over the specified interval.
    - Resetting the index and formatting the 'Date' column.
    """

    # Convert 'Date' column to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Set 'Date' as index
    df.set_index("Date", inplace=True)
    
    # Resample data and sum up the upvotes
    df_resampled = df.resample(resample_interval).sum()
    
    # Reset index for plotting and format 'Date'
    df_resampled.reset_index(inplace=True)
    df_resampled["Date"] = df_resampled["Date"].dt.strftime("%Y-%m-%d %H:%M")
    
    return df_resampled

def create_reddit_plot(df, title="Reddit Crypto related Upvotes per 2-Hour Interval"):
    """
    Creates a Plotly scatter plot for the processed Reddit data.
    """
    fig = px.scatter(
        df,
        x="Date",
        y="Upvotes",
        title=title,
        labels={"Upvotes": "Total Upvotes", "Date": "Time"},
        hover_data=["Upvotes"]
    )
    
    fig.update_layout(
        xaxis=dict(
            tickangle=45,           # Rotate ticks for better visibility
            tickformat="%Y-%m-%d %H:%M",  # Display both date and time
            title="Date and Time"
        ),
        width=1200,                  # Set plot width
        height=600,                  # Set plot height
        plot_bgcolor="black",        # Plot background color
        paper_bgcolor="black",       # Paper background color
        xaxis_title_font=dict(color="white", size=14),
        yaxis_title_font=dict(color="white", size=14),
        xaxis_tickfont=dict(color="white", size=12),
        yaxis_tickfont=dict(color="white", size=12),
        title_font=dict(color="white", size=20)
    )
    return fig

# Main Entry Point
def reddit_parser_and_vis():
    """
    Orchestrates the process of finding, loading, processing, and visualizing
    Reddit data from CSV files.
    """
    files = find_reddit_csv_files()
    print("Found files:", files)
    
    if not files:
        print("No Reddit CSV files found.")
        return None
    
    # Load data from the first matching file
    df = load_reddit_data(files[0])
    
    # Process data for visualization
    processed_df = process_reddit_data(df, resample_interval="2h")
    
    # Create and display the plot
    fig = create_reddit_plot(processed_df)
    fig.show()
