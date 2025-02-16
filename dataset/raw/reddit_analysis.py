import glob
import pandas as pd

def basic_reddit_info():
    files = glob.glob("*yahoo*.csv")
    print("Found files:", files)
    df = pd.read_csv(files[0])
    print(df.info())

basic_reddit_info()