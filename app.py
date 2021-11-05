# coding=utf-8
import dash
#from dash import dcc
#from dash import html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import json
import pandas as pd
from front_end import navbar, collapse
from analyse_data.regionalizar_distritos import RegionalizarDistritos
from get_data import get_data, get_distritos, get_subprefeituras, obterIdeb, obterDistritos, obterSubprefeituras
import dash_table
import plotly.io as pio

# Declarando o tema escuro para aplicar aos plots
plotly_template = pio.templates["plotly_dark"]

# Declarando o tema escuro que é aplicado na propriedades
# Isso normalmente é aplicado após o app = dash.Dash(__name__)
# Porém como há cards declarados em variáveis fora dele se fez necessário declarar ele aqui
colors = {
    'background': '#000000',
    'text': '#7FDBFF',
    'table_cell': '#111111',
    'table_text': '#bebebe'
}

pio.templates.default = "plotly_dark"

dfDadosIdeb = obterIdeb.dadosIdeb('data/cadastro_ideb_merged.csv')
dfDadosIdeb['ideb_2019'] = dfDadosIdeb['ideb_2019'].fillna(0)
dfDadosIdeb['coddist'] = dfDadosIdeb['coddist'].fillna(0)
dfDadosIdeb['codsub'] = dfDadosIdeb['codsub'].fillna(0)

totalEscolas = len(pd.unique(dfDadosIdeb["codigo_escola"]))

# Chamando a planilha de opções do dropdown de educação e a colocando em uma variável
dropdown_educ_location = 'data/dropdown_educacao.csv'
lista_educacao = pd.read_csv(dropdown_educ_location)

# Chamando a planilha de opções do dropdown de saude e a colocando em uma variável
dropdown_saud_location = 'data/dropdown_saude.csv'
lista_saude = pd.read_csv(dropdown_saud_location)

# Chamando a planilha de opções do dropdown de urbanismo e a colocando em uma variável
dropdown_urba_location = 'data/dropdown_urbanismo.csv'
lista_urbanismo = pd.read_csv(dropdown_urba_location)

# Chamando a planilha de opções do dropdown de orçamento e a colocando em uma variável
dropdown_orca_location = 'data/dropdown_orcamento.csv'
lista_orcamento = pd.read_csv(dropdown_orca_location)

filt = (dfDadosIdeb["tipo_anos"] == "iniciais")
df_filt = dfDadosIdeb[filt]
dfDadosIdebIniciais = df_filt.reset_index()

filt = (dfDadosIdeb["tipo_anos"] == "finais")
df_filt = dfDadosIdeb[filt]
dfDadosIdebFinais = df_filt.reset_index()


dfDadosDistritos = obterDistritos.distritos('data/geo_data/SIRGAS_SHP_distrito', dfDadosIdebIniciais, dfDadosIdebFinais)
dfDadoSubprefeituras = obterSubprefeituras.subprefeituras('data/geo_data/SIRGAS_SHP_subprefeitura', dfDadosIdebIniciais, dfDadosIdebFinais)

dfTabelaDistrito = dfDadosDistritos.filter(['ds_nome', 'ideb_iniciais', 'ideb_finais', 'media_final'], axis=1)
dfTabelaDistrito = dfTabelaDistrito.rename(columns = {'ds_nome': 'Nome', 'ideb_iniciais': 'Iniciais', 'ideb_finais': 'Finais', 'media_final': 'Média'}, inplace = False)
dfTabelaDistrito['Iniciais'] = dfTabelaDistrito['Iniciais'].apply(lambda x: round(x,2) if not pd.isnull(x) else 0)
dfTabelaDistrito['Finais'] = dfTabelaDistrito['Finais'].apply(lambda x: round(x,2) if not pd.isnull(x) else 0)
dfTabelaDistrito['Média'] = dfTabelaDistrito['Média'].apply(lambda x: round(x,2) if not pd.isnull(x) else 0)
#dfTabelaDistrito = dfTabelaDistrito.sort_values(by=['Iniciais'])


dfTabelaSubprefeitura = dfDadoSubprefeituras.filter(['sp_nome', 'ideb_iniciais', 'ideb_finais', 'media_final'], axis=1)
dfTabelaSubprefeitura = dfTabelaSubprefeitura.rename(columns = {'sp_nome': 'Nome', 'ideb_iniciais': 'Iniciais', 'ideb_finais': 'Finais', 'media_final': 'Média'}, inplace = False)
dfTabelaSubprefeitura['Iniciais'] = dfTabelaSubprefeitura['Iniciais'].apply(lambda x: round(x,2) if not pd.isnull(x) else 0)
dfTabelaSubprefeitura['Finais'] = dfTabelaSubprefeitura['Finais'].apply(lambda x: round(x,2) if not pd.isnull(x) else 0)
dfTabelaSubprefeitura['Média'] = dfTabelaSubprefeitura['Média'].apply(lambda x: round(x,2) if not pd.isnull(x) else 0)
#dfTabelaSubprefeitura = dfTabelaSubprefeitura.sort_values(by=['Iniciais'])

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

