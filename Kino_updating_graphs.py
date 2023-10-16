import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import json
from math import floor
from plotly.subplots import make_subplots




type = 'range'


app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
        dcc.Input(
            id=f"input-{type}",
            type=type,
            value=100,
            placeholder=f"input type {type}",

        ),
    # dcc.Input(
    #     id="input-number",
    #     type='number',
    #     value=50,
    #     placeholder=f"input type number",
    #
    # ),
    html.Div(id="out-all-types"),

    dcc.Graph(id='Kino-stats', style={'height': '90vh'}, figure={})
])


@app.callback(
    [Output(component_id='out-all-types', component_property='children'),
     Output(component_id='Kino-stats', component_property='figure')],
    [Input(component_id=f'input-{type}', component_property='value')]
)
def update_output(user_choice):
    print(len(df))

    user_choice = int(floor(float(user_choice)) * len(df)/100)
    container = ''
    # print(user_choice)
    # trace = go.Bar(x=pd.to_datetime(df['Draw Time'][:user_choice], unit='ms'),
    #                y=df['Wagers'][:user_choice])

    wagers_fig = make_subplots(rows=2, cols=1,
                               subplot_titles=("Λεφτά που μοιράζονται στους παίκτες", "Αριθμός παικτών μέσα στη μέρα"),
                               specs=[[{"type": "bar"}], [{"type": "bar"}]],
                               vertical_spacing=0.15,
                               shared_xaxes=True,
                               )
    wagers_fig.add_trace(
        # in x axis we use to_datetime to translate epoch time of ms into readable date, 'ms' because our time is 13bit num
        go.Bar(x=pd.to_datetime(df['Draw Time'][:user_choice], unit='ms'),
               y=df['Money Distributed'][:user_choice],
               ),
        row=1, col=1
    )

    wagers_fig.add_trace(
        go.Bar(x=pd.to_datetime(df['Draw Time'][:user_choice], unit='ms'),
               y=df['Wagers'][:user_choice]),
        row=2, col=1
    )

    wagers_fig.update_layout(title_text="Στατιστικά KINO 1")
    # set your desired layout of the graph
    # layout = go.Layout(
    #     # template='plotly_dark',
    #     title='Κινο Στατιστικά',
    #     # title_x=0.5,  # centers the title
    #     yaxis=dict(
    #         title='Αριθμός παικτών'
    #     ),
    #     xaxis=dict(
    #         title='Ημερομηνίες'
    #     )
    #     # height=1080
    #
    # )

    # fig = go.Figure(data=trace, layout=layout )
    return container, wagers_fig


def make_freq():
    df = pd.read_excel('KinoStats.xlsx')
    # get winning numbers frequency
    winning = []
    frequency = {}
    for numbers in df['Winning Numbers']:
        winning += json.loads(numbers)
    for i in range(1, 81):
        frequency[i] = winning.count(i)

    # get parity frequency
    parity_freq = {'draw': 0,
                   'odd': 0,
                   'even': 0}
    for elem in df['Winning Parity']:
        parity_freq[elem] += 1

    df_freq = pd.DataFrame({'number': frequency.keys(),
                            'frequency': frequency.values()})
    df_parity = pd.DataFrame({'kind': parity_freq.keys(),
                              'frequency': parity_freq.values()})
    # as df keep the rows that are not NaN in Wagers column

    df = df[df['Money Distributed'].notnull()]

    print(df)
    return df, df_parity, df_parity

if __name__ == '__main__':
    df, parity, freq = make_freq()

    app.run_server(debug=True)
