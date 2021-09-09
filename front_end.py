import dash_html_components as html
import dash_bootstrap_components as dbc


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
            dbc.Card(dbc.CardBody('''O mapa de calor acima permite uma visualização da média do Ideb por Distrito da cidade de São Paulo.\n
            Os dados do Ideb foram retirados diretamente do Inep e, a partir dele, calculamos uma média do Ideb das escolas de cada distrito para se chegar à média por Distrito.\n
            Essa forma de visualizar as informações permite uma análise regionalizada desse indicador de aprendizagem.\n
            O Ideb é um indicador de nível de aprendizagem usado no Ensino Fundamental, mas deve ser analisado levando-se em conta outros fatores como o Inse.\n
            Para que tenhamos uma visão mais abrangente também vamos incluir em nossa plataforma e em nossas análises outros indicadores de aprendizagem que englobam características da comunidade e da escola como o Idep.''')),
            id="collapse",
            is_open=False,
        ),
    ]
)