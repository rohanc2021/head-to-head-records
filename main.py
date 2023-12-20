import json
import pandas as pd


def format_data(raw_data: dict) -> dict[str, list[int]]:
    formatted_data = {}
    team1_index = 0  # Keeps track of which team we are iterating through WL data for
    # Iterate through data for each team
    for team, records in raw_data.items():
        team2_index = 0  # Keeps track of the head-to-head opponent's index
        formatted_data[team] = []

        # Iterate through data for current team
        for wl in records.values():
            wins = wl['W']  # Get win count
            if team2_index == team1_index:  # Add filler where team is compared to itself
                formatted_data[team].append('--')
            formatted_data[team].append(wins)  # Append relevant data

            team2_index += 1
        team1_index += 1

    formatted_data[list(formatted_data)[-1]].append('--')  # Add filler for final team
    return formatted_data


if __name__ == '__main__':
    with open('data.json', 'r') as f:
        data = json.load(f)

    # Get formatted data and column names (list of teams)
    win_data = format_data(data)
    teams_list = list(win_data.keys())

    # Create table
    df = pd.DataFrame.from_dict(data=win_data, orient='index', columns=teams_list)
    # Add columns to bottom of table
    df = df._append(pd.Series(name='Tm'))
    df.iloc[-1] = df.columns
    # Add tm to upper left
    df.columns.name = 'Tm'

    # Display table
    print(df.to_string())
