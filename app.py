# coding=utf-8
import dash
# from dash import dcc
# from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_table.Format import Format, Scheme, Group  # , Symbol
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import json
import pandas as pd
# from front_end import navbar, collapse
# from analyse_data.regionalizar_distritos import RegionalizarDistritos
from get_data import obterIdeb, obterDistritos, obterSubprefeituras  # , get_data, get_distritos, get_subprefeituras
import dash_table
import plotly.io as pio

# Para desativar modo escuro dos gráficos torne esta sessão em um comentário
# Declarando o tema escuro para aplicar aos plots
plotly_template = pio.templates["plotly_dark"]
pio.templates.default = "plotly_dark"

formatted = {'locale': {':,.2f'}, 'nully': '', 'prefix': None, 'specifier': ''}
###

# Declarando o tema escuro que é aplicado nas propriedades
# Isso normalmente é aplicado após o app = dash.Dash(__name__)
# Porém como há cards declarados em variáveis fora dele se fez necessário declarar ele aqui
colors = {
    # 'background': '#000000',  # Modo escuro
    # 'chart_background': '#000000'
    # 'text': '#7FDBFF',
    # 'table_cell': '#111111',
    # 'table_text': '#bebebe',
    # 'option_card_bg': '#222222',
    # 'option_card_txt': '#77BBFF',
    # 'topic_text': '#FFFFFF',
    ###############################################
    'background': '#252525',  # Modo pseudo-escuro
    'chart_background': '#333333',
    'text': '#FFFFFF',
    'table_cell': '#333333',
    'table_text': '#FFFFFF',
    'option_card_bg': '#222222',
    'option_card_txt': '#FFFFFF',
    'topic_text': '#FFFFFF',
    ###############################################
    # 'background': '#FFFFFF',  # Modo claro
    # 'chart_background': '#FFFFFF'
    # 'text': '#101010',
    # 'table_cell': '#EFEFEF',
    # 'table_text': '#111111',
    # 'option_card_bg': '#DDDDDD',
    # 'option_card_txt': '#010101',
    # 'topic_text': '#000000'
}
# Para alternar entre os tipos de modo claro/escuro torne em comentário e descomente as partes relevantes
# Não se esqueça de também de alterar o template dos gráficos próximo aos imports
# Você também deve alterar o stylesheet perto do app.layout e a logo

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


dfDadosDistritos = obterDistritos.distritos('data/geo_data/SIRGAS_SHP_distrito',
                                            dfDadosIdebIniciais,
                                            dfDadosIdebFinais)
dfDadoSubprefeituras = obterSubprefeituras.subprefeituras('data/geo_data/SIRGAS_SHP_subprefeitura',
                                                          dfDadosIdebIniciais,
                                                          dfDadosIdebFinais)

dfTabelaDistrito = dfDadosDistritos.filter(['ds_nome', 'ideb_iniciais', 'ideb_finais', 'media_final'], axis=1)
dfTabelaDistrito = dfTabelaDistrito.rename(
    columns={'ds_nome': 'Nome', 'ideb_iniciais': 'Iniciais', 'ideb_finais': 'Finais', 'media_final': 'Média'},
    inplace=False)
