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
            dbc.Card(dbc.CardBody('''Aqui vem um texto explicativo sobre o dashboard.
                                    Falando sobre o que é o IDEB e outras cositas mais.
                                    Que eu vou pedir pra você escrever pra mim porque o que eu gosto mesmo é codar.''')),
            id="collapse",
            is_open=False,
        ),
    ]
)