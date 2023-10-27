
# Crear una aplicación Dash
import dash
from dash import dcc, html, callback
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
from scipy import stats
import plotly.express as px

# Cargar los datos desde el archivo 'Data.xlsx'
df = pd.read_excel('Data.xlsx')

# Crear una aplicación Dash
dash.register_page(__name__, name='RegresionLineal X PE',suppress_callback_exceptions=True)


# Obtener la lista de estados únicos
estados = df['ENTIDAD_FEDERATIVA'].unique()

# Obtener la lista de programas de estudio únicos
programas_de_estudio = df['PROGRAMADEESTUDIOS'].unique()

# Obtener la lista de variables dependientes únicas
variables_dependientes = df.columns[5:-1]  # Seleccionar las columnas de la 6ª a la penúltima (variables numéricas)

# Diseño de la aplicación
layout = html.Div([
    html.H1("Análisis de Regresión de Mínimos Cuadrados - Comportamiento histórico de una carrera"),
    html.Label("Selecciona un estado:"),
    dcc.Dropdown(
        id='estado-dropdown',
        options=[{'label': estado, 'value': estado} for estado in estados],
        value=estados[0]  # Valor predeterminado
    ),
    html.Label("Selecciona una institución de educación superior:"),
    dcc.Dropdown(
        id='institucion-dropdown',
        value=None
    ),
    html.Label("Selecciona un programa de estudio:"),
    dcc.Dropdown(
        id='programa-dropdown',
        value=None
    ),
    html.Label("Selecciona una variable dependiente:"),
    dcc.Dropdown(
        id='variable-dependiente-dropdown',
        options=[{'label': var, 'value': var} for var in variables_dependientes],
        value=variables_dependientes[0]  # Valor predeterminado
    ),
    dcc.Graph(id='regression-plot'),
    html.Div(id='regression-text', style={'background-color': 'white'})  # Modificado
])

# Callback para actualizar las opciones del dropdown de institución en función del estado seleccionado
@callback(
    Output('institucion-dropdown', 'options'),
    Input('estado-dropdown', 'value')
)
def update_institucion_options(selected_estado):
    if selected_estado is None:
        return []

    # Filtrar las instituciones únicas en función del estado seleccionado
    instituciones = df[df['ENTIDAD_FEDERATIVA'] == selected_estado]['INSTITUCION_DE_EDUCACION_SUPERIOR'].unique()
    options = [{'label': institucion, 'value': institucion} for institucion in instituciones]

    return options

# Callback para actualizar las opciones del dropdown de programa de estudio en función del estado e institución seleccionados
@callback(
    Output('programa-dropdown', 'options'),
    [Input('estado-dropdown', 'value'), Input('institucion-dropdown', 'value')]
)
def update_programa_options(selected_estado, selected_institucion):
    if selected_estado is None or selected_institucion is None:
        return []

    # Filtrar los programas de estudio únicos en función del estado e institución seleccionados
    programas = df[(df['ENTIDAD_FEDERATIVA'] == selected_estado) & (df['INSTITUCION_DE_EDUCACION_SUPERIOR'] == selected_institucion)]['PROGRAMADEESTUDIOS'].unique()
    options = [{'label': programa, 'value': programa} for programa in programas]

    return options

# Callback para realizar la regresión y actualizar el gráfico
@callback(
    [Output('regression-plot', 'figure'), Output('regression-text', 'children')],
    [Input('estado-dropdown', 'value'), Input('institucion-dropdown', 'value'), Input('programa-dropdown', 'value'),
     Input('variable-dependiente-dropdown', 'value')]
)
def update_regression_plot(selected_estado, selected_institucion, selected_programa, selected_variable_dependiente):
    if selected_estado is None or selected_institucion is None or selected_programa is None or selected_variable_dependiente is None:
        # Si alguno de los valores no está seleccionado, no hay datos para mostrar
        empty_fig = px.scatter(title="No hay datos para mostrar")
        return empty_fig, ''

    # Filtrar los datos para el estado, institución, programa de estudio y variable dependiente seleccionados
    datos_filtrados = df[(df['ENTIDAD_FEDERATIVA'] == selected_estado) &
                         (df['INSTITUCION_DE_EDUCACION_SUPERIOR'] == selected_institucion) &
                         (df['PROGRAMADEESTUDIOS'] == selected_programa)]

    if len(datos_filtrados) == 0:
        empty_fig = px.scatter(title=f"No hay datos para mostrar para el estado: {selected_estado}, la institución: {selected_institucion}, el programa: {selected_programa} y la variable: {selected_variable_dependiente}")
        return empty_fig, ''

    # Variables independiente (Año) y dependiente (seleccionada por el usuario)
    x = datos_filtrados['Año']
    y = datos_filtrados[selected_variable_dependiente]

    # Realizar la regresión de mínimos cuadrados
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Calcular la línea de regresión
    linea_regresion = slope * x + intercept

    # Crear un gráfico interactivo con Plotly Express
    fig = px.scatter(datos_filtrados, x='Año', y=selected_variable_dependiente,
                     title=f'Regresión para el Estado "{selected_estado}" - Institución: {selected_institucion} - Programa de Estudio: {selected_programa} - Variable: {selected_variable_dependiente}')
    fig.add_trace(px.line(x=x, y=linea_regresion, labels={'y': 'Línea de Regresión'}).data[0])

    # Personalizar la gráfica
    fig.update_traces(mode='lines+markers', line=dict(color='red', width=2))  # Cambiar el color a rojo
    fig.update_layout(title_text=f'Regresión para el Estado "{selected_estado}" - Institución: {selected_institucion} - Programa de Estudio: {selected_programa} - Variable: {selected_variable_dependiente}',
                      xaxis_title='Año',
                      yaxis_title=selected_variable_dependiente,
                      showlegend=True)

    # Coeficiente de correlación (R-squared) y valor p
    r_squared = r_value ** 2
    regression_text = [
        html.H2("Análisis de Regresión de Mínimos Cuadrados:", style={'background-color': 'white'}),  # Modificado
        html.P(f"La pendiente de la regresión es {slope:.2f}, lo que indica la tendencia histórica.", style={'background-color': 'white'}),  # Modificado
        html.P(f"El coeficiente de correlación (R-squared) es {r_squared:.2f}, lo que sugiere la fuerza de la relación.", style={'background-color': 'white'}),  # Modificado
        html.P(f"El valor p es {p_value:.4f}, lo que indica si la relación es estadísticamente significativa.", style={'background-color': 'white'})  # Modificado
    ]

    return fig, regression_text
