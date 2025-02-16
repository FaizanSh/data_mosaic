from reddit.reddit_scrapper import fetch_reddit_data
from reddit.reddit_parser_and_visual import reddit_parser_and_vis
from google_trends.google_trends_scrapper import get_monthly_data
from google_trends.google_parser_and_visual import google_trends_parser
from kaggle_pipeline.Kaggle_module import kaggle_parser
from yahoo.yahoo_parser_and_visual import yahoo_data_fetch, yahoo_visualization

import json


def get_credentials():
    with open("config.json", "r") as file:
        credentials = json.load(file)
        print(credentials)
    return credentials

def reddit_pipeline(client_id, client_secret, user_agent, subreddit_name):
    # Call the function with API credentials
    fetch_reddit_data(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        subreddit_name=subreddit_name, 
        post_limit=100, 
        output_file="crypto_reddit_data.csv"
    )

def parse_months(months):
    """
    Parse the months dictionary from the config file into a format that the Google Trends API can understand.
    """
    # parse monthly data
    months = {month: (start_date, end_date) for month, (start_date, end_date) in months.items()} # Convert to dictionary
    return months


def visualize_google_trends(visualize_google):
    if visualize_google:
        google_trends_parser()

def visualize_reddit_data(visualize_reddit):
    if visualize_reddit:
        reddit_parser_and_vis()

def visualize_kaggle_data(visualize_kaggle):
    if visualize_kaggle:
        kaggle_parser()

def yahoo_viz(visualize_yahoo):
    if visualize_yahoo:
        yahoo_visualization()




if __name__ == "__main__":

    # # Get source configs
    # # Reddit Data Fetcher
    # print("Fetching data from Reddit...")
    credentials = get_credentials()
    print(credentials)
    client_id = credentials["Reddit"]["client_id"]
    client_secret = credentials["Reddit"]["client_secret"]
    user_agent = credentials["Reddit"]["user_agent"]
    subreddit_name = credentials["Reddit"]["subreddit_name"]
    visualize_reddit = credentials["Reddit"]["visualize"]

    reddit_pipeline(client_id, client_secret, user_agent, subreddit_name)
    visualize_reddit_data(visualize_reddit)
    print("Reddit data fetched successfully!")



    # # Google Trends Fetcher
    # print("Fetching data from Google Trends...")
    # keywords = credentials["Google"]["keywords"]
    # months = credentials["Google"]["months"]
    # visualize_google = credentials["Google"]["visualize"]

    # parse_months(months)
    # get_monthly_data(keywords, months  ,geo = 'SG')
    # visualize_google_trends(visualize_google)

    # print("Google Trends data fetched successfully!")
    


    # Kaggle Data Fetcher
    print("Fetching data from Kaggle...")

    # visualize_kaggle = credentials["Kaggle"]["visualize"]
    kaggle_parser()
    # visualize_kaggle_data(visualize_kaggle)

    print("Kaggle data fetched successfully!")
    


    # Yahoo Data Fetcher
    print("Fetching data from Yahoo...")

    visualize_yahoo = credentials["Yahoo"]["visualize"]
    
    yahoo_data_fetch()
    yahoo_viz(visualize_yahoo)
    print("Yahoo data fetched successfully")

    print("All tasks completed successfully!")