import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
from front_end import navbar, collapse
from analyse_data.regionalizar_distritos import RegionalizarDistritos

regionalizar = RegionalizarDistritos()

def gerar_geodf(anos_ideb):

    geodf = regionalizar(anos_ideb)

    geodf['geometry'] = geodf['geometry'].to_crs(epsg=4126)
    geodf.rename({'ds_nome' : 'Distrito'}, axis=1, inplace=True)
    geodf.set_index('Distrito', inplace=True)

    return geodf

def gerar_mapa(geodf):

    fig = px.choropleth(
        geodf,
        geojson=geodf.geometry,
        locations=geodf.index,
        color = 'ideb_2019',
        color_continuous_scale = 'Reds'
        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, width=1000, height=400)

    return fig

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Regionalização IDEB 2019'
server = app.server

app.layout = html.Div([
    navbar,
    html.H4("Média da pontuação no IDEB 2019 por Distrito - Rede Municipal"),
    html.H5("Anos ensino básico:"),
    dcc.Dropdown(
        id='anos_ideb', 
        options=[{'label' : 'Anos Finais', 'value' : 'finais'},
        {'label' : 'Anos iniciais', 'value' : 'iniciais'}],
        value='iniciais',
    ),
    dcc.Graph(id="choropleth"),
    collapse
])

@app.callback(
    Output("choropleth", "figure"), 
    [Input("anos_ideb", "value")])
def display_choropleth(anos_ideb):

    geodf = gerar_geodf(anos_ideb)
    fig = gerar_mapa(geodf)

    return fig

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == "__main__":

    app.run_server(debug=True)