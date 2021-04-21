import pandas as pd
import plotly.express as px
import pathlib

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Start the Dashboard
app = Dash(__name__)

# Import Data from csv
PATH = pathlib.Path(__file__).parent
PATH = PATH.joinpath('Dataset')
df = pd.read_csv(PATH.joinpath('intro_bees.csv'))

# Clean data
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]

# App Layout
app.layout = html.Div([

    html.H1('My first Dashboard', style={'text-align': 'center'}),

    dcc.Dropdown(id='bee_killers',
                 options=[{'label': i, 'value': i} for i in bee_killers],
                 multi=False,
                 value='Disease',
                 style={'width': '40%'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='bee_killers', component_property='value')]
)
def update_graph(option_selected1):
    print(option_selected1)

    container = f'The bee killer chosen by user was: {option_selected1} for States Alabama, Arizona and Florida'

    df_copy = df.copy()
    df_copy = df_copy[df_copy['Affected by'] == option_selected1]
    df_copy = df_copy[
        (df_copy['State'] == 'Alabama') | (df_copy['State'] == 'Arizona') | (df_copy['State'] == 'Florida')]

    print(df_copy)

    # Plotly Express
    fig = px.line(data_frame=df_copy, x='Year', y='Pct of Colonies Impacted', title='% Chart', color='State')

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
