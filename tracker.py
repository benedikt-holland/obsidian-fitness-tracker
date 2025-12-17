# Check a .md file in your obsidian vault and construct a time series
import pandas as pd
import numpy as np
from os.path import exists
from functions import read_md, to_md 
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-path", type=str, required=True
    )
    parser.add_argument(
        "-o", "--output-path", type=str, required=True
    )
    parser.add_argument(
        "-g", "--goal-path", type=str
    )
    args = parser.parse_args()
    input_file = args.input_path
    output_file = args.output_path
    df = read_md(input_file)
    if exists(output_file):
        history = pd.read_csv(output_file, index_col=0)
    else:
        history = pd.DataFrame()
    # Lines will be written to history if a column named 'value' contains a value
    if "max" in df.columns and "last" in df.columns:
        df["max"] = df[["last", "max", "value"]].replace("", np.nan).astype(float).max(axis=1).apply(lambda x: f"{int(x)}" if x.is_integer() else f"{x}")
        df.loc[df.value != "", "last"] = df.loc[df.value != "", "value"]
    done = df[df.value != ""].copy(deep=True)
    done["date"] = pd.Timestamp.today().date()
    done.set_index("date", inplace=True)
    if args.goal_path:
        goals = read_md(args.goal_path)
        done = done.join(goals.set_index(["category", "subcategory"]), on=["category", "subcategory"])
    history = pd.concat([history, done])
    history.to_csv(output_file)
    # Reset value
    df.value = ""
    if "satisfaction" in df.columns:
        df.satisfaction = "" 
    to_md(df, input_file)
