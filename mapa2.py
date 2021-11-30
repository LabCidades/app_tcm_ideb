import pandas as pd
import dash
from urllib.request import urlopen
import json
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

fips_choices = df['fips'].sort_values().unique()

loading_style = {'position': 'absolute', 'align-self': 'center'}

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Dropdown(id='dropdown1',
                 options=[{'label': i, 'value': i} for i in fips_choices],
                 value=fips_choices[0]
                 ),
    html.Div([dcc.Graph(id='us_map', style={'flex-grow': '1'}),
              dcc.Loading(id='loading', parent_style=loading_style)
              ], style={'position': 'relative', 'display': 'flex', 'justify-content': 'center'}
             )
])


@app.callback(
    [Output('us_map', 'figure'),
     Output('loading', 'parent_style')
     ],
    Input('dropdown1', 'value')
)
def update_map(county_select):
    new_loading_style = loading_style
    # Initial load only
    # new_loading_style['display'] = 'none'
    new_df = df[df['fips'] == county_select]
    fig = px.choropleth_mapbox(new_df, geojson=counties, locations='fips', color='unemp',
                               color_continuous_scale="Viridis",
                               range_color=(0, 12),
                               mapbox_style="carto-positron",
                               zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                               opacity=0.5
                               )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig, new_loading_style


app.run_server(host='0.0.0.0', port='8051')