info_ideb = html.Div(id="divInfo", children = [
        dbc.Button(
            "Info", id="open-body-scroll", color="info", n_clicks=0
        ),
          dbc.Modal(
            [
                dbc.ModalHeader(id = "info_header"),
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


# info_ideb = html.Div(
#     [
#         dbc.Button(
#             "Modal with scrollable body", id="btn_info_ideb", n_clicks=0
#         ),
#         dbc.Modal(
#             [
#                 dbc.ModalHeader("Header"),
#                 dbc.ModalBody(
#
# '''Índice de Desenvolvimento da Educação Paulistana (IDEP)
# A Secretaria Municipal de Educação (SME) apresenta o Índice de Desenvolvimento da Educação Paulistana (IDEP). Ele foi estruturado com base no princípio de que todos os estudantes têm direito não só à educação, mas à educação de qualidade. O IDEP foi criado para expressar o desempenho das escolas da Rede Municipal de Ensino, considerando os componentes curriculares avaliados na Prova São Paulo e o fluxo escolar.
# Para o Ensino Fundamental, o IDEP será calculado considerando os resultados dos 3º, 5º, 7º e 9º anos na Prova São Paulo, avaliação externa municipal de caráter censitário. Para os anos iniciais, serão considerados os resultados dos estudantes dos 3º e 5º anos, em Língua Portuguesa, Matemática e Ciências. O fluxo escolar considerado será do 1º ao 5º ano. Da mesma forma, para os anos finais, serão considerados os resultados dos estudantes dos 7º e 9º anos e o fluxo escolar do 6º ao 9º ano.
# Neste conjunto de dados estão disponíveis o IDEP de cada unidade escolar relativo aos anos de 2018 e 2019, precedido pelo Índice de Nível Socioeconômico (NSE aferido em 2013 pelo Inep) e o Indicador de Complexidade de Gestão (ICG)* da escola, seguidos dos resultados esperados como metas para o IDEP em cada um dos 5 anos posteriores (2019 a 2023).
# *Índice de Nível Socioeconômico (INSE): sintetiza, de maneira unidimensional, informações sobre a escolaridade dos pais e a renda familiar. O seu objetivo é contextualizar o desempenho das escolas nas avaliações e exames realizados pelo INEP/MEC, bem como seus esforços na realização do trabalho educativo cotidiano. Busca-se uma caracterização do padrão de vida do público de cada unidade escolar, considerando suas características socioeconômicas.
# *Indicador de Complexidade de Gestão (ICG): resume em uma única medida as informações de porte, turnos de funcionamento, nível de complexidade das etapas de ensino e quantidade de etapas ofertadas. Ainda que estes fatores não contemplem em totalidade todos os elementos e dimensões envolvidas na gestão escolar, verifica-se que os itens selecionados colaboram para a construção de um índice que potencialmente auxilia na contextualização de resultados das avaliações. A base desse indicador é o ano de 2018.
# Para mais informações sobre o Índice de Desenvolvimento da Educação Paulistana (IDEP) consulte a Nota Técnica que acompanha este Conjunto de Dados (disponível para download em:  http://dados.prefeitura.sp.gov.br/dataset/idep ).
# Obs: Os dados com * indicam que a escola não atendeu a um dos critérios necessários para o cálculo do Idep ou das suas metas."'''
#                 ),
#                 dbc.ModalFooter(
#                     dbc.Button(
#                         "Fechar",
#                         id="close-scroll",
#                         className="ml-auto",
#                         n_clicks=0,
#                     )
#                 ),
#             ],
#             id="modal-scroll",
#             scrollable=True,
#             is_open=False,
#         ),
#
#     ]
# )
#

# Fazendo a lista de opções de educação se tormar funcional
dropdown_educacao = [{'label': i, 'value': i} for i in lista_educacao['Indicador'].unique()]
dropdown_educacao.insert(0, {'label': 'Escolha um indicador', 'value': 'Escolha um indicador'})
print(dropdown_educacao)  # printando para testar

# Fazendo a lista de opções de saúde se tormar funcional
dropdown_saude = [{'label': i, 'value': i} for i in lista_saude['Indicador'].unique()]
dropdown_saude.insert(0, {'label': 'Escolha um indicador', 'value': 'Escolha um indicador'})

# Fazendo a lista de opções de urbanismo se tormar funcional
dropdown_urbanismo = [{'label': i, 'value': i} for i in lista_urbanismo['Indicador'].unique()]
dropdown_urbanismo.insert(0, {'label': 'Escolha um indicador', 'value': 'Escolha um indicador'})

# Fazendo a lista de opções de orçamento se tormar funcional
dropdown_orcamento = [{'label': i, 'value': i} for i in lista_orcamento['Indicador'].unique()]
dropdown_orcamento.insert(0, {'label': 'Escolha um indicador', 'value': 'Escolha um indicador'})

divdistritossubpreituras = dbc.Collapse(
    dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
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

        #info_ideb

    ])

])

], color="dark", outline=True), id="colapseddivistritossubpreituras", is_open=False)

