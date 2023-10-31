import dash
from dash import dcc, html,callback
import pandas as pd
import plotly.graph_objs as go

# Cargar los datos desde un archivo Excel
df = pd.read_excel("Data.xlsx")

# Obtener las opciones únicas de Clasificación y Carrera_Areas
clasificacion_options = [{'label': clasif, 'value': clasif} for clasif in df['Clasificación'].unique()]
carrera_areas_options = [{'label': area, 'value': area} for area in df['Carrera_Areas'].unique()]

# Inicializar la aplicación Dash
dash.register_page(__name__, name='Categorias X Matricula')

# Diseño de la aplicación
layout = html.Div([
    html.H1("Matrícula Total por Año, Clasificación y Carrera Áreas"),
    
    # Dropdown para seleccionar Clasificación
    html.Label("Selecciona la Clasificación:"),
    dcc.Dropdown(
        id="clasificacion-dropdown",
        options=clasificacion_options,
        value=clasificacion_options[0]['value']
    ),
    
    # Dropdown para seleccionar Carrera Áreas
    html.Label("Selecciona la Carrera Áreas:"),
    dcc.Dropdown(
        id="carrera-areas-dropdown",
        options=carrera_areas_options,
        value=carrera_areas_options[0]['value']
    ),
    
    dcc.Graph(id="matricula-bar-chart"),
])

# Callback para actualizar el gráfico en función de las selecciones
@callback(
    dash.dependencies.Output("matricula-bar-chart", "figure"),
    dash.dependencies.Input("clasificacion-dropdown", "value"),
    dash.dependencies.Input("carrera-areas-dropdown", "value")
)
def update_bar_chart(selected_clasificacion, selected_carrera_areas):
    filtered_df = df[(df['Clasificación'] == selected_clasificacion) & (df['Carrera_Areas'] == selected_carrera_areas)]
    total_matriculados = filtered_df.groupby('Año')['Matrícula_Total'].sum()
    
    fig = go.Figure(data=[
        go.Bar(x=total_matriculados.index, y=total_matriculados.values, text=total_matriculados.values, textposition='auto')
    ])
    
    fig.update_layout(title=f'Matrícula Total para {selected_clasificacion} - {selected_carrera_areas}',
                      xaxis_title='Año', yaxis_title='Matrícula Total')
    
    return fig



