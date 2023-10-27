import dash
from dash import dash_table as dt
import plotly.graph_objs as go
import plotly.express as px
from dash import html, dcc, Input, Output, callback
import pandas as pd

# Crear la aplicación Dash

dash.register_page(__name__, name='Municipio')
title = 'Municipio'

# Cargar tus datos desde un archivo (asegúrate de tener un archivo 'Data.xlsx' en el mismo directorio)
df = pd.read_excel('Data.xlsx')

# Agrega un Dropdown para seleccionar el año
layout = html.Div([
    html.Div([
        html.H1('ANUIES DASH'),
        html.Img(src='assets/municipios.png')
    ], className='banner'),

    html.Div([
        html.Div([
            html.Div([
                html.H3('Estados de México', style={
                    'margin-bottom': '8px', 'color': 'black'}),
            ])
        ], className='create_container1 four columns', id="title"),
    ], id="header", className="row flex-display", style={'margin-bottom': "25px"}),

    # Drop down list (Estado) para mostrar sus municipios correspondientes
    html.Div([
        html.Div([
            html.P('Selecciona el estado', className='fix_label',
                   style={'color': 'black', 'text-align': 'center'}),
            dcc.Dropdown(
                id='select_estados',
                multi=False,
                clearable=True,
                disabled=False,
                style={'display': True},
                value='AGUASCALIENTES',
                placeholder='Selecciona Estado',
                options=[{'label': c, 'value': c}
                         for c in df['ENTIDAD_FEDERATIVA'].unique()],
                className="dcc_compon"
            ),

            # Agrega un Dropdown para seleccionar el año
            html.P('Selecciona el año', className='fix_label',
                   style={'color': 'black', 'text-align': 'center'}),
            dcc.Dropdown(
                id='select_anio',
                multi=False,
                clearable=True,
                disabled=False,
                style={'display': True},
                value=2022,  # Ajusta esto según tus años reales en el DataFrame
                placeholder='Selecciona Año',
                options=[{'label': anio, 'value': anio}
                         for anio in df['Año'].unique()],
                className="dcc_compon"
            )
        ], className='create_container1 four columns', style={'margin-bottom': '8px'})
    ], className="row flex-display"),

    # Data Table
    html.Div([
        html.Div([
            dt.DataTable(
                id='my_datatable',
                columns=[{'name': c, 'id': c} for c in df.columns],
                page_current=0,
                page_size=10,
                page_action='custom',
            ),
        ], className='create_container2 thirteen columns'),
    ], className='row flex-display'),

    # Gráfico de Barras con la Suma de Variables por Municipio
    html.Div([
        html.Br(),
        dcc.Graph(id='bar_chartM',
                  config={'displayModeBar': 'hover'})
    ], className='create_container2 thirteen columns'),

    # Gráfico Lineal con la Suma de Variables por Municipio
    html.Div([
        html.Br(),
        dcc.Graph(id='line_chartM',
                  config={'displayModeBar': 'hover'})
    ], className='create_container2 thirteen columns'),

    # Crear los gráficos de pastel en grupos de dos
    html.Div([
        # Primera fila de gráficos de pastel
        html.Div([
            html.Br(),
            dcc.Graph(id='pie_chartM', config={'displayModeBar': 'hover'}),
                        html.Br(),

            dcc.Graph(id='pie_chartM1', config={'displayModeBar': 'hover'}),
        ],className='create_containes seven columns'),
        html.Br(),

        # Segunda fila de gráficos de pastel
        html.Div([
            html.Br(),
            dcc.Graph(id='pie_chartM2', config={'displayModeBar': 'hover'}),
                        html.Br(),

            dcc.Graph(id='pie_chartM3', config={'displayModeBar': 'hover'}),
        ], className='create_container six columns'),

        # Tercera fila de gráficos de pastel
        html.Div([
            html.Br(),
            dcc.Graph(id='pie_chartM4', config={'displayModeBar': 'hover'}),
                        html.Br(),

            dcc.Graph(id='pie_chartM5', config={'displayModeBar': 'hover'}),
        ], className='create_container five columns'),
    ], className='row flex-display'),

])

# Actualiza tus callbacks para incluir el año seleccionado
@callback(
    [Output('my_datatable', 'data'),
     Output('bar_chartM', 'figure'),
     Output('line_chartM', 'figure'),
     Output('pie_chartM', 'figure'),
     Output('pie_chartM1', 'figure'),
     Output('pie_chartM2', 'figure'),
     Output('pie_chartM3', 'figure'),
     Output('pie_chartM4', 'figure'),
     Output('pie_chartM5', 'figure')],
    [Input('select_estados', 'value'), Input('select_anio', 'value')]
)
def update_data(select_estados, select_anio):
    # Filtra los datos según el estado y el año seleccionados
    filtered_data = df[(df['ENTIDAD_FEDERATIVA'] == select_estados)
                       & (df['Año'] == select_anio)]

    # Actualiza la Data Table
    data_table = filtered_data.to_dict('records')

    # Variables a mostrar en los gráficos
    variables = ['Lugares_Ofertados', 'Solicitudes_de_Primer_Ingreso', 'Primer_Ingreso_Total',
                 'Matrícula_Total', 'Egresados_Total', 'Titulados_Total']

    # Calcula la suma de cada variable por municipio
    variable_sums = filtered_data.groupby('MUNICIPIO')[variables].sum().reset_index()

    bar_data = []
    line_data = []

    for variable in variables:
        # Gráfico de Barras
        bar_data.append(
            go.Bar(
                x=variable_sums['MUNICIPIO'],
                y=variable_sums[variable],
                name=variable,
                text=variable_sums[variable],
                textposition='inside'
            )
        )

        # Gráfico Lineal
        line_data.append(
            go.Scatter(
                x=variable_sums['MUNICIPIO'],
                y=variable_sums[variable],
                mode='lines+markers',
                name=variable,
                text=variable_sums[variable],
                textposition='top center'
            )
        )

    bar_fig = go.Figure(data=bar_data)
    bar_fig.update_layout(
        barmode='group',
        title=f'Suma de Variables por Municipio de {select_estados}',
        xaxis_title='Municipio',
        yaxis_title='Suma',
        yaxis=dict(title="Suma")
    )

    line_fig = go.Figure(data=line_data)
    line_fig.update_layout(
        title=f'Suma de Variables por Municipio de {select_estados} (Gráfico Lineal)',
        xaxis_title='Municipio',
        yaxis_title='Suma'
    )

    # Crear gráficos de pastel con Plotly Express para todas las variables
    pie_data_variables = []

    for variable in variables:
        # Modifica el título del gráfico de pastel
        pie_title = f'Distribución de {variable} en {select_estados}'
        pie_data = px.pie(filtered_data, names='MUNICIPIO', values=variable, title=pie_title)
        pie_data_variables.append(pie_data)

    pie_chartM = pie_data_variables[0]
    pie_chartM1 = pie_data_variables[1]
    pie_chartM2 = pie_data_variables[2]
    pie_chartM3 = pie_data_variables[3]
    pie_chartM4 = pie_data_variables[4]
    pie_chartM5 = pie_data_variables[5]

    return data_table, bar_fig, line_fig, pie_chartM, pie_chartM1, pie_chartM2, pie_chartM3, pie_chartM4, pie_chartM5


