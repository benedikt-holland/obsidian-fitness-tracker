# Check a .md file in your obsidian vault and construct a time series
import pandas as pd
from os.path import exists
from functions import read_md 
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-path", type=str, required=True
    )
    parser.add_argument(
        "-o", "--output-path", type=str, required=True
    )
    parser.add_argument('--process', action='store_true', default=False)
    args = parser.parse_args()
    input_file = args.input_path
    output_file = args.output_path
    df = read_md(input_file)
    if exists(output_file):
        history = pd.read_csv(output_file)
        original_cols = history.columns
        history = history.groupby(["category", "subcategory"]).last()
        latest = df.groupby(["category", "subcategory"]).last()
        latest = latest.join(history, rsuffix="_last")
        latest.reset_index(inplace=True)
        latest.goal = latest.goal.astype(int)
        latest.goal_last = latest.goal_last.astype(int)
        latest = latest[latest["goal"] != latest["goal_last"]]
        latest[original_cols].set_index("date").to_csv(output_file, mode="a", header=False)
    else:
        df["date"] = pd.Timestamp.today().date()
        df.set_index("date").to_csv(output_file)