dfTabelaDistrito['Iniciais'] = dfTabelaDistrito['Iniciais'].apply(lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaDistrito['Finais'] = dfTabelaDistrito['Finais'].apply(lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaDistrito['Média'] = dfTabelaDistrito['Média'].apply(lambda x: round(x, 2) if not pd.isnull(x) else 0)
# dfTabelaDistrito = dfTabelaDistrito.sort_values(by=['Iniciais'])


dfTabelaSubprefeitura = dfDadoSubprefeituras.filter(['sp_nome', 'ideb_iniciais', 'ideb_finais', 'media_final'], axis=1)
dfTabelaSubprefeitura = dfTabelaSubprefeitura.rename(
    columns={'sp_nome': 'Nome', 'ideb_iniciais': 'Iniciais', 'ideb_finais': 'Finais', 'media_final': 'Média'},
    inplace=False)
dfTabelaSubprefeitura['Iniciais'] = dfTabelaSubprefeitura['Iniciais'].apply(
    lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaSubprefeitura['Finais'] = dfTabelaSubprefeitura['Finais'].apply(
    lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaSubprefeitura['Média'] = dfTabelaSubprefeitura['Média'].apply(
    lambda x: round(x, 2) if not pd.isnull(x) else 0)

dfTabelaGastos_PerCapita = dfDadosDistritos[['ds_nome', 'EDU_PER_CAPITA_anual_2020']]
dfTabelaGastos_PerCapita = dfTabelaGastos_PerCapita.copy()
dfTabelaGastos_PerCapita['EDU_PER_CAPITA_anual_2020'] = dfTabelaGastos_PerCapita['EDU_PER_CAPITA_anual_2020'].apply(
    lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaGastos_PerCapita = dfTabelaGastos_PerCapita.rename(columns=
                                                           {'ds_nome': 'Nome', 'EDU_PER_CAPITA_anual_2020': 'Gastos'},
                                                           inplace=False)

dfTabelaGastos_Absoluto = dfDadosDistritos[['ds_nome', 'EDU_VALOR_TOTAL_ANUAL_2020']]
dfTabelaGastos_Absoluto = dfTabelaGastos_Absoluto.copy()
dfTabelaGastos_Absoluto['EDU_VALOR_TOTAL_ANUAL_2020'] = dfTabelaGastos_Absoluto['EDU_VALOR_TOTAL_ANUAL_2020'].apply(
    lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaGastos_Absoluto = dfTabelaGastos_Absoluto.rename(columns=
                                                         {'ds_nome': 'Nome', 'EDU_VALOR_TOTAL_ANUAL_2020': 'Gastos'},
                                                         inplace=False)

dfTabelaGastos_UBS = dfDadosDistritos[['ds_nome', 'ORC_REMUNERACAO_BRUTA_UBS_2020']]
dfTabelaGastos_UBS = dfTabelaGastos_UBS.copy()
dfTabelaGastos_UBS['ORC_REMUNERACAO_BRUTA_UBS_2020'] = dfTabelaGastos_UBS['ORC_REMUNERACAO_BRUTA_UBS_2020'].apply(
    lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaGastos_UBS = dfTabelaGastos_UBS.rename(columns={'ds_nome': 'Nome', 'ORC_REMUNERACAO_BRUTA_UBS_2020': 'Gastos'},
                                               inplace=False)

dfTabelaGastos_UBS2 = dfDadosDistritos[['ds_nome', 'ORC_GASTO_UBS_2020']]
dfTabelaGastos_UBS2 = dfTabelaGastos_UBS2.copy()
dfTabelaGastos_UBS2 = dfTabelaGastos_UBS2.sort_values('ds_nome')
dfTabelaGastos_UBS2['ORC_GASTO_UBS_2020'] = dfTabelaGastos_UBS2['ORC_GASTO_UBS_2020'].apply(
    lambda x: round(x, 2) if not pd.isnull(x) else 0)
dfTabelaGastos_UBS2 = dfTabelaGastos_UBS2.rename(columns={'ds_nome': 'Nome', 'ORC_GASTO_UBS_2020': 'Gastos'},
                                                 inplace=False)

dfTabelaGastos_UBS2_Unid = pd.read_csv('data/gasto_indireto_por_unid_2020.csv',
                                       sep=";",
                                       decimal=".")
dfTabelaGastos_UBS2_Unid['Gasto'] = dfTabelaGastos_UBS2_Unid['Gasto'].replace('.', ',')

dfTabelaEquipeMinima_Unid = pd.read_csv('data/equipe_minima_agrup_por_unidade_2020.csv',
                                        sep=";",
                                        decimal=".")
dfTabelaEquipeMinima_Unid = dfTabelaEquipeMinima_Unid[['DISTRITOS', 'DESCRICAO_UNIDADE', 'CONTRATADA_UNID',
                                                       'APONTADA_UNID', 'PORCENTAGEM_UNIDADE_CENT']]
dfTabelaEquipeMinima_Unid = dfTabelaEquipeMinima_Unid.rename(columns={'DISTRITOS': 'Distrito',
                                                                      'DESCRICAO_UNIDADE': 'Unidade',
                                                                      'CONTRATADA_UNID': 'Horas contratadas',
                                                                      'APONTADA_UNID': 'Horas apontadas',
                                                                      'PORCENTAGEM_UNIDADE_CENT': 'Taxa cumprida'},
                                                             inplace=False)

dfTabelaEquipeMinima_Dist = pd.read_csv('data/equipe_minima_agrup_por_distrito_2020.csv',
                                        sep=";",
                                        decimal=".")
dfTabelaEquipeMinima_Dist = dfTabelaEquipeMinima_Dist[['DISTRITOS', 'CONTRATADA_DIST',
                                                       'APONTADA_DIST', 'PORCENTAGEM_DIST']]
dfTabelaEquipeMinima_Dist = dfTabelaEquipeMinima_Dist.rename(columns={'DISTRITOS': 'Distrito',
                                                                      'CONTRATADA_DIST': 'Horas contratadas',
                                                                      'APONTADA_DIST': 'Horas apontadas',
                                                                      'PORCENTAGEM_DIST': 'Taxa cumprida'},
                                                             inplace=False)

# dfTabelaGastos_2019 = dfDadosDistritos[['ds_nome', 'gastos_2019']]
# dfTabelaGastos_2019 = dfTabelaGastos_2019.copy()
# dfTabelaGastos_2019['gastos_2019'] = dfTabelaGastos_2019['gastos_2019'].apply(
#     lambda x: round(x, 2) if not pd.isnull(x) else 0)
# dfTabelaGastos_2019 = dfTabelaGastos_2019.rename(columns={'ds_nome': 'Nome', 'gastos_2019': 'Gastos'}, inplace=False)

# dfTabelaGastos_2019['Gastos']=dfTabelaGastos_2019['Gastos'].map('{:,.2f}'.format)

dfEjaConsolidado = pd.read_csv("data/eja_consolidados.csv",
                               sep=";",
                               decimal=",")


info_ideb = '''Os dados acima refletem o ano de 2019 e
                     foram extraídos dos indicadores educacionais do Inep, 
                     disponíveis no portal 'Dados Abertos do Inep.', href = "https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados" <br>
                    Foram extraídos os resultados por escolas da rede municipal de São Paulo
                     e então foi feita a média desses dados por Distrito da cidade de São Paulo.
                      Esses dados estão divididos entre Anos Iniciais e Anos Finais refletindo a forma 
                      como são apresentados no Inep, sendo anos iniciais do 1º ao 4º ano e anos finais do
                       5º ao 9º ano do Ensino fundamental.  Esses dados foram cruzados com os dados das 
                       unidades educacionais da rede Municipal de Ensino de São Paulo disponíveis no 
                    Portal de Dados Abertos da Prefeitura Municipal de São Paulo.", href= "http://dados.prefeitura.sp.gov.br/dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas")
                    A partir desse cruzamento foi feita a média do Ideb por Distrito mostrada na figura. Alguns distritos não apresentam Ideb, pois não possuem escolas de Ensino Fundamental da Rede Municipal de Educação  (os alunos destes distritos frequentam escolas estaduais ou escolas em outros distritos.'''

info_idep = ''' href= "http://dados.prefeitura.sp.gov.br/dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas" Índice de Desenvolvimento da Educação Paulistana (IDEP)
A Secretaria Municipal de Educação (SME) apresenta o Índice de Desenvolvimento da Educação Paulistana (IDEP). Ele foi estruturado com base no princípio de que todos os estudantes têm direito não só à educação, mas à educação de qualidade. O IDEP foi criado para expressar o desempenho das escolas da Rede Municipal de Ensino, considerando os componentes curriculares avaliados na Prova São Paulo e o fluxo escolar.
Para o Ensino Fundamental, o IDEP será calculado considerando os resultados dos 3º, 5º, 7º e 9º anos na Prova São Paulo, avaliação externa municipal de caráter censitário. Para os anos iniciais, serão considerados os resultados dos estudantes dos 3º e 5º anos, em Língua Portuguesa, Matemática e Ciências. O fluxo escolar considerado será do 1º ao 5º ano. Da mesma forma, para os anos finais, serão considerados os resultados dos estudantes dos 7º e 9º anos e o fluxo escolar do 6º ao 9º ano.
Neste conjunto de dados estão disponíveis o IDEP de cada unidade escolar relativo aos anos de 2018 e 2019, precedido pelo Índice de Nível Socioeconômico (NSE aferido em 2013 pelo Inep) e o Indicador de Complexidade de Gestão (ICG)* da escola, seguidos dos resultados esperados como metas para o IDEP em cada um dos 5 anos posteriores (2019 a 2023).
*Índice de Nível Socioeconômico (INSE): sintetiza, de maneira unidimensional, informações sobre a escolaridade dos pais e a renda familiar. O seu objetivo é contextualizar o desempenho das escolas nas avaliações e exames realizados pelo INEP/MEC, bem como seus esforços na realização do trabalho educativo cotidiano. Busca-se uma caracterização do padrão de vida do público de cada unidade escolar, considerando suas características socioeconômicas.
*Indicador de Complexidade de Gestão (ICG): resume em uma única medida as informações de porte, turnos de funcionamento, nível de complexidade das etapas de ensino e quantidade de etapas ofertadas. Ainda que estes fatores não contemplem em totalidade todos os elementos e dimensões envolvidas na gestão escolar, verifica-se que os itens selecionados colaboram para a construção de um índice que potencialmente auxilia na contextualização de resultados das avaliações. A base desse indicador é o ano de 2018.
Para mais informações sobre o Índice de Desenvolvimento da Educação Paulistana (IDEP) consulte a Nota Técnica que acompanha este Conjunto de Dados (disponível para download em:  http://dados.prefeitura.sp.gov.br/dataset/idep ).
Obs: Os dados com * indicam que a escola não atendeu a um dos critérios necessários para o cálculo do Idep ou das suas metas."'''

info_ideb = html.Div(id="divInfo", children=[
    dbc.Button(
        "Informações sobre o indicador", id="open-body-scroll", color="info", n_clicks=0
    ),
    dbc.Modal(
        [
            dbc.ModalHeader(id="info_header"),
            dbc.ModalBody(id="info_body"),
            dbc.ModalFooter(
                dbc.Button(
                    "Fechar",
                    id="close-body-scroll",
                    className="ml-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="modal-body-scroll",
        scrollable=True,
        is_open=False,
    ),
    ]
)


divdistritossubpreituras = dbc.Collapse(
    dbc.Card(style={'backgroundColor': colors['option_card_bg'], 'color': colors['option_card_txt']}, children=[
        dbc.CardBody([
            html.H6("Dados", className="card-title"),

            dbc.Row([
                dbc.Col([

                    dcc.RadioItems(id="optdados",
                                   options=[
                                       {'label': 'Distritos', 'value': 'distrito'},
                                       {'label': 'Subprefeituras', 'value': 'subprefeitura'},
                                   ],
                                   value='distrito',
                                   labelStyle={'display': 'inline-block', "margin-right": "20px"}
                                   ),
                ]),

                # info_ideb

            ])

        ])

    ], color="dark", outline=True), id="colapseddivistritossubpreituras", is_open=False)


divTitulo = dbc.Collapse(
    dbc.Card(style={'backgroundColor': colors['option_card_bg'], 'color': colors['option_card_txt']}, children=[
        dbc.CardBody([
            html.H6("Anos", className="card-title"),
        ])
    ], color="dark", outline=True), id="collapseTituloDireita", is_open=False)


divdanos = dbc.Collapse(
    dbc.Card(style={'backgroundColor': colors['option_card_bg'], 'color': colors['option_card_txt']}, children=[
        dbc.CardBody([
            html.H6("Anos", className="card-title"),
            dcc.RadioItems(id="optanos",
                           options=[
                               {'label': 'Iniciais', 'value': 'ideb_iniciais'},
                               {'label': 'Finais', 'value': 'ideb_finais'},
                               {'label': 'Todos', 'value': 'todos'},
                           ],
                           value='ideb_iniciais',
                           labelStyle={'display': 'inline-block', "margin-right": "20px"}
                           ),
        ])
    ], color="dark", outline=True), id="collapsedivdanos", is_open=False)

divAnosUnersalizacao = dbc.Collapse(
    dbc.Card(style={'backgroundColor': colors['option_card_bg'], 'color': colors['option_card_txt']}, children=[
        dbc.CardBody([
            html.H6("Anos", className="card-title"),

            dbc.Row([
                dbc.Col([

                    dcc.RadioItems(id="optuniversalizacao",
                                   options=[
                                       {'label': '2019', 'value': 2019},
                                       {'label': '2020', 'value': 2020},
                                   ],
                                   value=2019,
                                   labelStyle={'display': 'inline-block', "margin-right": "20px"}
                                   ),
                ]),

            ]),

            # dbc.Row([
            #     dbc.Col([
            #
            #         dcc.RadioItems(id="optidep",
            #                        options=[
            #                            {'label': 'Iniciais', 'value': 'iniciais'},
            #                            {'label': 'Finais', 'value': 'finais'},
            #                        ],
            #                        value='iniciais',
            #                        labelStyle={'display': 'inline-block', "margin-right": "20px"}
            #                        ),
            #     ]),
            #
            # ])

        ])

    ], color="dark", outline=True), id="colapseddivuniversalizacao", is_open=False)


def gerar_geodf(anos_ideb):
    """Gera o GeoDataFrame de anos_ideb de acordo com os anos escolhidos e
    retorna um GeoDataFrame.

    Variable type: String
    Options: 'todos' ou 'iniciais'"""

    if anos_ideb == "todos":
        pass

        # geodf = regionalizar(anos_ideb)
        # geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
        # geodf['text'] = geodf['ds_nome'] + ':<br>Nota média:' \
        #     + geodf['ideb_2019'].apply(lambda x: str(round(x,2)) if not pd.isnull(x) else 'Não se aplica')

        # geodfi = gerar_geodf("iniciais")
        # geodff = gerar_geodf("finais")
        # geodf = pd.merge(geodfi, geodff[["ds_codigo", "ideb_2019"]], on="ds_codigo", how="left")
        # total = geodf["ideb_2019_x"] + geodf["ideb_2019_y"]
        # geodf["total"] = total
    else:
        if anos_ideb == "inicias":
            geodf = dfDadosDistritos
            geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
            geodf['text'] = geodf['ds_nome'] + ':<br>Nota média:' \
                + geodf['ideb_iniciais'].apply(
                lambda x: str(round(x, 2)) if not pd.isnull(x) or x != 0 else 'Não se aplica')

    return geodf


def gerar_mapa(tipografico, anos_ideb, tipodados, anos_universalizacao=0):
    """Gera o mapa Choropleth de acordo com os parâmetros passados e
    retorna uma fig.

    Variable type:{tipografico: String;
                        tipodados: String;
                        anos_universalizacao: int}

    Options:{tipografico: 'ideb', 'univerzalizacao', 'gastos1', 'gastos2', ou "equipe"
                tipodados: 'distritos' ou 'subprefeituras'
                anos_universalizacao: 2019}"""

    fig = go.Figure()

    if tipografico == "ideb":

        if tipodados == "distrito":
            geodf = dfDadosDistritos
            geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
            geodf['text'] = geodf['ds_nome'] + ':<br>Nota média:' \
                + geodf[anos_ideb].apply(lambda x: str(round(x, 2)) if not x == 0 else 'Não se aplica')

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
            fig.update_geos(fitbounds="locations", visible=False, showframe=True, framewidth=0,
                            bgcolor=colors['chart_background'], scope="south america")
            # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=True)
            fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0},
                              showlegend=False,
                              height=513,
                              title="Distribuição IDEB por Distritos",
                              mapbox_style="open-street-map",
                              plot_bgcolor=colors['chart_background'],
                              paper_bgcolor=colors['chart_background']
                              )

        else:
            if tipodados == "subprefeitura":
                geodf = dfDadoSubprefeituras
                geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                geodf['text'] = geodf['sp_nome'] + ':<br>Nota média:' \
                    + geodf[anos_ideb].apply(lambda x: str(round(x, 2)) if not x == 0 else 'Não se aplica')

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
                fig.update_geos(fitbounds="locations", visible=False,
                                bgcolor=colors['chart_background'], scope="south america")
                fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0},
                                  showlegend=False,
                                  height=513,
                                  title="Distribuição IDEB por Subprefeituras",
                                  plot_bgcolor=colors['chart_background'],
                                  paper_bgcolor=colors['chart_background']
                                  )

    else:
        if tipografico == "universalizacao":
            if anos_universalizacao == 2019:

                geodf = dfDadosDistritos
                geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                geodf['text'] = geodf['ds_nome'] + ':<br>Taxa(%):' \
                    + geodf['universalizacao_2019'].apply(lambda x: str(round(x, 2)) if not x == 0 else 'Não se aplica')

                min_universalizacao_2019 = geodf['universalizacao_2019'].min()
                fig = go.Figure(data=go.Choropleth(
                    geojson=json.loads(geodf.geometry.to_json()),
                    locations=geodf.index,
                    z=geodf['universalizacao_2019'],
                    colorscale='Reds',
                    autocolorscale=False,
                    text=geodf['text'],  # hover text
                    hoverinfo='text',
                    colorbar_title="Universalização",
                    zmin=min_universalizacao_2019,
                    zmax=geodf['universalizacao_2019'].max(),
                ))
                fig.update_geos(fitbounds="locations", visible=False,
                                bgcolor=colors['chart_background'], scope="south america")
                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                  showlegend=False,
                                  height=513,
                                  title="Universalização da Educação Infantil (2019)",
                                  plot_bgcolor=colors['chart_background'],
                                  paper_bgcolor=colors['chart_background']
                                  )
            else:

                geodf = dfDadosDistritos
                geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                geodf['text'] = geodf['ds_nome'] + ':<br>Taxa(%):' \
                    + geodf['universalizacao_2020'].apply(
                    lambda x: str(round(x, 2)) if not pd.isnull(x) or x != 0 else 'Não se aplica')

                min_universalizacao_2020 = geodf['universalizacao_2020'].min()
                fig = go.Figure(data=go.Choropleth(
                    geojson=json.loads(geodf.geometry.to_json()),
                    locations=geodf.index,
                    z=geodf['universalizacao_2020'],
                    colorscale='Reds',
                    autocolorscale=False,
                    text=geodf['text'],  # hover text
                    hoverinfo='text',
                    colorbar_title="Universalização",
                    zmin=min_universalizacao_2020,
                    zmax=geodf['universalizacao_2020'].max(),
                ))
                fig.update_geos(fitbounds="locations", visible=False,
                                bgcolor=colors['chart_background'], scope="south america")
                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                  showlegend=False,
                                  height=513,
                                  title="Universalização da Educação Infantil (2020)",
                                  plot_bgcolor=colors['chart_background'],
                                  paper_bgcolor=colors['chart_background']
                                  )

        else:
            if tipografico == "gastos1":
                geodf = dfDadosDistritos
                geodf['EDU_PER_CAPITA_anual_2020'] = geodf['EDU_PER_CAPITA_anual_2020'].apply(
                    lambda x: round(x, 2) if not pd.isnull(x) else 0)

                geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                geodf['text'] = geodf['ds_nome'] + ':<br>Gasto: ' \
                    + geodf['EDU_PER_CAPITA_anual_2020'].apply(
                    lambda x: '{:,.2f}'.format(
                        float(str(round(x, 2)))) if not pd.isna(x) or x != 0 else 'Não se aplica')

                geodf['text'] = geodf["text"].str.replace('.', '*')

                geodf['text'] = geodf["text"].str.replace(',', '.')

                geodf['text'] = geodf["text"].str.replace('*', ',')

                min_percapita = geodf['EDU_PER_CAPITA_anual_2020'].min()
                fig = go.Figure(data=go.Choropleth(
                    geojson=json.loads(geodf.geometry.to_json()),
                    locations=geodf.index,
                    z=geodf['EDU_PER_CAPITA_anual_2020'],
                    colorscale='Reds',
                    autocolorscale=False,
                    text=geodf['text'],  # hover text
                    hoverinfo='text',
                    colorbar_title="Gastos Per Capita 2020",
                    zmin=min_percapita,
                    zmax=geodf['EDU_PER_CAPITA_anual_2020'].max(),
                ))
                fig.update_geos(fitbounds="locations", visible=False,
                                bgcolor=colors['chart_background'], scope="south america")
                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                  showlegend=False,
                                  height=513,
                                  title="Gastos por Distrito Per Capita (2020)",
                                  plot_bgcolor=colors['chart_background'],
                                  paper_bgcolor=colors['chart_background']
                                  )

            else:
                if tipografico == "gastos2":
                    geodf = dfDadosDistritos
                    geodf['EDU_VALOR_TOTAL_ANUAL_2020'] = geodf['EDU_VALOR_TOTAL_ANUAL_2020'].apply(
                        lambda x: round(x, 2) if not pd.isnull(x) else 0)

                    geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                    geodf['text'] = geodf['ds_nome'] + ':<br>Gasto: ' \
                                    + geodf['EDU_VALOR_TOTAL_ANUAL_2020'].apply(
                        lambda x: '{:,.2f}'.format(
                            float(str(round(x, 2)))) if not pd.isna(x) or x != 0 else 'Não se aplica')

                    geodf['text'] = geodf["text"].str.replace('.', '*')

                    geodf['text'] = geodf["text"].str.replace(',', '.')

                    geodf['text'] = geodf["text"].str.replace('*', ',')

                    min_gastoAbsol = geodf['EDU_VALOR_TOTAL_ANUAL_2020'].min()
                    fig = go.Figure(data=go.Choropleth(
                        geojson=json.loads(geodf.geometry.to_json()),
                        locations=geodf.index,
                        z=geodf['EDU_VALOR_TOTAL_ANUAL_2020'],
                        colorscale='Reds',
                        autocolorscale=False,
                        text=geodf['text'],  # hover text
                        hoverinfo='text',
                        colorbar_title="Gasto Absoluto 2020",
                        zmin=min_gastoAbsol,
                        zmax=geodf['EDU_VALOR_TOTAL_ANUAL_2020'].max(),
                    ))
                    fig.update_geos(fitbounds="locations", visible=False,
                                    bgcolor=colors['chart_background'], scope="south america")
                    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                      showlegend=False,
                                      height=513,
                                      title="Gastos Absoluto por Distrito (2020)",
                                      plot_bgcolor=colors['chart_background'],
                                      paper_bgcolor=colors['chart_background']
                                      )

                else:
                    if tipografico == "ubs":
                        geodf = dfDadosDistritos
                        geodf['ORC_REMUNERACAO_BRUTA_UBS_2020'] = geodf['ORC_REMUNERACAO_BRUTA_UBS_2020'].apply(
                            lambda x: round(x, 2) if not pd.isnull(x) else 0)

                        geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                        geodf['text'] = geodf['ds_nome'] + ':<br>Gasto: ' \
                                        + geodf['ORC_REMUNERACAO_BRUTA_UBS_2020'].apply(
                            lambda x: '{:,.2f}'.format(
                                float(str(round(x, 2)))) if not pd.isna(x) or x != 0 else 'Não se aplica')

                        geodf['text'] = geodf["text"].str.replace('.', '*')

                        geodf['text'] = geodf["text"].str.replace(',', '.')

                        geodf['text'] = geodf["text"].str.replace('*', ',')

                        min_gastoUBS = geodf['ORC_REMUNERACAO_BRUTA_UBS_2020'].min()
                        fig = go.Figure(data=go.Choropleth(
                            geojson=json.loads(geodf.geometry.to_json()),
                            locations=geodf.index,
                            z=geodf['ORC_REMUNERACAO_BRUTA_UBS_2020'],
                            colorscale='Reds',
                            autocolorscale=False,
                            text=geodf['text'],  # hover text
                            hoverinfo='text',
                            colorbar_title="Gastos",
                            zmin=min_gastoUBS,
                            zmax=geodf['ORC_REMUNERACAO_BRUTA_UBS_2020'].max(),
                        ))
                        fig.update_geos(fitbounds="locations", visible=False,
                                        bgcolor=colors['chart_background'], scope="south america")
                        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                          showlegend=False,
                                          height=513,
                                          title="Gasto com Pessoal na Administração Direta por UBS de 2020",
                                          plot_bgcolor=colors['chart_background'],
                                          paper_bgcolor=colors['chart_background']
                                          )

                    else:
                        if tipografico == "equipe":
                            geodf = dfDadosDistritos
                            geodf['SAU_PORCENTAGEM_HORAS_CUMPRIDAS_DIST_2020'] = geodf['SAU_PORCENTAGEM_HORAS_CUMPRIDAS_DIST_2020'].apply(
                                lambda x: round(x, 4) if not pd.isnull(x) else 0)

                            geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                            geodf['text'] = geodf['ds_nome'] + ':<br>Porcentagem cumprida: ' \
                                            + (geodf['SAU_PORCENTAGEM_HORAS_CUMPRIDAS_DIST_2020']*100).apply(
                                lambda x: '{:,.2f}'.format(
                                    float(str(round(x, 2)))) if not pd.isna(x) or x != 0 else 'Não se aplica') + "%"

                            geodf['text'] = geodf["text"].str.replace('.', '*')

                            geodf['text'] = geodf["text"].str.replace(',', '.')

                            geodf['text'] = geodf["text"].str.replace('*', ',')

                            min_horasCumpridas = geodf['SAU_PORCENTAGEM_HORAS_CUMPRIDAS_DIST_2020'].min()
                            fig = go.Figure(data=go.Choropleth(
                                geojson=json.loads(geodf.geometry.to_json()),
                                locations=geodf.index,
                                z=geodf['SAU_PORCENTAGEM_HORAS_CUMPRIDAS_DIST_2020'],
                                colorscale='Reds',
                                autocolorscale=False,
                                text=geodf['text'],  # hover text
                                hoverinfo='text',
                                colorbar_title="Horas Cumpridas",
                                zmin=min_horasCumpridas,
                                zmax=geodf['SAU_PORCENTAGEM_HORAS_CUMPRIDAS_DIST_2020'].max(),
                            ))
                            fig.update_geos(fitbounds="locations", visible=False,
                                            bgcolor=colors['chart_background'], scope="south america")
                            fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                              showlegend=False,
                                              height=513,
                                              title="Equipe Miníma Contratada 2020",
                                              plot_bgcolor=colors['chart_background'],
                                              paper_bgcolor=colors['chart_background']
                                              )

                        else:
                            if tipografico == "gastoubs":
                                geodf = dfDadosDistritos
                                geodf['ORC_GASTO_UBS_2020'] = geodf['ORC_GASTO_UBS_2020'].apply(
                                    lambda x: round(x, 2) if not pd.isnull(x) else 0)

                                geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                                geodf['text'] = geodf['ds_nome'] + ':<br>Gasto: ' \
                                                + geodf['ORC_GASTO_UBS_2020'].apply(
                                    lambda x: '{:,.2f}'.format(
                                        float(str(round(x, 2)))) if not pd.isna(x) or x != 0 else 'Não se aplica')

                                geodf['text'] = geodf["text"].str.replace('.', '*')

                                geodf['text'] = geodf["text"].str.replace(',', '.')

                                geodf['text'] = geodf["text"].str.replace('*', ',')

                                min_gastoUBS = geodf['ORC_GASTO_UBS_2020'].min()
                                fig = go.Figure(data=go.Choropleth(
                                    geojson=json.loads(geodf.geometry.to_json()),
                                    locations=geodf.index,
                                    z=geodf['ORC_GASTO_UBS_2020'],
                                    colorscale='Reds',
                                    autocolorscale=False,
                                    text=geodf['text'],  # hover text
                                    hoverinfo='text',
                                    colorbar_title="Gastos",
                                    zmin=min_gastoUBS,
                                    zmax=geodf['ORC_GASTO_UBS_2020'].max(),
                                ))
                                fig.update_geos(fitbounds="locations", visible=False,
                                                bgcolor=colors['chart_background'], scope="south america")
                                fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                                  showlegend=False,
                                                  height=513,
                                                  title="Gasto com Pessoal na Administração Indireta por UBS de 2020",
                                                  plot_bgcolor=colors['chart_background'],
                                                  paper_bgcolor=colors['chart_background']
                                                  )

        #################################################

    return fig


