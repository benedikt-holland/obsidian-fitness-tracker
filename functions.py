import pandas as pd


def read_md(path):
    with open(path, "r") as f:
        lines = f.readlines()
    data = []
    for line in lines:
        if line[0] != "|":
            continue
        # Data is kept in a markdown table
        data.append([l.strip() for l in line[1:-2].split("|")])
    header = data[0]
    data = data[2:]
    return pd.DataFrame(data, columns=header)


def to_md(df: pd.DataFrame, path):
    with open(path, "w") as f:
        # Header
        f.write("| " + " | ".join(df.columns) + " |\n")
        # ----
        f.write("".join(["| - " for _ in df.columns]) + "|\n")
        # Content
        df.apply(lambda x: f.write("| " + " | ".join(x) + " |\n"), axis=1)
