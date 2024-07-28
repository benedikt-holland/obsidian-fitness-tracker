# Check a .md file in your obsidian vault and construct a time series
import pandas as pd
from os.path import exists
import os
from functions import read_md, to_md


if __name__ == "__main__":
    input = os.getenv("DASHBOARD")
    output = os.getenv("HISTORY")
    df = read_md(input)
    if exists(output):
        history = pd.read_csv("history.csv", index_col=0)
    else:
        history = pd.DataFrame()
    # Lines will be written to history if a column named 'value' contains a value
    df["max"] = df[["last", "max", "value"]].max(axis=1)
    done = df[df.value != ""].copy(deep=True)
    done["date"] = pd.Timestamp.today().date()
    done.set_index("date", inplace=True)
    history = pd.concat([history, done])
    history.to_csv(output)
    # Reset value
    df.loc[df.value != "", "last"] = df.loc[df.value != "", "value"]
    df.value = ""
    to_md(df, os.getenv("DASHBOARD"))