external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
# Para modo claro mude dbc.themes.* para BOOTSTRAP, modo escuro DARKLY ou SLATE e modo extra escuro mude para CYBORG


server = app.server

app.title = 'Observatório de Políticas Públicas - TCMSP'


loading_style = {'position': 'absolute', 'align-self': 'center'}

app.layout = dbc.Container(style={'backgroundColor': colors['background']}, children=[
    dbc.Row([
        dbc.Col([
            dbc.CardHeader(style={'backgroundColor': colors['background']}),
            dbc.Card(style={'backgroundColor': colors['background']}, children=[
                dbc.CardBody([
                    html.H5(children="Observatório de Políticas Publicas - TCMSP",
                            style={'color': colors['text']}
                            ),

                    dbc.Row(style={'backgroundColor': colors['background']}, children=[

                        dbc.Col([
                            dbc.Button("Educação",
                                       id='btn-educacao',
                                       color="secondary",
                                       n_clicks=0),
                            dbc.Button("Saúde",
                                       id='btn-saude',
                                       color="secondary",
                                       n_clicks=0,
                                       style={"margin-left": "5px"}),
                            dbc.Button("Urbanismo",
                                       id='btn-urbanismo',
                                       color="secondary",
                                       n_clicks=0,
                                       style={"margin-left": "5px"}),
                            dbc.Button("Orçamento",
                                       id='btn-orcamento',
                                       color="secondary",
                                       n_clicks=0,
                                       style={"margin-left": "5px"}),
                        ]),
                        #
                        # dbc.Col([
                        #     dbc.Button("Educação", id='btn-educacao', color="secondary", n_clicks=0, block=True, )
                        # ], width=3),
                        # dbc.Col([
                        #    dbc.Button("Urbanismo", id='btn-urbanismo', color="secondary", n_clicks=0, block=True),
                        # ], width=3),
                        # dbc.Col([
                        #    dbc.Button("Orçamento", id='btn-orcamento', color="secondary", n_clicks=0, block=True),
                        # ], width=3),
                        # dbc.Col([
                        #     dbc.Button("Saúde", id='btn-saude', color="secondary", n_clicks=0, block=True),
                        # ], width=3),

                        # html.Div([
                        #     html.Button('Educação',
                        #                 id='btn-educacao',
                        #                 style={'background-color': '#0099cc',
                        #                        'color': 'white',
                        #                        'width': '100px',
                        #                        "margin-left": "0px",
                        #                        'height': '40px'},
                        #                n_clicks=0),
                        #     html.Button('Saúde',
                        #                  id='btn-saude',
                        #                  style={'background-color': '#0099cc',
                        #                         'color': 'white',
                        #                         'width': '100px',
                        #                         "margin-left": "10px",
                        #                         'height': '40px'},
                        #                  n_clicks=0),
                        #     html.Button('Urbanismo',
                        #                 id='btn-urbanismo',
                        #                style={'background-color':
                        #                      '#0099cc', 'color':
                        #                     'white', 'width':
                        #                      '100px',
                        #                     "margin-left": "10px",
                        #                     'height': '40px'},
                        #               n_clicks=0),
                        #     html.Button('Orçamento',
                        #               id='btn-orcamento',
                        #               style={'background-color': '#0099cc',
                        #                      'color': 'white',
                        #                      'width': '100px',
                        #                       "margin-left": "10px",
                        #                        'height': '40px'},
                        #                 n_clicks=0),
                        #     html.P(""),
                        #     html.Div(id='drpindicadores')
                        #         ]),
                    ]),

                    html.P(""),
                    dbc.Row([
                        dbc.Col(style={'backgroundColor': colors['background']}, children=[
                            info_ideb
                        ], md=9)]),
                    html.P(""),
                    dbc.Row([
                        dbc.Col([
                            dbc.Collapse(
                                dcc.Dropdown(
                                    id='dpEducacao',
                                    options=[{'label': 'Ideb (2019)', 'value': 'ideb'},
                                             {'label': 'Idep (2019)', 'value': 'idep'},
                                             {'label': 'EJA (2006-2020)', 'value': 'eja'},
                                             {'label': 'Gastos Per Capita (2020)', 'value': 'gastos1'},
                                             {'label': 'Gasto Absoluto (2020)', 'value': 'gastos2'},
                                             {'label': 'Taxa de Abandono (2012-2020)', 'value': 'abandono'},
                                             {'label': 'Universalização (2010-2020)', 'value': 'universalizacao'}],
                                    placeholder='Escolha um indicador',
                                    style={'backgroundColor': colors['background']}),
                                id="colEducacao", is_open=False),

                            dbc.Collapse(
                                dcc.Dropdown(
                                    id='dpSaude',
                                    options=[{'label': 'Equipe Mínima Contratada (2020)', 'value': 'equipe'},
                                             ],
                                    placeholder='Escolha um indicador',
                                    style={'backgroundColor': colors['background']}),
                                id="colSaude", is_open=False),

                            dbc.Collapse(
                                dcc.Dropdown(
                                    id='dpUrbanismo',
                                    options=[{'label': 'Em desenvolvimento', 'value': 'urbanismo1'},
                                             ],
                                    placeholder='Escolha um indicador',
                                    style={'backgroundColor': colors['background']}),
                                id="colUrbanismo", is_open=False),

                            dbc.Collapse(
                                dcc.Dropdown(
                                    id='dpOrcamento',
                                    options=[{'label': 'Gasto com Pessoal na Administração Direta por UBS (2020)', 'value': 'ubs'},
                                             {'label': 'Gasto com Pessoal na Administração Indireta (OSS) por UBS (2020)', 'value': 'gastoubs'}
                                             ],
                                    placeholder='Escolha um indicador',
                                    style={'backgroundColor': colors['background']}),
                                id="colOrcamento", is_open=False),

                        ], md=9),

                    ]),
                    # html.Div(id='drpindicadores')

                ])
            ], color="dark", outline=True),

            # Este cartão tem três Divs. Cada uma contendo um gráfico. Todas posicionadas à esquerda
            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                    dbc.CardBody(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                        # html.Div([
                        #     html.Span(id="titulocardlinha"),
                        # ]),
                        html.Div(id="divGrafEsquerdaSup", children=[
                            dcc.Loading(id="Loading-2", type="default",
                                        children=[dcc.Graph(id="GrafEsquerdaSup"),
                                                  ])
                        ]),
                        html.Div(id="divGrafEsquerdaInf", children=[

                            dcc.Loading(id="Loading-3", type="default",
                                        children=[dcc.Graph(id="GrafEsquerdaInf"), ])
                        ]),

                        html.Div(id="divGrafEsquerdaInf2", children=[

                            dcc.Loading(id="Loading-4", type="default",
                                        children=[dcc.Graph(id="GrafEsquerdaInf2"), ])
                        ]),

                    ])
                ], color="dark", outline=True),
                id="collapseGraficosEsquerda", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("IDEB - Distritos", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divTabelaDistrito",
                                 children=[
                                     dash_table.DataTable(id="tabela",
                                                          data=dfTabelaDistrito.to_dict('records'),
                                                          sort_action='native',
                                                          style_table={'height': '350px',
                                                                       'overflowY': 'auto'},
                                                          style_header={'fontSize': 13,
                                                                        'font-family': 'arial',
                                                                        'fontWeight': 'bold'},
                                                          style_cell={'backgroundColor': colors['table_cell'],
                                                                      'color': colors['table_text'],
                                                                      'textAlign': 'left',
                                                                      'width': '85px',
                                                                      'whiteSpace': 'normal',
                                                                      'fontSize': 13,
                                                                      'font-family': 'arial'},
                                                          columns=[
                                                              {'id': c, 'name': c} for c in dfTabelaDistrito.columns])

                                 ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaDistrito", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("Gasto por Distrito", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divTabelaGastosPerCapita", children=[
                                dash_table.DataTable(id="tabelagastosPerCapita",
                                                     data=dfTabelaGastos_PerCapita.to_dict('records'),
                                                     sort_action='native',
                                                     style_table={'height': '350px', 'overflowY': 'auto'},
                                                     style_header={'fontSize': 13, 'font-family': 'arial',
                                                                   'fontWeight': 'bold'},
                                                     style_cell={'backgroundColor': colors['table_cell'],
                                                                 'color': colors['table_text'],
                                                                 'textAlign': 'left',
                                                                 'width': '85px',
                                                                 'whiteSpace': 'normal', 'fontSize': 13,
                                                                 'font-family': 'arial'},
                                                     columns=[
                                                         {'id': c, 'name': c, 'type': 'numeric', 'format': Format(
                                                             scheme=Scheme.fixed,
                                                             precision=2,
                                                             group=Group.yes,
                                                             groups=3,
                                                             group_delimiter=".",
                                                             decimal_delimiter=",",
                                                         )}
                                                         for c in dfTabelaGastos_PerCapita.columns])

                            ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaGastosPerCapita", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("Gasto por Distrito", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divTabelaGastosAbsoluto", children=[
                                dash_table.DataTable(id="tabelagastosAbsoluto",
                                                     data=dfTabelaGastos_Absoluto.to_dict('records'),
                                                     sort_action='native',
                                                     style_table={'height': '350px', 'overflowY': 'auto'},
                                                     style_header={'fontSize': 13, 'font-family': 'arial',
                                                                   'fontWeight': 'bold'},
                                                     style_cell={'backgroundColor': colors['table_cell'],
                                                                 'color': colors['table_text'],
                                                                 'textAlign': 'left',
                                                                 'width': '85px',
                                                                 'whiteSpace': 'normal', 'fontSize': 13,
                                                                 'font-family': 'arial'},
                                                     columns=[
                                                         {'id': c, 'name': c, 'type': 'numeric', 'format': Format(
                                                             scheme=Scheme.fixed,
                                                             precision=2,
                                                             group=Group.yes,
                                                             groups=3,
                                                             group_delimiter=".",
                                                             decimal_delimiter=",",
                                                         )}
                                                         for c in dfTabelaGastos_Absoluto.columns])

                            ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaGastosAbsoluto", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("Equipe Miníma por Distrito", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divTabelaEquipeMinimaDist", children=[
                                dash_table.DataTable(id="tabelaEquipeMinimaDist",
                                                     data=dfTabelaEquipeMinima_Dist.to_dict('records'),
                                                     sort_action='native',
                                                     style_table={'height': '350px', 'overflowY': 'auto'},
                                                     style_header={'fontSize': 13, 'font-family': 'arial',
                                                                   'fontWeight': 'bold'},
                                                     style_cell={'backgroundColor': colors['table_cell'],
                                                                 'color': colors['table_text'],
                                                                 'textAlign': 'left',
                                                                 'width': '85px',
                                                                 'whiteSpace': 'normal', 'fontSize': 13,
                                                                 'font-family': 'arial'},
                                                     columns=[
                                                         {'id': c, 'name': c, 'type': 'numeric', 'format': Format(
                                                             scheme=Scheme.fixed,
                                                             precision=0,
                                                             group=Group.yes,
                                                             groups=3,
                                                             group_delimiter=".",
                                                             decimal_delimiter=",",
                                                         )}
                                                         for c in dfTabelaEquipeMinima_Dist.columns]
                                                     )

                            ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaEquipeMinimaDist", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("Equipe Miníma por Unidade", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divTabelaEquipeMinimaUnid", children=[
                                dash_table.DataTable(id="tabelaEquipeMinimaUnid",
                                                     data=dfTabelaEquipeMinima_Unid.to_dict('records'),
                                                     sort_action='native',
                                                     style_table={'height': '350px', 'overflowY': 'auto'},
                                                     style_header={'fontSize': 13, 'font-family': 'arial',
                                                                   'fontWeight': 'bold'},
                                                     style_cell={'backgroundColor': colors['table_cell'],
                                                                 'color': colors['table_text'],
                                                                 'textAlign': 'left',
                                                                 'width': '85px',
                                                                 'whiteSpace': 'normal', 'fontSize': 13,
                                                                 'font-family': 'arial'},
                                                     columns=[
                                                         {'id': c, 'name': c, 'type': 'numeric', 'format': Format(
                                                             scheme=Scheme.fixed,
                                                             precision=0,
                                                             group=Group.yes,
                                                             groups=3,
                                                             group_delimiter=".",
                                                             decimal_delimiter=",",
                                                         )}
                                                         for c in dfTabelaEquipeMinima_Unid.columns]
                                                     )

                            ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaEquipeMinimaUnid", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("Gasto por Distrito", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divTabelaGastosUBS", children=[
                                dash_table.DataTable(id="tabelagastosUBS",
                                                     data=dfTabelaGastos_UBS.to_dict('records'),
                                                     sort_action='native',
                                                     style_table={'height': '350px', 'overflowY': 'auto'},
                                                     style_header={'fontSize': 13, 'font-family': 'arial',
                                                                   'fontWeight': 'bold'},
                                                     style_cell={'backgroundColor': colors['table_cell'],
                                                                 'color': colors['table_text'],
                                                                 'textAlign': 'left',
                                                                 'width': '85px',
                                                                 'whiteSpace': 'normal', 'fontSize': 13,
                                                                 'font-family': 'arial'},
                                                     columns=[
                                                         {'id': c, 'name': c, 'type': 'numeric', 'format': Format(
                                                             scheme=Scheme.fixed,
                                                             precision=2,
                                                             group=Group.yes,
                                                             groups=3,
                                                             group_delimiter=".",
                                                             decimal_delimiter=",",
                                                         )}
                                                         for c in dfTabelaGastos_UBS.columns])

                            ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaGastosUBS", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("Gasto por Distrito", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divTabelaGastosUBS2", children=[
                                dash_table.DataTable(id="tabelagastosUBS2",
                                                     data=dfTabelaGastos_UBS2.to_dict('records'),
                                                     sort_action='native',
                                                     style_table={'height': '350px', 'overflowY': 'auto'},
                                                     style_header={'fontSize': 13, 'font-family': 'arial',
                                                                   'fontWeight': 'bold'},
                                                     style_cell={'backgroundColor': colors['table_cell'],
                                                                 'color': colors['table_text'],
                                                                 'textAlign': 'left',
                                                                 'width': '85px',
                                                                 'whiteSpace': 'normal', 'fontSize': 13,
                                                                 'font-family': 'arial'},
                                                     columns=[
                                                         {'id': c, 'name': c, 'type': 'numeric', 'format': Format(
                                                             scheme=Scheme.fixed,
                                                             precision=2,
                                                             group=Group.yes,
                                                             groups=3,
                                                             group_delimiter=".",
                                                             decimal_delimiter=",",
                                                         )}
                                                         for c in dfTabelaGastos_UBS2.columns])

                            ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaGastosUBS2", is_open=False),

            dbc.Collapse(
                dbc.Card(style={'margin-top': 20,
                                'backgroundColor': colors['background'],
                                'color': colors['topic_text']},
                         children=[
                             html.H6("Gasto por Unidade", className="card-title"),
                             html.Div(
                                 style={'backgroundColor': colors['background'], 'color': colors['text']},
                                 id="divdfTabelaGastos_UBS2_Unid", children=[
                                     dash_table.DataTable(id="dfTabelaGastos_UBS2_Unid",
                                                          data=dfTabelaGastos_UBS2_Unid.to_dict('records'),
                                                          sort_action='native',
                                                          style_table={'height': '350px',
                                                                       'overflowY': 'auto'},
                                                          style_header={'fontSize': 13,
                                                                        'font-family': 'arial',
                                                                        'fontWeight': 'bold',
                                                                        'width': '250px'},
                                                          style_cell={
                                                              'backgroundColor': colors['table_cell'],
                                                              'color': colors['table_text'],
                                                              'textAlign': 'left', 'minWidth': '50px',
                                                              'whiteSpace': 'normal', 'fontSize': 13,
                                                              'font-family': 'arial'},
                                                          columns=[{'id': c, 'name': c} for c in
                                                                   dfTabelaGastos_UBS2_Unid.columns])

                                 ]),

                         ], color="dark", outline=True),
                id="collapsedfTabelaGastos_UBS2_Unid", is_open=False),

            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['topic_text']}, children=[
                    dbc.CardBody([
                        html.H6("IDEB - Subprefeituras", className="card-title"),
                        html.Div(id="divTabelaSubprefeitura", children=[
                            dash_table.DataTable(id="tabelas",
                                                 data=dfTabelaSubprefeitura.to_dict('records'),
                                                 sort_action='native',
                                                 # page_size=10,
                                                 style_table={'height': '350px',
                                                              'overflowY': 'auto'},
                                                 style_header={'fontSize': 13,
                                                               'font-family': 'arial',
                                                               'fontWeight': 'bold'},
                                                 style_cell={'backgroundColor': colors['table_cell'],
                                                             'color': colors['table_text'],
                                                             'textAlign': 'left',
                                                             'width': '85px',
                                                             'whiteSpace': 'normal',
                                                             'fontSize':13,
                                                             'font-family':'arial'},
                                                 columns=[{'id': c, 'name': c} for c in dfTabelaSubprefeitura.columns])

                        ]),

                    ])
                ], color="dark", outline=True),
                id="collapseTabelaSubprefeitura", is_open=False),

            dbc.CardHeader(style={'backgroundColor': colors['background']})

        ], width=5),
        dbc.Col(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
            dbc.CardHeader(style={'backgroundColor': colors['background']}),
            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                    dbc.CardBody([

                        dbc.Row([
                            dbc.Col([

                                # html.Div(id="distsub"),
                                divdistritossubpreituras,

                            ]),

                            dbc.Col([

                                divdanos,
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([

                                divAnosUnersalizacao,

                            ]),
                        ]),


                        html.Div(id="divGrafDireita",
                                 children=[
                                     dcc.Loading(id="Loading-1", type="default",
                                                 children=[dcc.Graph(id="choropleth"
                                                                     # , style={'height': '100%','width': '100%'}
                                                                     )])
                                 ]),
                        html.Div(id="divSlider", style={'margin-bottom': 20}, children=[
                            dcc.RangeSlider(
                                id='sliderEja',
                                dots=False,
                                min=2006,
                                max=2020,
                                value=[2006, 2020],
                                step=1,
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False
                            )

                        ]),

                        ############################################

                        dbc.Collapse(
                            dbc.Card(style={'margin-top': 20,
                                            'backgroundColor': colors['background'],
                                            'color': colors['topic_text']},
                                     children=[
                                         html.H6("Total de Matrículas por Distrito", className="card-title"),
                                         html.Div(
                                             style={'backgroundColor': colors['background'], 'color': colors['text']},
                                             id="divTabelaEja", children=[
                                                 dash_table.DataTable(id="tabelaEja",
                                                                      data=dfEjaConsolidado.to_dict('records'),
                                                                      sort_action='native',
                                                                      style_table={'height': '350px',
                                                                                   'overflowY': 'auto'},
                                                                      style_header={'fontSize': 13,
                                                                                    'font-family': 'arial',
                                                                                    'fontWeight': 'bold',
                                                                                    'width': '250px'},
                                                                      style_cell={
                                                                          'backgroundColor': colors['table_cell'],
                                                                          'color': colors['table_text'],
                                                                          'textAlign': 'left', 'minWidth': '50px',
                                                                          'whiteSpace': 'normal', 'fontSize': 13,
                                                                          'font-family': 'arial'},
                                                                      columns=[{'id': c, 'name': c} for c in
                                                                               dfEjaConsolidado.columns])

                                             ]),

                                     ], color="dark", outline=True),
                            id="collapseTabelaEja", is_open=False),
                        #############################################


                    ])],
                         color="dark", outline=True),
                id="collapseGraficosDireita", is_open=False),

            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                    dbc.CardImg(src="./assets/logo_observatorio_dark.svg", top=True),
                    dbc.CardBody([
                        html.H3("Observatório de Políticas Públicas", className="card-title"),
                        html.H4("Tribunal de Contas do Município de São Paulo", className="card-title"),
                        html.H5("Escola Superior de Gestão e Contas Públicas", className="card-title"),
                        # dbc.CardLink('IRIS - Informações e Relatórios de Interesse Social',
                        #              href="https://iris.tcm.sp.gov.br/", target="_blank"),
                        # html.P(""),
                        # dbc.CardLink('Portal de Dados Abertos da Cidade de São Paulo',
                        #              href="http://dados.prefeitura.sp.gov.br/",
                        #              target="_blank"),

                    ])
                ], color="dark", outline=True),
                id="colApresentacaoDireita", is_open=True),
            dbc.CardHeader(style={'backgroundColor': colors['background']}),

        ], width=7)
    ], no_gutters=False)
])


