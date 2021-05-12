import plotly.express as px
import requests
import pandas as pd


number_of_results = 100

url = f'https://api.opap.gr/draws/v3.0/1100/last/{number_of_results}'

response = requests.get(url)

# skip active game that has no result yet
json = [x for x in response.json() if x['status'] == 'results']

# get only the useful data
catalog = {'Draw ID': [],
           'Winning Numbers': [],
           'Winning Parity': [],
           'Draw Time': [],
           'Wagers': [],
           'Money Distributed': []}


# create dictionary with useful data
for game in json:
    catalog['Draw ID'].append(game['drawId'])
    catalog['Winning Numbers'].append(game['winningNumbers']['list'])
    catalog['Winning Parity'].append(game['winningNumbers']['sidebets']['winningParity'])
    catalog['Draw Time'].append(game['drawTime'])
    catalog['Wagers'].append(game['wagerStatistics']['wagers'])
    # get how much money are distrebuted in each draw
    money = 0
    for dic in game['prizeCategories']:
        money += dic['distributed']
    catalog['Money Distributed'].append((money))

old_df = pd.read_excel('KinoStats.xlsx', index_col=None)

df = pd.DataFrame(catalog)

# append the results to the old excel file
result = pd.concat([df, old_df], ignore_index=True)

lista = list(result['Draw ID'])

# filter duplicates on result df using a trueFalse list
unique = []
temp = []
for x in lista:
    if unique.count(x) > 0:
        temp.append(False)
    elif unique.count(x) == 0:
        unique.append(x)
        temp.append(True)

result = result.loc[temp]

# use index=False to avoid confusion with both df's indexes
result.to_excel("KinoStats.xlsx", index=False)

new_draws = len(result) - len(old_df)

print('Προστέθηκαν ', new_draws, ' νέες κληρώσεις')

print(result.head(new_draws))

