import pandas as pd
from functions import read_md, to_md
import argparse


DAY_WEIGHT = 1
CATEGORY_WEIGHT = 1
SUBCATEGORY_WEIGHT = 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input-file", type=str, required=True
    )
    parser.add_argument(
        "-d", "--dashboard-file", type=str, required=True
    )
    parser.add_argument(
        "-g", "--goal-file", type=str, required=True
    )
    args = parser.parse_args()
    history = pd.read_csv(args.input_file)
    history.rename({"Unnamed: 0": "check"}, axis=1, inplace=True)
    dashboard = read_md(args.dashboard_file)
    orig_columns = dashboard.columns
    dashboard["full_name"] = dashboard.name + " " + dashboard.variant
    history["full_name"] = history.name + " " + history.variant
    history.check = pd.to_datetime(history.check)
    history["day_diff"] = history.check.rsub(pd.Timestamp.now()).dt.days
    # Count number of entries by column
    cols = ["category", "subcategory"]
    group_cols = []
    for col in ["category", "subcategory", "full_name"]:
        group_cols.append(col)
        dashboard = dashboard.join(
            history.groupby(group_cols).count().check.rename(col),
            on=group_cols,
            rsuffix="_count",
        )
        dashboard[col + "_count"] = dashboard[col + "_count"].fillna(0)
    # Add to main df
    dashboard = dashboard.join(
        history.groupby(cols).min(numeric_only=True).day_diff.rename("days"), on=cols
    )
    # Calculate relative amounts
    total = history.shape[0]
    for col in [c + "_count" for c in cols]:
        dashboard[col.split("_")[0] + "%"] = (dashboard[col] / total).fillna(0)
        total = dashboard[col]
    # Goals contains the relative amount of category and subcategory counts wanted
    goals = read_md(args.goal_file)
    goals.goal = goals.goal.astype(int)
    total = goals.goal.sum()
    group_cols = []
    for col in cols:
        group_cols.append(col)
        goals = goals.join(
            goals.groupby(group_cols).sum()["goal"].rename(col),
            on=group_cols,
            rsuffix="_total",
        )
        goals[col + "%"] = goals[col + "_total"] / total
        total = goals[col + "_total"]
    dashboard = dashboard.join(
        goals.set_index(cols).add_suffix("_goal"),
        on=cols,
    )
    # Calculate score
    for col in cols:
        # Score should always be positive
        # Higher score means the exercise was done less than expected
        # Lower score means the exercise was done more than expected
        dashboard[col + "_score"] = 1 + dashboard[col + "%_goal"] - dashboard[col + "%"]
    dashboard["score"] = (
        CATEGORY_WEIGHT * dashboard.category_score
        + SUBCATEGORY_WEIGHT * dashboard.subcategory_score
    )
    # Recently done exercises should have a lower score
    dashboard["day_score"] = (
        dashboard["days"].fillna(dashboard.days.max()) * dashboard.score
    )
    dashboard = dashboard.sort_values(
        ["day_score", "category", "subcategory", "full_name_count", "full_name"], ascending=[False, False, False, False, False] 
    )
    dashboard = dashboard[orig_columns]
    to_md(dashboard, args.dashboard_file)
