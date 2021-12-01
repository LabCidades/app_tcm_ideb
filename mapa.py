import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
# import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import json
# from front_end import navbar, collapse
# from analyse_data.regionalizar_distritos import RegionalizarDistritos
from get_data import obterIdeb, obterDistritos  # , obterSubprefeituras, get_data, get_distritos, get_subprefeituras

dfDadosIdeb = obterIdeb.dadosIdeb('data/cadastro_ideb_merged.csv')
dfDadosIdeb['ideb_2019'] = dfDadosIdeb['ideb_2019'].fillna(0)
dfDadosIdeb['coddist'] = dfDadosIdeb['coddist'].fillna(0)
dfDadosIdeb['codsub'] = dfDadosIdeb['codsub'].fillna(0)

totalEscolas = len(pd.unique(dfDadosIdeb["codigo_escola"]))

filt = (dfDadosIdeb["tipo_anos"] == "iniciais")
df_filt = dfDadosIdeb[filt]
dfDadosIdebIniciais = df_filt.reset_index()

filt = (dfDadosIdeb["tipo_anos"] == "finais")
df_filt = dfDadosIdeb[filt]
dfDadosIdebFinais = df_filt.reset_index()


dfDadosDistritos = obterDistritos.distritos('data/geo_data/SIRGAS_SHP_distrito', dfDadosIdebIniciais, dfDadosIdebFinais)

df = px.data.election()
geojson = px.data.election_geojson()
candidates = df.winner.unique()


dfjson = json.load(open('c:\\c2\\myshpfile.geojson', 'r'))

geojson1 = json.loads(dfDadosDistritos.geometry.to_json())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H6("Observatório de Políticas Publicas - TCMSP"),
                html.P(""),
            ]),
        ], md=4),

        dbc.Col([

            html.Div([
                html.P("Candidate:"),
                dcc.RadioItems(
                    id='candidate',
                    options=[{'value': x, 'label': x}
                             for x in candidates],
                    value=candidates[0],
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Graph(id="choropleth"),
            ])

        ], md=8)

    ])

])


@app.callback(
    Output("choropleth", "figure"),
    [Input("candidate", "value")])
def display_choropleth(candidate):
    anos_ideb = "ideb_iniciais"
    geodf = dfDadosDistritos
    geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
    geodf['text'] = geodf['ds_nome'] + ':<br>Nota média:' \
        + geodf[anos_ideb].apply(
        lambda x: str(round(x, 2)) if not x == 0 else 'Não se aplica')

    min_ideb = geodf[anos_ideb].min()
    fig = go.Figure(data=go.Choropleth(
        geojson=json.loads(geodf.geometry.to_json()),
        locations=geodf.index,
        z=geodf[anos_ideb],
        colorscale='Reds',
        autocolorscale=False,
        text=geodf['text'],  # hover text
        hoverinfo='text',
        colorbar_title="IDEB 2019",
        zmin=min_ideb,
        zmax=geodf[anos_ideb].max(),
    ))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=True, height=500)

    return fig


app.run_server(debug=True)
