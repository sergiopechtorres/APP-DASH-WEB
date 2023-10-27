import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__, path='/',name='Home')

df = px.data.gapminder()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

layout = html.Div(
    [
        
       
    ],style={'background-image': 'url("/assets/fondo.png")'},
    
)
