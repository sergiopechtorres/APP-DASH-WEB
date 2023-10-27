import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Cargar los datos desde el archivo Excel
data = pd.read_excel("Data.xlsx")

# Crear una aplicación Dash
app = dash.Dash(__name__)

# Diseño del dashboard
app.layout = html.Div([
    html.H1("Análisis de Datos"),
    
    # Menú desplegable para seleccionar un año
    dcc.Dropdown(
        id="dropdown-ano",
        options=[
            {"label": str(ano), "value": ano} for ano in data["Año"].unique()
        ],
        value=data["Año"].max(),
        multi=False
    ),
    
    # Gráfico de barras horizontal para la distribución de ENTIDAD_FEDERATIVA
    dcc.Graph(id="entidad-federativa-bar"),
    
    # Gráfico de barras horizontal para la distribución de MUNICIPIO
    dcc.Graph(id="municipio-bar"),
    
    # Gráfico de barras apiladas para la distribución de CLASIFICACIÓN
    dcc.Graph(id="clasificacion-bar"),
    
    # Gráfico de barras apiladas para la distribución de Carrera_Areas
    dcc.Graph(id="carrera-areas-bar"),
    
    # Gráfico de línea para la evolución de AÑO
    dcc.Graph(id="ano-line"),
    
    # Gráfico de dispersión para AÑO vs. Carrera_Areas
    dcc.Graph(id="scatter-ano-carrera"),
    
    # Gráfico de pastel para la distribución de Clasificación
    dcc.Graph(id="clasificacion-pie"),
])

# Callbacks para actualizar los gráficos
@app.callback(
    Output("entidad-federativa-bar", "figure"),
    Output("municipio-bar", "figure"),
    Output("clasificacion-bar", "figure"),
    Output("carrera-areas-bar", "figure"),
    Output("ano-line", "figure"),
    Output("scatter-ano-carrera", "figure"),
    Output("clasificacion-pie", "figure"),
    Input("dropdown-ano", "value")
)
def update_figures(selected_year):
    filtered_data = data[data["Año"] == selected_year]
    
    # Gráfico de barras horizontal para la distribución de ENTIDAD_FEDERATIVA
    entidad_federativa_fig = px.bar(
        filtered_data, x="ENTIDAD_FEDERATIVA", title="Distribución de ENTIDAD_FEDERATIVA",
        labels={"ENTIDAD_FEDERATIVA": "Entidad Federativa"}
    )
    
    # Gráfico de barras horizontal para la distribución de MUNICIPIO
    municipio_fig = px.bar(
        filtered_data, x="MUNICIPIO", title="Distribución de MUNICIPIO",
        labels={"MUNICIPIO": "Municipio"}
    )
    
    # Gráfico de barras apiladas para la distribución de CLASIFICACIÓN
    clasificacion_fig = px.bar(
        filtered_data, x="Clasificación", title="Distribución de CLASIFICACIÓN"
    )
    
    # Gráfico de barras apiladas para la distribución de Carrera_Areas
    carrera_areas_fig = px.bar(
        filtered_data, x="Carrera_Areas", title="Distribución de Carrera_Areas"
    )
    
    # Gráfico de línea para la evolución de AÑO
    ano_line_fig = px.line(
        data, x="Año", y="Matrícula_Total", title="Evolución de Matrícula Total por Año",
        labels={"Año": "Año", "Matrícula_Total": "Matrícula Total"}
    )
    
    # Gráfico de dispersión para AÑO vs. Carrera_Areas
    scatter_ano_carrera_fig = px.scatter(
        filtered_data, x="Año", y="Carrera_Areas", title="Dispersión de AÑO vs. Carrera_Areas",
        labels={"Año": "Año", "Carrera_Areas": "Área de Carrera"}
    )
    
    # Gráfico de pastel para la distribución de Clasificación
    clasificacion_pie_fig = px.pie(
        data, names="Clasificación", title="Distribución de Clasificación"
    )
    
    return entidad_federativa_fig, municipio_fig, clasificacion_fig, carrera_areas_fig, ano_line_fig, scatter_ano_carrera_fig, clasificacion_pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)