divdanos = dbc.Collapse(
    dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
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



def gerar_geodf(anos_ideb):

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
        if anos_ideb =="inicias":
            geodf = dfDadosDistritos
            geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
            geodf['text'] = geodf['ds_nome'] + ':<br>Nota média:' \
                + geodf['ideb_iniciais'].apply(lambda x: str(round(x,2)) if not pd.isnull(x) or x !=0 else 'Não se aplica')

    return geodf

def gerar_texto():
    dfDistritosMini = dfDadosDistritos.loc[dfDadosDistritos['ideb_iniciais'] == dfDadosDistritos['ideb_iniciais'].apply(lambda x: x if x > 0 else None).min()]
    dfDistritosMaxi = dfDadosDistritos.loc[dfDadosDistritos['ideb_iniciais'] == dfDadosDistritos['ideb_iniciais'].apply(lambda x: x if x > 0 else None).max()]
    dfDistritosMinf = dfDadosDistritos.loc[dfDadosDistritos['ideb_finais'] == dfDadosDistritos['ideb_finais'].apply(lambda x: x if x > 0 else None).min()]
    dfDistritosMaxf = dfDadosDistritos.loc[dfDadosDistritos['ideb_finais'] == dfDadosDistritos['ideb_finais'].apply(lambda x: x if x > 0 else None).max()]
    dfDistritosMediai = dfDadosDistritos.loc[dfDadosDistritos['media_final'] == dfDadosDistritos['media_final'].apply(lambda x: x if x > 0 else None).min()]
    dfDistritosMediaf = dfDadosDistritos.loc[dfDadosDistritos['media_final'] == dfDadosDistritos['media_final'].apply(lambda x: x if x > 0 else None).max()]

    dfSubprefeiturasMini = dfDadoSubprefeituras.loc[dfDadoSubprefeituras['ideb_iniciais'] == dfDadoSubprefeituras['ideb_iniciais'].apply(lambda x: x if x > 0 else None).min()]
    dfSubprefeiturasMaxi = dfDadoSubprefeituras.loc[dfDadoSubprefeituras['ideb_iniciais'] == dfDadoSubprefeituras['ideb_iniciais'].apply(lambda x: x if x > 0 else None).max()]
    dfSubprefeiturasMinf = dfDadoSubprefeituras.loc[dfDadoSubprefeituras['ideb_finais'] == dfDadoSubprefeituras['ideb_finais'].apply(lambda x: x if x > 0 else None).min()]
    dfSubprefeiturasMaxf = dfDadoSubprefeituras.loc[dfDadoSubprefeituras['ideb_finais'] == dfDadoSubprefeituras['ideb_finais'].apply(lambda x: x if x > 0 else None).max()]
    dfSubprefeiturasMediai = dfDadoSubprefeituras.loc[dfDadoSubprefeituras['media_final'] == dfDadoSubprefeituras['media_final'].apply(lambda x: x if x > 0 else None).min()]
    dfSubprefeiturasMediaf = dfDadoSubprefeituras.loc[dfDadoSubprefeituras['media_final'] == dfDadoSubprefeituras['media_final'].apply(lambda x: x if x > 0 else None).max()]

    vdfDistritosMini = dfDistritosMini["ideb_iniciais"].values[0]
    vdfDistritosMaxi = dfDistritosMaxi["ideb_iniciais"].values[0]
    vdfDistritosMinf = dfDistritosMinf["ideb_finais"].values[0]
    vdfDistritosMaxf = dfDistritosMaxf["ideb_finais"].values[0]
    vdfDistritosMediai = dfDistritosMediai["media_final"].values[0]
    vdfDistritosMediaf = dfDistritosMediaf["media_final"].values[0]
    vQtdDistritos = len(dfDadosDistritos)

    vdfSubprefeiturasMini = dfSubprefeiturasMini["ideb_iniciais"].values[0]
    vfSubprefeiturasMaxi = dfSubprefeiturasMaxi["ideb_iniciais"].values[0]
    vdfSubprefeiturasMinf = dfSubprefeiturasMinf["ideb_finais"].values[0]
    vfSubprefeiturasMaxf = dfSubprefeiturasMaxf["ideb_finais"].values[0]
    vfSubprefeiturasMediai = dfSubprefeiturasMediai["media_final"].values[0]
    vfSubprefeiturasMediaf = dfSubprefeiturasMediaf["media_final"].values[0]
    vQtdSubprefeituras = len(dfDadoSubprefeituras)

    totais  = (vdfDistritosMini, vdfDistritosMaxi, vdfDistritosMinf, vdfDistritosMaxf, vQtdDistritos, vdfSubprefeiturasMini,
               vfSubprefeiturasMaxi, vdfSubprefeiturasMinf, vfSubprefeiturasMaxf, vQtdSubprefeituras,
               vdfDistritosMediai, vdfDistritosMediaf, vfSubprefeiturasMediai, vfSubprefeiturasMediaf)

    return totais

def gerar_mapa(tipografico, anos_ideb, tipodados):

    fig = go.Figure()

    txtTotalDistritosIniciais = "Distritos: " + str(round(totais[4], 2)) + " Escolas: " + str(totalEscolas) + " Menor nota: " + \
                                str(round(totais[0], 2)) + " Maior nota: " + str(round(totais[1], 2))

    txtTotalDistritosFinais = "Distritos: " + str(round(totais[4])) + " Escolas: " + str(totalEscolas) + " Menor nota: " + \
                              str(round(totais[2], 2)) + " Maior nota: " + str(round(totais[3], 2))

    txtTotalDistritosMedia = "Distritos: " + str(round(totais[4], 2)) + " Escolas: " + str(totalEscolas) + " Menor nota: " + \
                             str(round(totais[10], 2)) + " Maior nota: " + str(round(totais[11], 2))

    txtTotalSubprefeiturasIniciais = "Subprefeituras: " + str(round(totais[9], 2)) + " Escolas: " + str(totalEscolas) + " Menor nota: " + \
                                  str(round(totais[5], 2)) + " Maior nota: " + str(round(totais[6], 2))

    txtTotalSubprefeiturasFinais = "Subprefeituras: " + str(round(totais[9])) + " Escolas: " + str(totalEscolas) + " Menor nota: " + \
                                str(round(totais[7], 2)) + " Maior nota: " + str(round(totais[8], 2))

    txtTotalSubprefeiturasMedia = "Subprefeituras: " + str(round(totais[9], 2)) + " Escolas: " + str(totalEscolas) + " Menor nota: " + \
                               str(round(totais[12], 2)) + " Maior nota: " + str(round(totais[13], 2))



    if tipografico == "mapa":

        if tipodados == "distrito":
            geodf = dfDadosDistritos
            geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
            geodf['text'] = geodf['ds_nome'] + ':<br>Nota média:' \
                        + geodf[anos_ideb].apply(
            lambda x: str(round(x, 2)) if not x==0 else 'Não se aplica')

            min_ideb = geodf[anos_ideb].min()
            fig = go.Figure(data=go.Choropleth(
            geojson=json.loads(geodf.geometry.to_json()),
            locations=geodf.index,
            z=geodf[anos_ideb],
            colorscale='Reds',
            autocolorscale=False,
            text=geodf['text'], # hover text
            hoverinfo = 'text',
            colorbar_title="IDEB 2019",
            zmin=min_ideb,
            zmax = geodf[anos_ideb].max(),
            ))
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=True, height=500)

            # fig = px.choropleth(geodf, geojson=geodf.geometry, locations=geodf.index, color="ideb_iniciais")
            # fig.update_geos(fitbounds="locations", visible=False)
            # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), autosize=True)

            if anos_ideb == "ideb_iniciais":
                txtTotal = txtTotalDistritosIniciais
            else:
                if anos_ideb == "ideb_finais":
                    txtTotal = txtTotalDistritosFinais
                else:
                    txtTotal = txtTotalDistritosMedia

        else:
            if tipodados == "subprefeitura":
                geodf = dfDadoSubprefeituras
                geodf['geometry'] = geodf['geometry'].to_crs(epsg=4669)
                geodf['text'] = geodf['sp_nome'] + ':<br>Nota média:' \
                            + geodf[anos_ideb].apply(
                lambda x: str(round(x, 2)) if not x==0 else 'Não se aplica')

                min_ideb = geodf[anos_ideb].min()
                fig = go.Figure(data=go.Choropleth(
                geojson=json.loads(geodf.geometry.to_json()),
                locations=geodf.index,
                z=geodf[anos_ideb],
                colorscale='Reds',
                autocolorscale=False,
                text=geodf['text'], # hover text
                hoverinfo = 'text',
                colorbar_title="IDEB 2019",
                zmin=min_ideb,
                zmax = geodf[anos_ideb].max(),
                ))
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(margin={"r":0,"t":20,"l":0,"b":0})

                if anos_ideb == "ideb_iniciais":
                    txtTotal = txtTotalSubprefeiturasIniciais
                else:
                    if anos_ideb == "ideb_finais":
                        txtTotal = txtTotalSubprefeiturasFinais
                    else:
                        txtTotal = txtTotalSubprefeiturasMedia
    else:
        if tipografico == "distribuicao":
            if tipodados == "distrito":
                geodf = dfDadosDistritos
                if anos_ideb == 'ideb_iniciais':
                    fig.add_trace(go.Scatter(
                        x=geodf.ds_nome, y=geodf.ideb_iniciais, mode="markers",
                        marker_color=geodf.ideb_iniciais, text=geodf.ds_nome, marker=dict(showscale=True), orientation="v"
                    ))
                    fig.update_traces(marker_line_width=2, marker_size=10)
                else:
                    if anos_ideb == 'ideb_finais':
                        fig.add_trace(go.Scatter(
                            x=geodf.ds_nome, y=geodf.ideb_finais, mode="markers",
                            marker_color=geodf.ideb_finais, text=geodf.ds_nome, marker=dict(showscale=True)
                        ))
                    else:
                        fig.add_trace(go.Scatter(
                            x=geodf.ds_nome, y=geodf.media_final, mode="markers",
                            marker_color=geodf.media_final, text=geodf.ds_nome, marker=dict(showscale=True)
                        ))

                if anos_ideb == "ideb_iniciais":
                    txtTotal = txtTotalDistritosIniciais
                else:
                    if anos_ideb == "ideb_finais":
                        txtTotal = txtTotalDistritosFinais
                    else:
                        txtTotal = txtTotalDistritosMedia

            else:
                if tipodados == "subprefeitura":
                    geodf = dfDadoSubprefeituras
                    if anos_ideb == 'ideb_iniciais':
                        fig.add_trace(go.Scatter(
                            x=geodf.sp_nome, y=geodf.ideb_iniciais, mode="markers",
                            marker_color=geodf.ideb_iniciais, text=geodf.sp_nome, marker=dict(showscale=True)
                        ))
                        fig.update_traces(marker_line_width=2, marker_size=10)
                    else:
                        if anos_ideb == 'ideb_finais':
                            fig.add_trace(go.Scatter(
                                x=geodf.sp_nome, y=geodf.ideb_iniciais, mode="markers",
                                marker_color=geodf.ideb_finais, text=geodf.sp_nome, marker=dict(showscale=True)
                            ))
                            fig.update_traces(marker_line_width=2, marker_size=10)
                        else:
                            fig.add_trace(go.Scatter(
                                x=geodf.sp_nome, y=geodf.media_final, mode="markers",
                                marker_color=geodf.media_final, text=geodf.sp_nome, marker=dict(showscale=True)
                            ))
                            fig.update_traces(marker_line_width=2, marker_size=10)

                    if anos_ideb == "ideb_iniciais":
                        txtTotal = txtTotalSubprefeiturasIniciais
                    else:
                        if anos_ideb == "ideb_finais":
                            txtTotal = txtTotalSubprefeiturasFinais
                        else:
                            txtTotal = txtTotalSubprefeiturasMedia
        else: #Barras
            if tipodados == "distrito":
                if anos_ideb == "ideb_iniciais":
                    ggg = dfDadosDistritos.sort_values("ideb_iniciais")
                    m = ggg["ideb_iniciais"].mean()
                    ggg["media"] = m

                    datah = [go.Bar(x=ggg.ds_nome, y=ggg.ideb_iniciais, name="Distritos"),
                             go.Scatter(x=ggg.ds_nome, y=ggg.media, hoverinfo="none", hovertext="",
                                        name="Média (" + str(round(m, 2)) + ")")]

                else:
                    if anos_ideb == 'ideb_finais':
                        ggg = dfDadosDistritos.sort_values("ideb_finais")
                        m = ggg["ideb_finais"].mean()
                        ggg["media"] = m

                        datah = [go.Bar(x=ggg.ds_nome, y=ggg.ideb_finais, name="Distritos"),
                                 go.Scatter(x=ggg.ds_nome, y=ggg.media, hoverinfo="none", hovertext="",
                                            name="Média (" + str(round(m, 2)) + ")")]

                    else:
                        ggg = dfDadosDistritos.sort_values("media_final")
                        m = ggg["ideb_finais"].mean()
                        ggg["media"] = m

                        datah = [go.Bar(x=ggg.ds_nome, y=ggg.media_final, name="Distritos"),
                                 go.Scatter(x=ggg.ds_nome, y=ggg.media, hoverinfo="none", hovertext="",
                                            name="Média (" + str(round(m, 2)) + ")")]

                if anos_ideb == "ideb_iniciais":
                    txtTotal = txtTotalDistritosIniciais
                else:
                    if anos_ideb == "ideb_finais":
                        txtTotal = txtTotalDistritosFinais
                    else:
                        txtTotal = txtTotalDistritosMedia

                fig = go.Figure(data=datah)

            else:
                if tipodados == "subprefeitura":
                    if anos_ideb == "ideb_iniciais":
                        ggg = dfDadoSubprefeituras.sort_values("ideb_iniciais")
                        m = ggg["ideb_iniciais"].mean()
                        ggg["media"] = m

                        datah = [go.Bar(x=ggg.sp_nome, y=ggg.ideb_iniciais, name="Subprefeituras"),
                                 go.Scatter(x=ggg.sp_nome, y=ggg.media, hoverinfo="none", hovertext="",
                                            name="Média (" + str(round(m, 2)) + ")")
                                 ]
                        # layouth = go.Layout(title="Notas dos Distritos por ordem crescente.")
                    else:
                        if anos_ideb == 'ideb_finais':
                            ggg = dfDadoSubprefeituras.sort_values("ideb_finais")
                            m = ggg["ideb_finais"].mean()
                            ggg["media"] = m

                            datah = [go.Bar(x=ggg.sp_nome, y=ggg.ideb_finais, name="Subprefeituras"),
                                     go.Scatter(x=ggg.sp_nome, y=ggg.media, hoverinfo="none", hovertext="",
                                                name="Média (" + str(round(m, 2)) + ")")
                                     ]
                        else:
                            ggg = dfDadoSubprefeituras.sort_values("media_final")
                            m = ggg["media_final"].mean()
                            ggg["media"] = m

                            datah = [go.Bar(x=ggg.sp_nome, y=ggg.media_final, name="Subprefeituras"),
                                     go.Scatter(x=ggg.sp_nome, y=ggg.media, hoverinfo="none", hovertext="",
                                                name="Média (" + str(round(m, 2)) + ")")
                                     ]
                            # layouth = go.Layout(title="Notas dos Distritos por ordem crescente.")

                fig = go.Figure(data=datah)

                if anos_ideb == "ideb_iniciais":
                    txtTotal = txtTotalSubprefeiturasIniciais
                else:
                    if anos_ideb == "ideb_finais":
                        txtTotal = txtTotalSubprefeiturasFinais
                    else:
                        txtTotal = txtTotalSubprefeiturasMedia



    return fig

