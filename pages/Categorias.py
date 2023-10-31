import pandas as pd
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px  # Importa plotly.express

# Carga el archivo "Data.xlsx" en un DataFrame
df = pd.read_excel("Data.xlsx")

# Obtiene la lista de años únicos en el DataFrame
años_disponibles = df['Año'].unique()

dash.register_page(__name__, name='Categorias')

# Layout del tablero
layout = html.Div([
    html.H1("Conteo de Categorías", style={'text-align': 'center'}),
    # Dropdown para seleccionar la columna a visualizar
    html.Label("Categorias"),  # Título para el Dropdown de Categorias

    dcc.Dropdown(
        id='column-selector',
        options=[
            {'label': 'Clasificación', 'value': 'Clasificación'},
            {'label': 'Carrera_Areas', 'value': 'Carrera_Areas'}
        ],
        value='Clasificación',  # Valor predeterminado
        style={'width': '50%'},
        className="custom-dropdown"

    ),
    

    # Dropdown para seleccionar el año
        html.Div(style={'height': '20px'}),  # Espacio vertical entre los Dropdowns

    html.Label("Año"),  # Título para el Dropdown de Categorias


    dcc.Dropdown(

        id='year-selector',
        options=[{'label': año, 'value': año} for año in años_disponibles],
        value=años_disponibles[0],  # Valor predeterminado
        style={'width': '50%'},
                className="custom-dropdown"


    ),

    # Gráfico de barras
    dcc.Graph(id='bar-chart'),

    # Gráfico de Dona
    dcc.Graph(id='donut-chart')  # Agrega un nuevo componente para el Gráfico de Dona
])

# Callback para actualizar el gráfico de barras según la columna seleccionada y el año
@callback(
    Output('bar-chart', 'figure'),
    Input('column-selector', 'value'),
    Input('year-selector', 'value')
)
def update_bar_chart(selected_column, selected_year):
    # Filtra el DataFrame según el año seleccionado
    df_filtered = df[df['Año'] == selected_year]

    # Obtén el conteo de categorías únicas en la columna seleccionada
    count_data = df_filtered[selected_column].value_counts().reset_index()
    count_data.columns = [selected_column, 'Cantidad']

    # Crea un gráfico de barras personalizado
    figure = go.Figure()
    figure.add_trace(go.Bar(
        x=count_data[selected_column],
        y=count_data['Cantidad'],
        text=count_data['Cantidad'],
        textposition='outside',
        marker=dict(color='royalblue')
    ))

    figure.update_layout(
        title=f'Conteo de Categorías en la columna "{selected_column}" - Año {selected_year}',
        xaxis=dict(title=selected_column),
        yaxis=dict(title='Cantidad'),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Arial, sans-serif', size=12, color='black'),
        margin=dict(l=50, r=30, b=50, t=80)
    )

    return figure

# Callback para actualizar el gráfico de dona según la columna seleccionada y el año
@callback(
    Output('donut-chart', 'figure'),
    Input('column-selector', 'value'),
    Input('year-selector', 'value')
)
def update_donut_chart(selected_column, selected_year):
    # Filtra el DataFrame según el año seleccionado
    df_filtered = df[df['Año'] == selected_year]

    # Obtén el conteo de categorías únicas en la columna seleccionada
    count_data = df_filtered[selected_column].value_counts().reset_index()
    count_data.columns = [selected_column, 'Cantidad']

    # Crea un gráfico de dona con plotly.express
    fig = px.pie(count_data, names=selected_column, values='Cantidad', title=f'Distribución de {selected_column} - Año {selected_year}')
    
    return fig


