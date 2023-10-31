import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash.register_page(__name__, name='Eliminación')

# Carga el archivo Excel en un DataFrame
df = pd.read_excel('Data.xlsx')

def create_figure():
    figure = {
        'data': [{'x': df['Año'].value_counts().index, 'y': df['Año'].value_counts().values, 'type': 'bar'}],
        'layout': {
            'title': 'Número de Filas por Año'
        }
    }
    return figure

layout = html.Div([
    html.H1("Eliminar Filas por Año"),
    html.Label("Seleccione un año:"),
    dcc.Dropdown(
        id='dropdown-year',
        options=[{'label': year, 'value': year} for year in df['Año'].unique()],
        value=df['Año'].min()
    ),
    html.Br(),
    html.Button("Eliminar Filas", id="delete-button"),
    html.Br(),
    dcc.Graph(id='output-graph'),
    dbc.Alert(id='confirmation-alert', is_open=False)
])

@callback(
    Output('output-graph', 'figure'),
    Output('confirmation-alert', 'is_open'),
    Input('delete-button', 'n_clicks'),
    Input('dropdown-year', 'value')
)
def delete_rows(n_clicks, selected_year):
    if n_clicks is None:
        return create_figure(), False

    global df
    original_length = len(df)
    df = df[df['Año'] != selected_year]

    df.to_excel('Data.xlsx', index=False)

    confirmation_message = f'Filas eliminadas para el año {selected_year}'

    return create_figure(), True