totais = gerar_texto()

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

server = app.server

app.title = 'Regionalização IDEB 2019'

# app.layout = dbc.Container(children=[
#     navbar,
#     dbc.Row([
#         dbc.Col([
#             dcc.Dropdown(
#                 id='dados',
#                 options=[{'label' : 'Distritos', 'value' : 'distrito'},
#                          {'label' : 'Subprefeituras', 'value' : 'subprefeitura'}],
#                         style={'height': '40px'},
#                 placeholder='Dados'
#
#             )
#         ], md=3),
#         dbc.Col([
#             dcc.Dropdown(
#                 id='anos_ideb',
#                 options=[{'label' : 'Anos iniciais', 'value' : 'ideb_iniciais'},
#                          {'label' : 'Anos Finais', 'value' : 'ideb_finais'},
#                          {'label' : 'Todos', 'value' : 'media_final'}],
#                          style={'height': '40px'},
#                          placeholder='Anos'
#
#             )
#         ], md=3),
#         dbc.Col([
#             dcc.Dropdown(
#                 id='visualizacao',
#                 options=[{'label': 'Mapa', 'value': 'mapa'},
#                          {'label': 'Distribuição', 'value': 'distribuicao'},
#                          {'label': 'Barra', 'value': 'barra'}],
#                          style={'height': '40px'},
#                          placeholder='Tipos de Gráfico'
#             )], md=3),
#         dbc.Col([
#             dbc.Button("Ok", id="submit", color="info", style={"verticalAlign": "middle", 'height': '40px', "border-radius": "10%"}, n_clicks=0)
#         ], md=3),
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody(children=[
#                     html.H6("21111", id="textototal"),
#
#             ])
#             ], color="Light", style={"border-style": "none"})
#         ])
#
#     ]),
#     dbc.Row([
#         dbc.Col([
#             dcc.Loading(id="Loading-1", type="default",
#                     children=[dcc.Graph(id="choropleth")])
#         ])
#
#     ]),
#     dbc.Row([
#         dbc.Col([
#             collapse
#         ])
#
#     ])
#
# ])
loading_style = {'position': 'absolute', 'align-self': 'center'}

app.layout = dbc.Container(style={'backgroundColor': colors['background']}, children=[
    dbc.Row([
        dbc.Col([
            dbc.Card(style={'backgroundColor': colors['background']}, children=[
                    dbc.CardBody([
                    html.H5(children="Observatório de Políticas Publicas - TCMSP",
                    style={'color': colors['text']}
                    ),

            dbc.Row(style={'backgroundColor': colors['background']}, children=[

                dbc.Col([
                dbc.Button("Educação", id='btn-educacao', color="secondary",  n_clicks=0),
                dbc.Button("Saúde", id='btn-saude',  color="secondary", n_clicks=0, style={"margin-left": "5px"}),
                dbc.Button("Urbanismo", id='btn-urbanismo',  color="secondary", n_clicks=0, style={"margin-left": "5px"}),
                dbc.Button("Orçamento", id='btn-orcamento',  color="secondary", n_clicks=0, style={"margin-left": "5px"}),
                ]),
                #
                # dbc.Col([
                #     dbc.Button("Educação", id='btn-educacao', color="secondary", n_clicks=0, block=True, )
                # ], width=3),
                # dbc.Col([
                #     dbc.Button("Urbanismo", id='btn-urbanismo', color="secondary", n_clicks=0, block=True),
                # ], width=3),
                # dbc.Col([
                #     dbc.Button("Orçamento", id='btn-orcamento', color="secondary", n_clicks=0, block=True),
                # ], width=3),
                # dbc.Col([
                #     dbc.Button("Saúde", id='btn-saude', color="secondary", n_clicks=0, block=True),
                # ], width=3),

                # html.Div([
                #     html.Button('Educação', id='btn-educacao', style={'background-color': '#0099cc', 'color': 'white', 'width': '100px', "margin-left": "0px", 'height': '40px'}, n_clicks=0),
                #     html.Button('Saúde', id='btn-saude', style={'background-color': '#0099cc', 'color': 'white', 'width': '100px', "margin-left": "10px", 'height': '40px'},  n_clicks=0),
                #     html.Button('Urbanismo', id='btn-urbanismo', style={'background-color': '#0099cc', 'color': 'white', 'width': '100px', "margin-left": "10px", 'height': '40px'}, n_clicks=0),
                #     html.Button('Orçamento', id='btn-orcamento', style={'background-color': '#0099cc', 'color': 'white', 'width': '100px', "margin-left": "10px", 'height': '40px'},n_clicks=0),
                #     html.P(""),
                #     html.Div(id='drpindicadores')
                #         ]),
                    ]),

                        html.P(""),
                dbc.Row([
                dbc.Col([
                dbc.Collapse(
                    dcc.Dropdown(
                        id='dpEducacao',
                        options=dropdown_educacao,
                        value=[0],
                        multi=False,
                        placeholder='Escolha um indicador',
                        style={'backgroundColor': colors['background'], 'color': colors['text']}),
                    id="colEducacao", is_open=False),

                dbc.Collapse(
                    dcc.Dropdown(
                        id='dpSaude',
                        options=dropdown_saude,
                        value=[0],
                        multi=False,
                        placeholder='Escolha um indicador'),
                        style={'backgroundColor': colors['background'], 'color': colors['text']},
                    id="colSaude", is_open=False),

                dbc.Collapse(
                    dcc.Dropdown(
                        id='dpUurbanismo',
                        options=dropdown_urbanismo,
                        value=[0],
                        multi=False,
                        placeholder='Escolha um indicador'),
                        style={'backgroundColor': colors['background'], 'color': colors['text']},
                    id="colUrbanismo", is_open=False),

                dbc.Collapse(
                    dcc.Dropdown(
                        id='dpOrcamento',
                        options=dropdown_orcamento,
                        value=[0],
                        multi=False,
                        placeholder='Escolha um indicador'),
                        style={'backgroundColor': colors['background'], 'color': colors['text']},
                    id="colOrcamento", is_open=False),

], md=9),
            dbc.Col(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                info_ideb
            ], md=3),

]),
                        #html.Div(id='drpindicadores')

])
            ], color="dark", outline=True),

            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                    dbc.CardBody(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                        # html.Div([
                        #     html.Span(id="titulocardlinha"),
                        # ]),
                        html.Div(id="divGrafEsquerdaSup", children=[
                        dcc.Loading(id="Loading-2", type="default",
                                    children=[dcc.Graph(id="GrafEsquerdaSup"),])
                            ]),
                        html.Div(id="divGrafEsquerdaInf", children=[

                            dcc.Loading(id="Loading-3", type="default",
                                        children=[dcc.Graph(id="GrafEsquerdaInf"), ])
                        ]),

                    ])
                ], color="dark", outline=True)

                # dbc.Card([
                #     dbc.CardBody([
                #         html.Div(id="divGrafEsquerdaInf2", children=[
                #
                #         dash_table.DataTable(id="tabela",
                #             data=dft.to_dict('records'),
                #             columns=[{'id': c, 'name': c} for c in dft.columns]),
                #         ]),
                #
                #     ])
                # ], color="dark", outline=True)


                , id="colEsquerda", is_open=False),

            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                    dbc.CardBody([
                        html.H6("Distritos", className="card-title"),
                        html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, id="divTabelaDistrito", children=[
                                    dash_table.DataTable(id="tabela",
                                        data=dfTabelaDistrito.to_dict('records'),
                                        sort_action='native',
                                        style_table={'height': '350px', 'overflowY': 'auto'},
                                        style_header={'fontSize': 13, 'font-family': 'arial', 'fontWeight': 'bold'},
                                        style_cell={'backgroundColor': colors['table_cell'], 'color': colors['table_text'],
                                                    'textAlign': 'left', 'width': '85px', 'width': '85px', 'width': '85px',
                                                    'whiteSpace': 'normal', 'fontSize': 13, 'font-family': 'arial'},
                                        columns=[{'id': c, 'name': c} for c in dfTabelaDistrito.columns])

                        ]),

                    ])
                ], color="dark", outline=True)
                , id="colDistrito", is_open=False),

            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                    dbc.CardBody([
                        html.H6("Subprefeituras", className="card-title"),
                        html.Div(id="divTabelaSubprefeitura", children=[
                            dash_table.DataTable(id="tabelas",
                                                 data=dfTabelaSubprefeitura.to_dict('records'),
                                                 sort_action='native',
                                                 # page_size=10,
                                                 style_table={'height': '350px', 'overflowY': 'auto'},
                                                 style_header={'fontSize':13, 'font-family':'arial', 'fontWeight': 'bold'},
                                                 style_cell={'backgroundColor': colors['table_cell'], 'color': colors['table_text'],
                                                             'textAlign': 'left', 'width': '85px', 'width': '85px','width': '85px',
                                                             'whiteSpace': 'normal', 'fontSize':13, 'font-family':'arial'},
                                                 columns=[{'id': c, 'name': c} for c in dfTabelaSubprefeitura.columns])

                        ]),

                    ])
                ], color="dark", outline=True)
                , id="colSubprefeitura", is_open=False)

        ], width=5),
        dbc.Col(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                dbc.CardBody([

                    dbc.Row([
                        dbc.Col([

                            #html.Div(id="distsub"),
                            divdistritossubpreituras,

                            # dcc.RadioItems(
                            #     options=[
                            #         {'label': 'Distritos', 'value': 'optdistritos'},
                            #         {'label': 'Subprefeituras', 'value': 'optsubprefeituras'},
                            #     ],
                            #     value='optdistritos',
                            #     labelStyle={'display': 'inline-block', "margin-right": "20px"}
                            # ),

                        ]),
                        dbc.Col([

                            #html.Div(id="distanos"),
                            divdanos,
                            # dcc.RadioItems(
                            #     options=[
                            #         {'label': 'Anos iniciais', 'value': 'optanosiniciais'},
                            #         {'label': 'Anos Finais', 'value': 'optanosfinais'},
                            #     ],
                            #     value='optanosiniciais',
                            #     labelStyle={'display': 'inline-block', "margin-right": "20px"}
                            # ),
                        ]),
                    ]),

                    html.Div(id="divGrafDireita", children=[
                        dcc.Loading(id="Loading-1", type="default",
                                    children=[dcc.Graph(id="choropleth")])
                    ]),

                ])
                    ], color="dark", outline=True),
                    id = "colDireita", is_open = False),

            dbc.Collapse(

                dbc.Card(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
                    dbc.CardImg(src="./assets/mapa_transparente.png", top=True),
                    dbc.CardBody([
                        html.H3("Observatório de Políticas Públicas", className="card-title"),
                        html.H4("Tribunal de Contas do Município de São Paulo", className="card-title"),
                        html.H5("Escola Superior de Gestão e Contas Públicas", className="card-title"),
                        dbc.CardLink('Portal TCMSP',
                                 href="https://portal.tcm.sp.gov.br/", target="_blank"),
                        html.P(""),
                        dbc.CardLink('Dados Abertos do Inep.',
                                 href="https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados", target="_blank"),

                    ])
                ], color="dark", outline=True)
                , id="colApresentacaoDireita", is_open=True),

], width=7)
], no_gutters=False)
])



