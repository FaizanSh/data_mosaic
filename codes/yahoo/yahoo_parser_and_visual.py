import yfinance as yf
import pandas as pd
import plotly.express as px

def fetch_crypto_data(tickers, period="2y"):
    """
    Fetches historical closing prices for given tickers using yfinance.
    """
    data = yf.download(tickers, period=period)["Close"]
    return data

def resample_crypto_data(data, sampling_time="2M"):
    """
    Resamples the data to a specified frequency and calculates the mean values.
    """
    resampled_data = data.resample(sampling_time).mean()
    return resampled_data

def create_crypto_plot(data, tickers):
    """
    Creates a Plotly line chart for the provided cryptocurrency data.
    """
    fig = px.line(
        data,
        x=data.index,
        y=tickers,
        title="Cryptocurrency Average Prices",
        labels={"value": "Price (USD)", "index": "Date"},
        markers=True
    )

    fig.update_layout(
        plot_bgcolor="black",       # Plot background color
        paper_bgcolor="black",       # Paper background color
        yaxis_title="Value (USD)",
        xaxis_title_font=dict(color="white", size=14),
        yaxis_title_font=dict(color="white", size=14),
        xaxis_tickfont=dict(color="white", size=12),
        yaxis_tickfont=dict(color="white", size=12),
        title_font=dict(color="white", size=20)
    )
    return fig

# Main Entry Point
def yahoo_data_fetch(tickers=["BTC-USD", "ETH-USD", "DOGE-USD", "SOL-USD", "BNB-USD"], sampling_time="2M"):
    """
    Main function that orchestrates fetching, processing, and visualizing cryptocurrency data.
    """
    # Fetch data from Yahoo Finance
    crypto_data = fetch_crypto_data(tickers, period="2y")
    crypto_data.to_csv("../dataset/raw/yahoo_crypto_data.csv", index=False)
    
    # Resample the data
    crypto_resampled = resample_crypto_data(crypto_data, sampling_time)

    # Write data to csv
    # crypto_resampled.to_csv("../dataset/raw/yahoo_crypto_data.csv", index=False)
    crypto_resampled.to_csv("../analysis/yahoo_crypto_resampled_data.csv", index=False)
    
    return crypto_resampled

def yahoo_visualization():
    """
    Main function to fetch, process, and visualize Yahoo Finance cryptocurrency data.
    """
    read_data = pd.read_csv("../dataset/raw/yahoo_crypto_data.csv")
    
    # Create Plot
    fig = create_crypto_plot(read_data, ["BTC-USD", "ETH-USD", "DOGE-USD", "SOL-USD", "BNB-USD"])
    import plotly.io as pio

    # pio.renderers.default = "browser"
    import plotly.io as pio
    pio.renderers.default = "vscode"

    fig.show()

    
    # fig.show()