#####################################################################
# Botões
#####################################################################
@app.callback(
    Output('colEducacao', 'is_open'),
    Output('colSaude', 'is_open'),
    Output('colUrbanismo', 'is_open'),
    Output('colOrcamento', 'is_open'),
    [Input('btn-educacao', 'n_clicks'),
     Input('btn-saude', 'n_clicks'),
     Input('btn-urbanismo', 'n_clicks'),
     Input('btn-orcamento', 'n_clicks')
     ]
             )
def displayClick(btn1, btn2, btn3, btn4):
    """Torna os botões da aplicação interativos retornando os dropdowns
    que aparecem ao clicar neles.

    Variable type: none"""

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    m_dropdown_educacao = False
    m_dropdown_saude = False
    m_dropdown_urbanismo = False
    m_dropdown_orcamento = False

    if 'btn-educacao' in changed_id:
        m_dropdown_educacao = True
    elif 'btn-saude' in changed_id:
        m_dropdown_saude = True
    elif 'btn-urbanismo' in changed_id:
        m_dropdown_urbanismo = True
    elif 'btn-orcamento' in changed_id:
        m_dropdown_orcamento = True
    else:
        pass

    return m_dropdown_educacao, m_dropdown_saude, m_dropdown_urbanismo, m_dropdown_orcamento


