# Check a .md file in your obsidian vault and construct a time series
import pandas as pd
from os.path import exists

INPUT = '../../obsidian/living/fitness/Gym.md'
OUTPUT = 'history.csv'

if __name__ == '__main__':
    with open(INPUT, 'r') as f:
        lines = f.readlines()
    data = [] 
    for line in lines:
        if line[0] != "|":
            continue  
        # Data is kept in a markdown table
        data.append([l.strip() for l in line[1:-2].split("|")])
    header = data[0]
    data = data[2:]  
    df = pd.DataFrame(data, columns=header)
    if exists(OUTPUT):
        history = pd.read_csv("history.csv",index_col=0)
    else:
        history = pd.DataFrame()
    # Lines will be written to history if a column named 'check' contains an 'x'
    done = df[df.check.str.contains('x')] 
    done.check = pd.Timestamp.today().date()
    done.set_index("check", inplace=True)
    history = pd.concat([history, done])
    history.to_csv(OUTPUT)
    # Remove checkmarks
    with open(INPUT, 'w') as f:
        for line in lines:
            f.write(line.replace(' x ', '')) 