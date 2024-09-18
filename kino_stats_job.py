import time
import os
from datetime import datetime
import pytz
import requests
import pandas as pd
import gc

def update_kino_stats(old_df_filename):
    number_of_results = 100
    url = f'https://api.opap.gr/draws/v3.0/1100/last/{number_of_results}'

    # Fetch data from API
    response = requests.get(url)
    data = [x for x in response.json() if x['status'] == 'results']

    # Create dictionary with useful data
    catalog = {
        'Draw ID': [game['drawId'] for game in data],
        'Winning Numbers': [game['winningNumbers']['list'] for game in data],
        'Winning Parity': [game['winningNumbers']['sidebets']['winningParity'] for game in data],
        'Draw Time': [datetime.fromtimestamp(game['drawTime'] / 1000) for game in data]
    }

    # Check if the old DataFrame file exists and load it; if not, create an empty DataFrame
    if os.path.exists(old_df_filename):
        old_df = pd.read_csv(old_df_filename)
    else:
        old_df = pd.DataFrame(columns=catalog.keys())

    # Create DataFrame for new results
    new_df = pd.DataFrame(catalog)

    # Combine new and old data, drop duplicates based on 'Draw ID'
    combined_df = pd.concat([new_df, old_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset='Draw ID', keep='first')

    # Save the updated DataFrame
    combined_df.to_csv(old_df_filename, index=False)

    # Print the number of new draws and display them
    new_draws = len(combined_df) - len(old_df)
    print(f'Added ({new_draws}) new draws')
    # print(combined_df.tail(new_draws))

    # Clean up memory
    del data, catalog, new_df, combined_df
    gc.collect()


def get_greek_time():
    # Get the current time in the 'Europe/Athens' timezone
    tz = pytz.timezone('Europe/Athens')
    return datetime.now(tz)

def main():
    while True:
        current_time = get_greek_time()
        start_time = current_time.replace(hour=8, minute=0, second=0, microsecond=0)
        end_time = current_time.replace(hour=23, minute=0, second=0, microsecond=0)

        # Check if current time is within the range
        if start_time <= current_time <= end_time:
            # Sleep for 5 minutes
            update_kino_stats('kino_stats.csv')
            time.sleep(300) # 5 minutes in seconds
        else:
            # Sleep for 9 hours  before checking again
            time.sleep(32400) # 9 hours in seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted.")
    finally:
        os._exit(0)
