import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Ejemplo de Dropdown con Estilo Azul #378DFC"),
    
    dcc.Dropdown(
        options=[
            {'label': 'Opción 1', 'value': 'option-1'},
            {'label': 'Opción 2', 'value': 'option-2'},
            {'label': 'Opción 3', 'value': 'option-3'}
        ],
        value='option-1',
        style={
            'width': '100%',
            'padding': '12px',
            'border': '2px solid #378DFC',
            'border-radius': '6px',
            'background-color': '#fff',
            'color': '#333',
            'font-size': '16px',
            'transition': 'border-color 0.3s, box-shadow 0.3s'
        }
    ),
    
    html.P("Este es un Dropdown con estilo azul #378DFC.")
])

if __name__ == "__main__":
    app.run_server(debug=True)
