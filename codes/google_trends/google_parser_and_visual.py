import glob
import pandas as pd
import plotly.graph_objects as go

def find_crypto_csv_files(pattern="crypto*.csv"):
    """
    Finds CSV files matching the provided pattern in the ../dataset/raw/ folder.
    """
    search_path = f"../dataset/raw/{pattern}"
    files = glob.glob(search_path)
    print("Found files:", files)
    return files

def load_and_merge_csv_files(files):
    """
    Loads and merges multiple CSV files into a single DataFrame.
    """
    df_list = [pd.read_csv(file) for file in files]
    merged_df = pd.concat(df_list, ignore_index=True)
    print(merged_df.info())
    return merged_df

def process_trends_data(df, date_col="date/time"):
    """
    Processes the trends DataFrame by converting date columns to datetime.
    """
    df[date_col] = pd.to_datetime(df[date_col])
    return df

def create_trends_plot(df, date_col="date/time"):
    """
    Creates a Plotly figure with interest score traces.
    """
    fig = go.Figure()
    
    # Add trace for Bitcoin Interest Score
    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df["Bitcoin_interest_score"],
        mode="markers",
        name="Bitcoin Interest Score",
        connectgaps=False
    ))
    
    # Add trace for Crypto Interest Score
    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df["Crypto_interest_score"],
        mode="markers",
        name="Crypto Interest Score",
        connectgaps=False
    ))
    
    # Update layout for better styling and readability
    fig.update_layout(
        title="Google Trends Interest Scores",
        xaxis_title="Date",
        yaxis_title="Interest Score",
        xaxis=dict(
            tickangle=45
        ),
        legend_title="Trend",
        hovermode="x unified",
        width=1200,
        height=600,
        plot_bgcolor="black",
        paper_bgcolor="black",
        xaxis_title_font=dict(color="white", size=14),
        yaxis_title_font=dict(color="white", size=14),
        xaxis_tickfont=dict(color="white", size=12),
        yaxis_tickfont=dict(color="white", size=12),
        title_font=dict(color="white", size=20)
    )
    return fig

# Main Entry Point
def google_trends_parser():
    """
    Orchestrates the process of finding, loading, processing, and visualizing
    Google Trends data from CSV files.
    """
    # Find files
    files = find_crypto_csv_files()
    if not files:
        print("No matching CSV files found.")
        return None
    
    # Load and merge data from CSV files
    merged_df = load_and_merge_csv_files(files)
    
    # Process the merged DataFrame
    processed_df = process_trends_data(merged_df, date_col="date/time")
    
    # Create and show the plot
    fig = create_trends_plot(processed_df, date_col="date/time")
    fig.show()