#####################################################################
# Gráficos e Mapas
#####################################################################
@app.callback(Output("choropleth", "figure"),
              Output("GrafEsquerdaSup", "figure"),
              Output("GrafEsquerdaInf", "figure"),
              Output("GrafEsquerdaInf2", "figure"),
              Output("collapsedivdanos", "is_open"),
              Output("colapseddivistritossubpreituras", "is_open"),
              Output("colapseddivuniversalizacao", "is_open"),
              Output('divGrafEsquerdaSup', 'style'),
              Output('divGrafEsquerdaInf', 'style'),
              Output('divGrafEsquerdaInf2', 'style'),
              Output('divGrafDireita', 'style'),
              Output("info_body", "children"),
              Output("divInfo", "style"),
              Output("divSlider", "style"),
              Output("info_header", "children"),
              Output("collapseGraficosEsquerda", "is_open"),
              Output("collapseGraficosDireita", "is_open"),
              Output("colApresentacaoDireita", "is_open"),
              Output("collapseTabelaDistrito", "is_open"),
              Output("collapseTabelaSubprefeitura", "is_open"),
              Output("collapseTabelaGastosPerCapita", "is_open"),
              Output("collapseTabelaGastosAbsoluto", "is_open"),
              Output("collapseTabelaEja", "is_open"),
              Output("collapseTabelaEquipeMinimaDist", "is_open"),
              Output("collapseTabelaEquipeMinimaUnid", "is_open"),
              Output("collapseTabelaGastosUBS", "is_open"),
              Output("collapseTabelaGastosUBS2", "is_open"),
              Output("collapsedfTabelaGastos_UBS2_Unid", "is_open"),
              Input("dpEducacao", "value"),
              Input("dpSaude", "value"),
              # Input("dpUrbanismo", "value"),
              Input("dpOrcamento", "value"),
              Input("optdados", "value"),
              Input("optanos", "value"),
              Input("optuniversalizacao", "value"),
              Input("sliderEja", "value")
              )

