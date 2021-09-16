import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Observatório de Políticas Públicas", href="https://portal.tcm.sp.gov.br/Pagina/28207")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Nossos Portais", header=True),
                dbc.DropdownMenuItem("Portal TCM", href="https://portal.tcm.sp.gov.br/"),
                dbc.DropdownMenuItem("Código aberto", href="https://github.com/h-pgy/app_tcm_ideb"),
            ],
            nav=True,
            in_navbar=True,
            label="Mais",
        ),
    ],
    brand="Tribunal de Contas do Município de São Paulo",
    color="white",
    dark=False,
)


collapse = html.Div(
    [
        dbc.Button(
            "Sobre os dados:",
            id="collapse-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                    html.P( 
                     children=[
                    '''Os dados acima refletem o ano de 2019 e
                     foram extraídos dos indicadores educacionais do Inep, 
                     disponíveis no portal ''',
                     dcc.Link('Dados Abertos do Inep.', href = "https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados"),
                     ]),
                    html.P(children = ['''Foram extraídos os resultados por escolas da rede municipal de São Paulo
                     e então foi feita a média desses dados por Distrito da cidade de São Paulo.
                      Esses dados estão divididos entre Anos Iniciais e Anos Finais refletindo a forma 
                      como são apresentados no Inep, sendo anos iniciais do 1º ao 4º ano e anos finais do
                       5º ao 9º ano do Ensino fundamental.  Esses dados foram cruzados com os dados das 
                       unidades educacionais da rede Municipal de Ensino de São Paulo disponíveis no ''',
                       dcc.Link("Portal de Dados Abertos da Prefeitura Municipal de São Paulo.", href= "http://dados.prefeitura.sp.gov.br/dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas")
                    ]),
                    html.P('''A partir desse cruzamento foi feita a média do Ideb por Distrito mostrada na figura. Alguns distritos não apresentam Ideb, pois não possuem escolas de Ensino Fundamental da Rede Municipal de Educação  (os alunos destes distritos frequentam escolas estaduais ou escolas em outros distritos.'''),
            ],
            ),
            ),
        id="collapse",
        is_open=False
        ),
    ],
)