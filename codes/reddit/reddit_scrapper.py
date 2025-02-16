import praw
import pandas as pd
import os

def authenticate_reddit(client_id, client_secret, user_agent):
    """
    Authenticates with Reddit's API and returns a Reddit instance.
    """
    return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

def get_hot_posts(reddit, subreddit_name, post_limit=100):
    """
    Fetches hot posts from a specified subreddit.
    """
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=post_limit):
        posts.append([
            post.title,
            post.selftext,
            post.author.name if post.author else "Unknown",
            post.created_utc,
            post.score,
            post.subreddit.display_name,
        ])
    return posts

def convert_posts_to_dataframe(posts):
    """
    Converts a list of post data into a pandas DataFrame.
    """
    df = pd.DataFrame(
        posts, 
        columns=["Title", "Post Text", "Author", "Date", "Upvotes", "Subreddit"]
    )
    df["Date"] = pd.to_datetime(df["Date"], unit="s")
    return df

def save_dataframe_to_csv(df, output_file):
    """
    Saves a DataFrame to a CSV file.
    """
    # df.to_csv(output_file, index=False)
    # Define the path to the dataset folder in the previous directory
    file = os.path.join("..", "dataset", output_file)

# Save the DataFrame to the specified path
    df.to_csv(file, index=False)
    print(f"Data saved to {file}")


# Main Entry Point
def fetch_reddit_data(client_id, client_secret, user_agent, 
                      subreddit_name="cryptocurrency", post_limit=100, 
                      output_file="../dataset/crypto_reddit_data.csv"):
    """
    Data Orchastration
    1. Authenticate with Reddit.
    2. Fetch hot posts from the specified subreddit.
    3. Convert the post data into a DataFrame.
    4. Save the DataFrame to a CSV file.

    """

    reddit = authenticate_reddit(client_id, client_secret, user_agent)
    posts = get_hot_posts(reddit, subreddit_name, post_limit)
    df = convert_posts_to_dataframe(posts)
    save_dataframe_to_csv(df, output_file)
    return df