#####################################################################
#Botões
#####################################################################
@app.callback(
              Output('colEducacao', 'is_open'),
              Output('colSaude', 'is_open'),
              Output('colUrbanismo', 'is_open'),
              Output('colOrcamento', 'is_open'),
             [Input('btn-educacao', 'n_clicks'),
              Input('btn-saude', 'n_clicks'),
              Input('btn-urbanismo', 'n_clicks'),
              Input('btn-orcamento', 'n_clicks')])

def displayClick(btn1, btn2, btn3, btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    m_dropdown_educacao = False
    m_dropdown_saude =  False
    m_dropdown_urbanismo =  False
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

    return (m_dropdown_educacao, m_dropdown_saude,m_dropdown_urbanismo, m_dropdown_orcamento)


# #####################################################################
# #Botões
# #####################################################################
# @app.callback(Output('dropdown-educacao', 'children'),
#               Output('collapse_educacao', 'is_open'),
#               Input('btn-educacao', 'n_clicks'),
#               Input('btn-saude', 'n_clicks'),
#               Input('btn-urbanismo', 'n_clicks'),
#               Input('btn-orcamento', 'n_clicks'))
#
# def displayClick(btn1, btn2, btn3, btn4):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'btn-educacao' in changed_id:
#         msg =  dcc.Dropdown(
#                 id='dropdown_educacao',
#                 options=[{'label' : 'Ideb', 'value' : 'ideb'},
#                          {'label' : 'Universalização', 'value' : 'unversalizacao'},
#                          {'label' : 'Idep', 'value' : 'idep'},
#                          {'label' : 'Taxa de Abandono', 'value' : 'abandono'},
#                          {'label' : 'EJA', 'value' : 'eja'}],
#                          placeholder='Escolha um indicador'), html.Div(id='dropdown-ideb')
#
#
#     elif 'btn-saude' in changed_id:
#         msg = dcc.Dropdown(
#                 id='dropdown-saude',
#                 options=[{'label' : 'Saúde 1', 'value' : 'saude1'},
#                          {'label' : 'Saúde 3', 'value' : 'saude2'},
#                          {'label' : 'Saúde 3', 'value' : 'saude3'}],
#                          placeholder='Escolha um indicador')
#     elif 'btn-urbanismo' in changed_id:
#         msg = dcc.Dropdown(
#                 id='dropdown-urbanismo',
#                 options=[{'label' : 'Urbanismo 1', 'value' : 'urbanismo1'},
#                          {'label' : 'Urbanismo 3', 'value' : 'urbanismo2'},
#                          {'label' : 'Urbanismo 3', 'value' : 'urbanismo3'}],
#                          placeholder='Escolha um indicador')
#     elif 'btn-orcamento' in changed_id:
#         msg =  dcc.Dropdown(
#                 id='dropdown-orcamento',
#                 options=[{'label' : 'Orçamento 1', 'value' : 'orcamento1'},
#                          {'label' : 'Orçamento 3', 'value' : 'orcamento2'},
#                          {'label' : 'Orçamento 3', 'value' : 'orcamento3'}],
#                          placeholder='Escolha um indicador')
#     else:
#         msg = ''
#
#     return html.Div(msg)

#####################################################################
#MAPA
#####################################################################
@app.callback(Output("choropleth", "figure"),
              Output("GrafEsquerdaSup", "figure"),
              Output("GrafEsquerdaInf", "figure"),
              Output("collapsedivdanos", "is_open"),
              Output("colapseddivistritossubpreituras", "is_open"),
              Output('divGrafEsquerdaSup', 'style'),
              Output('divGrafEsquerdaInf', 'style'),
              Output('divGrafDireita', 'style'),
              Output("info_body", "children"),
              Output("divInfo", "style"),
              Output("info_header", "children"),
              Output("colEsquerda", "is_open"),
              Output("colDireita", "is_open"),
              Output("colApresentacaoDireita", "is_open"),
              Output("colDistrito", "is_open"),
              Output("colSubprefeitura", "is_open"),
              Input("dpEducacao", "value"),
              Input("optdados", "value"),
              Input("optanos", "value")
            )



def displayMapa(indicadores, dados, anos):
    user_click = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    card_anos = False
    card_distritos = False
    card_Esquerda = False
    card_Direita = False
    card_Distrito = False
    card_Subprefeitura = False
    card_Apresentacao_Direita = True
    fig = go.Figure()
    fig2 = go.Figure()
    fig3 = go.Figure()
    divEsquerdaSup = {"display": "none"}
    divEsquerdaInf = {"display": "none"}
    divGrafDireita  = {"display": "none"}
    divInfo  = {"display": "none"}
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

    if indicadores is not None:
        if indicadores =="ideb":
            #Cria mapa e gráfico de linhas
            fig = gerar_mapa("mapa", anos, dados)

            card_anos = True
            card_distritos = True
            card_Direita = True
            card_Esquerda = True
            card_Apresentacao_Direita = False
            divGrafDireita = {"display": "block"}
            #divEsquerdaSup = {"display": "block"}
            divInfo = {"display": "block"}
            info = info_ideb
            info_header = "Indicador - IDEB"

            if dados is not None:
                if dados == "distrito":
                    card_Distrito = True
                else:
                    card_Subprefeitura = True

        else:
            if indicadores == "idepiniciais":
                labels = ['Faixa 1', 'Faixa 2', 'Faixa 3', 'Faixa 4','Faixa 5','Faixa 6']
                values = [17 ,13 ,45 ,21 ,3 ,1 ]

                fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
                fig2.update_layout(margin=dict(l=0, r=0, t=50, b=0), autosize=True,  title="Percentual de escolas por faixa do IDEP <br> Anos Iniciais (2019)")

                dfBarra = pd.read_excel("data/idep_barras_iniciais.xlsx")
                fig = px.bar(dfBarra, y="Distrito", x=["Faixa 1","Faixa 2","Faixa 3","Faixa 4","Faixa 5","Faixa 6"], orientation='h', title="Distribuição das escolas por faixa do Idep por Distrito (2019)", height=1200)


                labels = ['Não Atingiram', 'Atingiram']
                values = [15.50 ,84.50]

                fig3 = go.Figure(data=[go.Pie(labels=labels, values=values)])
                fig3.update_layout(margin=dict(l=0, r=0, t=50, b=0), autosize=True, showlegend=True, title="Escolas que atingiram a meta do IDEP <br> Anos Finais para 2019")

                divEsquerdaSup = {"display": "block"}
                divEsquerdaInf = {"display": "block"}
                divGrafDireita = {"display": "block"}
                divInfo = {"display": "block"}
                info = info_idep
                info_header = "Indicador - IDEP"
                card_Esquerda = True
                card_Direita = True
                card_Apresentacao_Direita = False

            else:
                if indicadores == "abandono":
                    df = pd.read_excel("data/evasao_linha.xlsx")

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
                    fig2.update_traces(marker_line_width=2, marker_size=3)
                    fig2.update_layout(margin=dict(l=0, r=0, t=50, b=0), autosize=True,
                                       title="Taxa de abandono Ensino Fundamental")
                    fig2.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='black')
                    fig2.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='black')

                    divEsquerdaSup = {"display": "block"}
                    divEsquerdaInf = {"display": "none"}
                    divGrafDireita = {"display": "block"}
                    divInfo = {"display": "block"}
                    card_Esquerda = True
                    card_Direita = True
                    card_Apresentacao_Direita = False

                    df = pd.read_excel("data/evasao_barra.xlsx")
                    df['taxa'] = pd.to_numeric(df['taxa'], errors='coerce')
                    df = df.sort_values("taxa")
                    fig = px.bar(df, y="Distrito", x="taxa",
                                 orientation='h',
                                 title="Taxa de abandono no Ensino Fundamental(%)")

                    info = "abandono"
                    info_header = "Indicador - Taxa de Abandono"




    else: #indicadores não escolhidos
        return (go.Figure(), go.Figure(), go.Figure(), card_distritos, card_anos, divEsquerdaSup, divEsquerdaInf, divGrafDireita, info, divInfo, info_header, card_Esquerda, card_Direita, card_Apresentacao_Direita, card_Distrito, card_Subprefeitura)


    return (fig, fig2, fig3, card_distritos, card_anos, divEsquerdaSup, divEsquerdaInf, divGrafDireita, info, divInfo, info_header, card_Esquerda, card_Direita, card_Apresentacao_Direita, card_Distrito, card_Subprefeitura)




#####################################################################
#MAPA - Distritos e Anos (Radio buttom)
#####################################################################
# @app.callback(Output("choropleth", "figure"),
#               Input("optanos", "value"),
#               Input("optdados", "value"))
#
#
# def displayMapaOpt(indicadores):
#     if indicadores is not None:
#         fig = gerar_mapa("mapa", "ideb_iniciais", "distrito")
#     else:
#         return (go.Figure())
#
#
#     return (fig)

# @app.callback(
# )

# @app.callback(
#     [Output("choropleth", "figure"),
#     Output("textototal", "children")],
#     [Input("submit", "n_clicks"),
#      State("anos_ideb", "value"),
#      State("indicadores", "value"),
#      State("dados", "value"),]
# )

# def display_choropleth(n_clicks, anos_ideb, tipografico, dados):
#     if n_clicks is not None and n_clicks != 0:
#         fig, txtTotais = gerar_mapa(tipografico, anos_ideb, dados)
#         return (fig, txtTotais)
#     else:
#         return (go.Figure(), "")
#
#
#
# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open



def toggle_modal(n1, n2, is_open):
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