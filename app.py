import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.MORPH])
server = app.server

# Ejemplo de mejoras en el estilo del Sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#343a40",  # Cambia el color de fondo
    "color": "white",  # Cambia el color de fuente
    "transition": "all 0.5s",  # Agrega una transición suave
}

# Agrega la pestaña "Administrador"
pages = list(dash.page_registry.values())
administrador_page = {
    "name": "Administrador",
    "path": "/administrador"
}

# Agrega la pestaña "Eliminación" al sidebar
eliminacion_page = {
    "name": "Eliminación",
    "path": "/eliminacion"
}

sidebar = html.Div(
    [
        html.H2("Menú", className="display-4", style={'color': 'white'}),
        html.Hr(),
        html.P(
            "Barra de navegación", className="lead"
        ),

        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in pages  # Utiliza la lista de páginas
                if page["path"] != "/eliminacion"  # Excluye la página "/eliminacion" del navbar
            ],
            vertical=True,
            pills=True,
            className="bg-light",
        ),

        # Agrega el título "Administrador"
        html.H2("Administrador", style={'fontSize': 20, 'textAlign': 'center', 'font': 'white'}),
        # Agrega la pestaña "Eliminación" debajo de "Administrador"
        dbc.NavLink(
            "Eliminación",
            href="/eliminacion",
            active="exact",
            style={'fontSize': 14, 'textAlign': 'center'},
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Sistema de Evaluación Estadística de Educación Superior Computacional",
                         style={'fontSize': 20, 'textAlign': 'center', 'font': 'red'})
        )
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2
            ),
            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=8, lg=10, xl=10, xxl=10
            ),
        ]
    )

], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)

