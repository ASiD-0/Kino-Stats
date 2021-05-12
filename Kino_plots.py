import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from plotly.subplots import make_subplots

df = pd.read_excel('KinoStats.xlsx')

winning = []
for numbers in df['Winning Numbers']:
    winning += json.loads(numbers)

frequency = {}
for i in range(1,81):
    frequency[i] = winning.count(i)

parity_freq = {'draw': 0,
               'odd': 0,
               'even': 0}

for elem in df['Winning Parity']:
    parity_freq[elem] += 1

# print(parity_freq)

df_freq = pd.DataFrame({'number': frequency.keys(),
                        'frequency': frequency.values()})
df_parity = pd.DataFrame({'kind': parity_freq.keys(),
                          'frequency': parity_freq.values()})

# print(df_freq)


df = df[df['Wagers'].notnull()]

print(df)

# in x axis we use to_datetime to translate epoch time of milliseconds into readable datetime
wagers_fig = make_subplots(rows=2, cols=1,
                    subplot_titles=( "Λεφτά που μοιράζονται στους παίκτες", "Αριθμός παικτών μέσα στη μέρα"),
                    specs=[[{"type": "bar"}],[ {"type": "bar"}]])


wagers_fig.add_trace(
    go.Bar(x=pd.to_datetime(df['Draw Time'], unit='ms'),
           y=df['Money Distributed'],
           ),
    row=1, col=1
)

wagers_fig.add_trace(
    go.Bar(x=pd.to_datetime(df['Draw Time'], unit='ms'),
           y=df['Wagers']),
    row=2, col=1
)

wagers_fig.update_layout(height=900, width=1900, title_text="Στατιστικά KINO", )

wagers_fig.show()

# wagers_fig = go.Figure(go.Bar(x=pd.to_datetime(df['Draw Time'], unit='ms'), y=df['Wagers']))
# wagers_fig.show()

# 2 pie plots
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("Συχνότητα Εμφάνησης Αριθμών", "Συχνότητα Μονά-Ζυγά"),
                    specs=[[{"type": "pie"}, {"type": "pie"}]])


# frequency pie chart

fig.add_trace(
    go.Pie(labels=df_freq['number'],
           values=df_freq['frequency'],

           ),
    row=1, col=1
)

# oddEven pie chart
fig.add_trace(
    go.Pie(labels=df_parity['kind'],
           values=df_parity['frequency'],
           textinfo='label+percent',
            marker={'colors': ['gold', 'mediumturquoise', 'darkorange', 'lightgreen'],
                    'line': dict(color='#000000', width=2)
                   }
           ),
    row=1, col=2
)
fig.update_layout(height=1080, width=1920, title_text="Στατιστικά KINO", )

fig.show()