def displayMapa(indicadores_educacao, indicadores_saude, indicadores_orcamento, dados, anos, anos_universalizacao, sliderEja):
    """Exibe os mapas e/ou gráficos gerados de acordo com os botões clicados, retornando
    as figuras de acordo.

    Variable type: String

    Options: 'ideb', 'idep', 'abandono', 'universalizacao', 'gastos1', 'gastos2', 'eja', 'equipe', 'ubs' ou 'gastoubs'"""

    user_click = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    colapseddivistritossubpreituras = False
    collapsedivdanos = False
    card_universalizacao = False
    collapseGraficosEsquerda = False
    collapseGraficosDireita = False
    collapseTabelaDistrito = False
    collapseTabelaSubprefeitura = False
    collapseTabelaGastosPerCapita = False
    collapseTabelaGastosAbsoluto = False
    collapseTabelaEja = False
    collapseTabelaEquipeMinimaDist = False
    collapseTabelaEquipeMinimaUnid = False
    collapseTabelaGastosUBS = False
    collapseTabelaGastosUBS2 = False
    collapsedfTabelaGastos_UBS2_Unid = False
    card_Apresentacao_Direita = True
    fig = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    fig4 = go.Figure()
    divEsquerdaSup = {"display": "none"}
    divEsquerdaInf = {"display": "none"}
    divEsquerdaInf2 = {"display": "none"}
    divGrafDireita = {"display": "none"}
    divInfo = {"display": "none"}
    divSlider = {"display": "none"}
    info = "vazio"
    info_header = "vazio"

    info_ideb = '''Os dados acima refletem o ano de 2019 e
foram extraídos dos indicadores educacionais do Inep, 
disponíveis no portal 'Dados Abertos do Inep.', href = "https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados"),
Foram extraídos os resultados por escolas da rede municipal de São Paulo
e então foi feita a média desses dados por Distrito da cidade de São Paulo.
Esses dados estão divididos entre Anos Iniciais e Anos Finais refletindo a forma 
como são apresentados no Inep, sendo anos iniciais do 1º ao 4º ano e anos finais do
5º ao 9º ano do Ensino fundamental.  Esses dados foram cruzados com os dados das 
unidades educacionais da rede Municipal de Ensino de São Paulo disponíveis no 
Portal de Dados Abertos da Prefeitura Municipal de São Paulo.", href= "http://dados.prefeitura.sp.gov.br/dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas")
A partir desse cruzamento foi feita a média do Ideb por Distrito mostrada na figura. Alguns distritos não apresentam Ideb, pois não possuem escolas de Ensino Fundamental da Rede Municipal de Educação  (os alunos destes distritos frequentam escolas estaduais ou escolas em outros distritos.'''

    info_idep = ''' href= "http://dados.prefeitura.sp.gov.br/dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas" Índice de Desenvolvimento da Educação Paulistana (IDEP)
    A Secretaria Municipal de Educação (SME) apresenta o Índice de Desenvolvimento da Educação Paulistana (IDEP). Ele foi estruturado com base no princípio de que todos os estudantes têm direito não só à educação, mas à educação de qualidade. O IDEP foi criado para expressar o desempenho das escolas da Rede Municipal de Ensino, considerando os componentes curriculares avaliados na Prova São Paulo e o fluxo escolar.
    Para o Ensino Fundamental, o IDEP será calculado considerando os resultados dos 3º, 5º, 7º e 9º anos na Prova São Paulo, avaliação externa municipal de caráter censitário. Para os anos iniciais, serão considerados os resultados dos estudantes dos 3º e 5º anos, em Língua Portuguesa, Matemática e Ciências. O fluxo escolar considerado será do 1º ao 5º ano. Da mesma forma, para os anos finais, serão considerados os resultados dos estudantes dos 7º e 9º anos e o fluxo escolar do 6º ao 9º ano.
    Neste conjunto de dados estão disponíveis o IDEP de cada unidade escolar relativo aos anos de 2018 e 2019, precedido pelo Índice de Nível Socioeconômico (NSE aferido em 2013 pelo Inep) e o Indicador de Complexidade de Gestão (ICG)* da escola, seguidos dos resultados esperados como metas para o IDEP em cada um dos 5 anos posteriores (2019 a 2023).
    *Índice de Nível Socioeconômico (INSE): sintetiza, de maneira unidimensional, informações sobre a escolaridade dos pais e a renda familiar. O seu objetivo é contextualizar o desempenho das escolas nas avaliações e exames realizados pelo INEP/MEC, bem como seus esforços na realização do trabalho educativo cotidiano. Busca-se uma caracterização do padrão de vida do público de cada unidade escolar, considerando suas características socioeconômicas.
    *Indicador de Complexidade de Gestão (ICG): resume em uma única medida as informações de porte, turnos de funcionamento, nível de complexidade das etapas de ensino e quantidade de etapas ofertadas. Ainda que estes fatores não contemplem em totalidade todos os elementos e dimensões envolvidas na gestão escolar, verifica-se que os itens selecionados colaboram para a construção de um índice que potencialmente auxilia na contextualização de resultados das avaliações. A base desse indicador é o ano de 2018.
    Para mais informações sobre o Índice de Desenvolvimento da Educação Paulistana (IDEP) consulte a Nota Técnica que acompanha este Conjunto de Dados (disponível para download em:  http://dados.prefeitura.sp.gov.br/dataset/idep ).
    Obs: Os dados com * indicam que a escola não atendeu a um dos critérios necessários para o cálculo do Idep ou das suas metas."'''

    if user_click == "dpEducacao":
        if indicadores_educacao is not None:
            if indicadores_educacao == "ideb":
                # Cria mapa e gráfico de linhas
                fig = gerar_mapa("ideb", anos, dados)

                ########################################################

                colapseddivistritossubpreituras = True
                collapsedivdanos = True
                collapseGraficosEsquerda = True
                collapseGraficosDireita = True
                card_Apresentacao_Direita = False
                divGrafDireita = {"display": "block"}
                # divEsquerdaSup = {"display": "block"}
                divInfo = {"display": "block"}
                info = info_ideb
                info_header = "Indicador - IDEB"

                if dados is not None:
                    if dados == "distrito":
                        collapseTabelaDistrito = True
                    else:
                        collapseTabelaSubprefeitura = True

            else:
                if indicadores_educacao == "idep":
                    labels = ['Faixa 1', 'Faixa 2', 'Faixa 3', 'Faixa 4', 'Faixa 5', 'Faixa 6']
                    values = [17, 13, 45, 21, 3, 1]

                    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    fig2.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                       autosize=True,
                                       title="Percentual de escolas por faixa do IDEP <br> Anos Iniciais (2019)",
                                       plot_bgcolor=colors['chart_background'],
                                       paper_bgcolor=colors['chart_background']
                                       )
                    colors_fig2 = ['rgb (230,159,0)', 'rgb (86,180,233)', 'rgb (0,158,115)', 'rgb (240,228,66)',
                                   'rgb (0,114,178)', 'rgb (213,94,0)']
                    fig2.update_traces(marker=dict(colors=colors_fig2, line=dict(color='#000000', width=1)))

                    dfBarra = pd.read_csv("data/idep_barras_iniciais.csv",
                                          sep=";",
                                          decimal=",")
                    fig = px.bar(dfBarra, y="Distrito",
                                 x=["Faixa 1", "Faixa 2", "Faixa 3", "Faixa 4", "Faixa 5", "Faixa 6"],
                                 orientation='h', title="Distribuição das escolas por faixa do Idep por Distrito (2019)",
                                 height=1200)
                    fig.update_layout(font_size=10, yaxis={'categoryorder': 'category descending'},
                                      plot_bgcolor=colors['chart_background'],
                                      paper_bgcolor=colors['chart_background']
                                      )

                    labels = ['Não Atingiram', 'Atingiram']
                    values = [15.50, 84.50]

                    fig3 = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    fig3.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                       autosize=True,
                                       showlegend=True,
                                       title="Escolas que atingiram a meta do IDEP <br> Anos Iniciais (2019)",
                                       plot_bgcolor=colors['chart_background'],
                                       paper_bgcolor=colors['chart_background']
                                       )
                    colors_fig3 = ['orange', 'skyblue']
                    fig3.update_traces(marker=dict(colors=colors_fig3, line=dict(color='#000000', width=1)))

                    labels = ['Não Atingiram', 'Atingiram']
                    values = [65.3, 34.7]

                    fig4 = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    fig4.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                                       autosize=True,
                                       showlegend=True,
                                       title="Escolas que atingiram a meta do IDEP <br> Anos Finais (2019)",
                                       plot_bgcolor=colors['chart_background'],
                                       paper_bgcolor=colors['chart_background']
                                       )
                    colors_fig4 = ['orange', 'skyblue']
                    fig4.update_traces(marker=dict(colors=colors_fig4, line=dict(color='#000000', width=1)))

                    divEsquerdaSup = {"display": "block"}
                    divEsquerdaInf = {"display": "block"}
                    divEsquerdaInf2 = {"display": "block"}
                    divGrafDireita = {"display": "block"}
                    divInfo = {"display": "block"}
                    info = info_idep
                    info_header = "Indicador - IDEP"
                    collapseGraficosEsquerda = True
                    collapseGraficosDireita = True
                    card_Apresentacao_Direita = False

                else:

                    if indicadores_educacao == "abandono":
                        df = pd.read_csv("data/evasao_linha.csv",
                                         sep=";",
                                         decimal=",")

                        fig2.add_trace(go.Scatter(
                            x=df.Ano, y=df.taxa, mode="markers", line_shape='linear',
                            marker_color=df.taxa, text=df.Ano, marker=dict(showscale=True)
                        ))
                        fig2.update_traces(marker_line_width=2, marker_size=10)

                        datah = [go.Scatter(x=df["Ano"], y=df["taxa"], hoverinfo="none", hovertext="")]

                        fig2 = go.Figure(data=datah)

                        # fig2 = go.Figure(layout={"template": "plotly_dark"})
                        fig2.layout.update(showlegend=False)
                        fig2.add_trace(go.Scatter(x=df["Ano"], y=df["taxa"]))
                        fig2.update_traces(marker_line_width=2, marker_size=3, mode="markers+lines")
                        fig2.update_layout(margin=dict(l=0, r=0, t=50, b=0), autosize=True,
                                           title="Taxa de abandono Ensino Fundamental",
                                           plot_bgcolor=colors['chart_background'],
                                           paper_bgcolor=colors['chart_background']
                                           )
                        fig2.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='black')
                        fig2.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='black')
                        # fig.update_layout(font_size=10, yaxis={'categoryorder': 'category descending'})

                        divEsquerdaSup = {"display": "block"}
                        divEsquerdaInf = {"display": "none"}
                        divGrafDireita = {"display": "block"}
                        divInfo = {"display": "block"}
                        collapseGraficosEsquerda = True
                        collapseGraficosDireita = True
                        card_Apresentacao_Direita = False

                        df = pd.read_csv("data/evasao_barra.csv",
                                         sep=";",
                                         decimal=",")
                        df['taxa'] = pd.to_numeric(df['taxa'], errors='coerce')
                        df = df.sort_values("taxa")
                        fig = px.bar(df, y="Distrito", x="taxa",
                                     orientation='h',
                                     title="Taxa de abandono no Ensino Fundamental(%)")
                        fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), height=1200, font_size=11,
                                          plot_bgcolor=colors['chart_background'],
                                          paper_bgcolor=colors['chart_background']
                                          )
                        # fig.update_layout(font_size=10, yaxis={'categoryorder': 'category descending'})
                        info = "abandono"
                        info_header = "Indicador - Taxa de Abandono"

                    else:

                        if indicadores_educacao == "universalizacao":

                            def custom_legend_name(new_names):
                                """Gera nomes customizados na legenda do gráfico de linhas da fig3 do Indicador de Universalização

                                Variable type: list"""

                                for i, new_name in enumerate(new_names):
                                    fig3.data[i].name = new_name

                            ####################

                            # fig = gerar_mapa("universalizacao", anos, "dist_universalizacao", anos_universalizacao)
                            dfLineRME = pd.read_csv("data/universalizacao_evol_matr_rme_15-20.csv",
                                                    sep=";",
                                                    decimal=",")
                            fig = px.line(dfLineRME,
                                          x="Ano",
                                          y="Matriculas",
                                          title='Matrículas na Pré-Escola da Rede Municipal de Ensino')
                            fig.update_layout(xaxis={'title': 'Ano'},
                                              yaxis={'title': 'Matrículas'},
                                              plot_bgcolor=colors['chart_background'],
                                              paper_bgcolor=colors['chart_background']
                                              )
                            fig.update_traces(mode="markers+lines")

                            ####################

                            dfLine = pd.read_csv("data/universalizacao_evol_indic_mun_15-20.csv",
                                                 sep=";",
                                                 decimal=",")
                            fig2 = px.line(dfLine,
                                           x="Ano",
                                           y="Taxa",
                                           title='Taxa de Universalização da Educação Infantil <br> (somente pré-escola) (%)')
                            fig2.update_layout(yaxis_range=[88, 100],
                                               xaxis={'title': 'Ano'},
                                               yaxis={'title': 'Taxa (%)'},
                                               plot_bgcolor=colors['chart_background'],
                                               paper_bgcolor=colors['chart_background']
                                               )
                            fig2.update_traces(mode="markers+lines")

                            dfLine2 = pd.read_csv("data/universalizacao_evol_var_mun_15-20.csv",
                                                  sep=";",
                                                  decimal=",")
                            fig3 = px.line(dfLine2,
                                           x="Ano",
                                           y=["Matriculas", "Populacao"],
                                           title='Taxa de Universalização da Educação Infantil <br> (somente pré-escola)')
                            custom_legend_name(['Matrículas<br>(todas as redes)', 'População<br>(4 e 5 anos)'])
                            fig3.update_layout(yaxis_range=[280000, 350000],
                                               xaxis={'title': 'Ano'},
                                               yaxis={'title': 'Taxa'},
                                               legend=dict(orientation="h",
                                                           yanchor="bottom",
                                                           y=-0.4, xanchor="right",
                                                           x=1),
                                               legend_title_text='',
                                               plot_bgcolor=colors['chart_background'],
                                               paper_bgcolor=colors['chart_background']
                                               )
                            fig3.update_traces(mode="markers+lines")

                            divEsquerdaSup = {"display": "block"}
                            divEsquerdaInf = {"display": "block"}
                            divGrafDireita = {"display": "block"}
                            divInfo = {"display": "block"}
                            info = info_idep
                            info_header = "Indicador - IDEP"
                            collapseGraficosEsquerda = True
                            collapseGraficosDireita = True
                            card_Apresentacao_Direita = False
                            card_universalizacao = False

                        else:

                            if indicadores_educacao == "gastos1":
                                fig = gerar_mapa("gastos1", anos, "", 0)

                                divEsquerdaSup = {"display": "block"}
                                divEsquerdaInf = {"display": "block"}
                                divGrafDireita = {"display": "block"}
                                divInfo = {"display": "block"}
                                info = info_idep
                                info_header = "Indicador - IDEP"
                                collapseGraficosDireita = True
                                card_Apresentacao_Direita = False
                                collapseTabelaGastosPerCapita = True

                            else:

                                if indicadores_educacao == "eja":

                                    # dfEjaGenero = pd.read_excel("data/eja.xlsx",
                                    #                             sheet_name="gênero")

                                    labels = ['Feminino', 'Masculino']
                                    values = [16515, 25103]

                                    # fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
                                    # fig2 = px.pie(dfEjaGenero,
                                    #               values='Gênero',
                                    #               names='Quantidade',
                                    #               title='Population of European continent')
                                    fig2 = go.Figure(data=[go.Pie(labels=labels, values=values,
                                                                  textinfo='label+percent',
                                                                  insidetextorientation='radial',
                                                                  hole=0.3
                                                                  )])
                                    fig2.update_layout(margin=dict(l=0, r=0, t=50, b=0), autosize=True,
                                                       title="Percentual por Gênero",
                                                       plot_bgcolor=colors['chart_background'],
                                                       paper_bgcolor=colors['chart_background']
                                                       )
                                    colors_fig2 = ['skyblue', 'orange']
                                    fig2.update_traces(marker=dict(colors=colors_fig2,
                                                                   line=dict(color='#000000', width=2)))

                                    dfEjaMatriculas = pd.read_csv("data/eja_matriculas2.csv",
                                                                  sep=";",
                                                                  decimal=",")

                                    dfSlider = dfEjaMatriculas.loc[(dfEjaMatriculas['Ano'] >= sliderEja[0]) &
                                                                   (dfEjaMatriculas['Ano'] <= sliderEja[1])]

                                    fig = px.line(dfSlider, x='Ano', y='Matrículas', color='Distrito',
                                                  height=600, width=600,
                                                  orientation="v",
                                                  title="EJA - Matrículas por Distrito")
                                    fig.update_layout(xaxis_tickformat='d',
                                                      plot_bgcolor=colors['chart_background'],
                                                      paper_bgcolor=colors['chart_background']
                                                      )
                                    fig.update_xaxes(
                                        showgrid=True,
                                        ticks="outside",
                                        tickson="boundaries",
                                        ticklen=0
                                    )

                                    labels = ['Amarelo', 'Branco', 'Indígena', 'Não declarada',
                                              'Parda', 'Preta', 'Recusou informar']
                                    values = [135, 11565, 87, 7907, 13767, 3906, 4273]

                                    fig3 = go.Figure(data=[go.Pie(labels=labels, values=values,
                                                                  textinfo='label+percent',
                                                                  insidetextorientation='radial')])
                                    fig3.update_layout(margin=dict(l=0, r=0, t=50, b=0), autosize=True, showlegend=True,
                                                       title="Percentual por Raça",
                                                       plot_bgcolor=colors['chart_background'],
                                                       paper_bgcolor=colors['chart_background']
                                                       )
                                    colors_fig3 = ['#f8f398', 'wheat', 'lightsalmon', 'dimgray', '#6f4e37', '#2c1608',
                                                   'gray']
                                    fig3.update_traces(marker=dict(colors=colors_fig3))

                                    labels = ['15-18', '19-25', '26-30', '31-40', '41-50', '51-60', '61-70', '71-94']
                                    values = [6332, 5411, 2679, 6091, 8856, 6994, 3540, 1711]

                                    fig4 = go.Figure(data=[go.Pie(labels=labels, values=values,
                                                                  textinfo='label+percent',
                                                                  insidetextorientation='auto')])
                                    fig4.update_layout(margin=dict(l=0, r=0, t=50, b=0), autosize=True, showlegend=True,
                                                       title="Percentual por Idade",
                                                       plot_bgcolor=colors['chart_background'],
                                                       paper_bgcolor=colors['chart_background']
                                                       )
                                    colors_fig4 = ['rgb (255,255,255)', 'rgb (230,159,0)', 'rgb (86,180,233)',
                                                   'rgb (0,158,115)', 'rgb (240,228,66)', 'rgb (0,114,178)',
                                                   'rgb (213,94,0)', 'rgb (204,121,167)']
                                    fig4.update_traces(marker=dict(colors=colors_fig4, line=dict(color='#000000', width=1)))

                                    divEsquerdaSup = {"display": "block"}
                                    divEsquerdaInf = {"display": "block"}
                                    divEsquerdaInf2 = {"display": "block"}
                                    divGrafDireita = {"display": "block"}
                                    divInfo = {"display": "block"}
                                    divSlider = {"display": "block"}
                                    info = info_idep
                                    info_header = "Indicador - IDEP"
                                    collapseGraficosEsquerda = True
                                    collapseGraficosDireita = True
                                    card_Apresentacao_Direita = False
                                    collapseTabelaEja = True

                                else:

                                    if indicadores_educacao == 'gastos2':

                                        fig = gerar_mapa("gastos2", anos, "", 0)

                                        divEsquerdaSup = {"display": "block"}
                                        divEsquerdaInf = {"display": "block"}
                                        divGrafDireita = {"display": "block"}
                                        divInfo = {"display": "block"}
                                        info = info_idep
                                        info_header = "Indicador - IDEP"
                                        collapseGraficosDireita = True
                                        card_Apresentacao_Direita = False
                                        collapseTabelaGastosAbsoluto = True


    elif user_click == "dpSaude":
        if indicadores_saude is not None:
            if indicadores_saude == 'equipe':

                fig = gerar_mapa("equipe", anos, "", 0)

                divEsquerdaSup = {"display": "block"}
                divEsquerdaInf = {"display": "block"}
                divGrafDireita = {"display": "block"}
                divInfo = {"display": "block"}
                info = info_idep
                info_header = "Indicador - IDEP"
                collapseGraficosDireita = True
                card_Apresentacao_Direita = False
                collapseTabelaEquipeMinimaDist = True
                collapseTabelaEquipeMinimaUnid = True


    elif user_click == "dpOrcamento":
        if indicadores_orcamento is not None:
            if indicadores_orcamento == 'ubs':
                fig = gerar_mapa("ubs", anos, "", 0)

                divEsquerdaSup = {"display": "block"}
                divEsquerdaInf = {"display": "block"}
                divGrafDireita = {"display": "block"}
                divInfo = {"display": "block"}
                info = info_idep
                info_header = "Indicador - Saúde"
                collapseGraficosDireita = True
                card_Apresentacao_Direita = False
                collapseTabelaGastosUBS = True

            else:

                if indicadores_orcamento == 'gastoubs':
                    fig = gerar_mapa("gastoubs", anos, "", 0)

                    divEsquerdaSup = {"display": "block"}
                    divEsquerdaInf = {"display": "block"}
                    divGrafDireita = {"display": "block"}
                    divInfo = {"display": "block"}
                    info = info_idep
                    info_header = "Indicador - Saúde"
                    collapseGraficosDireita = True
                    card_Apresentacao_Direita = False
                    collapseTabelaGastosUBS2 = True
                    collapsedfTabelaGastos_UBS2_Unid = True


    # elif user_click == "dpSaude":
    #     if indicadores_saude is not None:
    #         pass

    else:  # indicadores não escolhidos
        return (go.Figure(), go.Figure(), go.Figure(), go.Figure(), collapsedivdanos,
                colapseddivistritossubpreituras, card_universalizacao, divEsquerdaSup, divEsquerdaInf,
                divEsquerdaInf2, divGrafDireita, info, divInfo, divSlider, info_header, collapseGraficosEsquerda,
                collapseGraficosDireita, card_Apresentacao_Direita, collapseTabelaDistrito,
                collapseTabelaSubprefeitura, collapseTabelaGastosPerCapita, collapseTabelaGastosAbsoluto,
                collapseTabelaEja, collapseTabelaEquipeMinimaDist, collapseTabelaEquipeMinimaUnid, collapseTabelaGastosUBS, collapseTabelaGastosUBS2,
                collapsedfTabelaGastos_UBS2_Unid)

    return (fig, fig2, fig3, fig4, collapsedivdanos, colapseddivistritossubpreituras, card_universalizacao,
            divEsquerdaSup, divEsquerdaInf, divEsquerdaInf2, divGrafDireita, info, divInfo, divSlider, info_header,
            collapseGraficosEsquerda, collapseGraficosDireita, card_Apresentacao_Direita, collapseTabelaDistrito,
            collapseTabelaSubprefeitura, collapseTabelaGastosPerCapita, collapseTabelaGastosAbsoluto,
            collapseTabelaEja, collapseTabelaEquipeMinimaDist, collapseTabelaEquipeMinimaUnid, collapseTabelaGastosUBS, collapseTabelaGastosUBS2,
            collapsedfTabelaGastos_UBS2_Unid)

def toggle_modal(n1, n2, is_open):
    """Torna o botão de info funcional"""

    if n1 or n2:
        return not is_open
    return is_open


# app.callback(
#     Output("modal-scroll", "is_open"),
#     [Input("open-scroll", "n_clicks"), Input("close-scroll", "n_clicks")],
#     [State("modal-scroll", "is_open")],
# )(toggle_modal)

app.callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)(toggle_modal)

if __name__ == "__main__":

    app.run_server(debug=True)
