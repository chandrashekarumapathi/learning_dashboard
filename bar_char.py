import pandas as pd
import plotly.express as px
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
PATH = pathlib.Path(__file__).parent
PATH = PATH.joinpath('Dataset')
df = pd.read_csv(PATH.joinpath('intro_bees.csv'))

# Clean data
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    dcc.Graph(id='my_bee_map', figure={}),

    dcc.Dropdown(id='bee_killers',
                 options=[{'label': i, 'value': i} for i in bee_killers],
                 multi=False,
                 value='Disease',
                 style={'width': '40%'}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='second_graph', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure'),
     Output(component_id='second_graph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
     Input(component_id='bee_killers', component_property='value')]
)
def update_graph(option_slctd, option_selected1):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    df_copy = df.copy()
    df_copy = df_copy[df_copy['Affected by'] == option_selected1]
    df_copy = df_copy[
        (df_copy['State'] == 'Alabama') | (df_copy['State'] == 'Arizona') | (df_copy['State'] == 'Florida')]

    fig1 = px.line(data_frame=df_copy, x='Year', y='Pct of Colonies Impacted', title='% Chart', color='State')

    # Plotly Express
    fig = px.bar(data_frame=dff, x='State', y='Pct of Colonies Impacted', color='Pct of Colonies Impacted')

    return container, fig, fig1


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
