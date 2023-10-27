import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table as dt
import plotly.graph_objs as go
import plotly.express as px

df = pd.read_excel('Data.xlsx')
estados = df['ENTIDAD_FEDERATIVA'].unique()
years = df['Año'].unique()  # Assuming you have a column named 'Año' for years

dash.register_page(__name__, name='Programa de Estudios')

layout = html.Div([
    html.Div([
        html.Div([
            html.P('Elige Estado :', className='fix_label', style={'color': 'black'}),
            dcc.Dropdown(id='w_estado',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': True},
                         value='AGUASCALIENTES',
                         placeholder='Selecciona Estados',
                         options=[{'label': c, 'value': c} for c in estados], className='DCC_compon'),
            html.P('Elige Municipio :', className='fix_label', style={'color': 'black'}),
            dcc.Dropdown(id='muni',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': True},
                         placeholder='Selecciona Municipios',
                         options=[], className='dcc_compon'),
            html.P('Elige Año :', className='fix_label', style={'color': 'black'}),
            dcc.Dropdown(id='year',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': True},
                         value=years[0],  # Set the default year
                         placeholder='Selecciona Año',
                         options=[{'label': y, 'value': y} for y in years], className='dcc_compon'),
        ], className="create_container six columns"),
        html.Div([
            dcc.Graph(id='bar_chart', config={'displayModeBar': 'hover'}),
        ], className="Create_container eleven columns"),
        html.Div([
            dcc.Graph(id='pie_chart', config={'displayModeBar': 'hover'}),
        ], className="create_container eleven columns"),
        html.Div([
            dcc.Graph(id='line-chart', config={'displayModeBar': 'hover'}),
        ], className="create_container eleven columns"),
        html.Div([
            dcc.Graph(id='scatter_chart', config={'displayModeBar': 'hover'}),
        ], className="create_container eleven columns"),
    ])
])

@callback(
    Output('muni', 'options'),
    Input('w_estado', 'value'))
def get_country_options(w_estado):
    terr3 = df[df['ENTIDAD_FEDERATIVA'] == w_estado]
    return [{'label': i, 'value': i} for i in terr3['MUNICIPIO'].unique()]

@callback(
    Output('muni', 'value'),
    Input('muni', 'options'))
def get_country_value(muni_options):
    return muni_options[0]['value'] if muni_options else None

# Update the bar chart
@callback(
    Output('bar_chart', 'figure'),
    [Input('muni', 'value'), Input('year', 'value')]
)
def update_bar_chart(selected_muni, selected_year):
    if not selected_muni:
        return go.Figure()
    data = df[(df['MUNICIPIO'] == selected_muni) & (df['Año'] == selected_year)]
    selected_estado = data['ENTIDAD_FEDERATIVA'].values[0]
    fig = px.bar(
        data,
        x='PROGRAMADEESTUDIOS',
        y=['Lugares_Ofertados', 'Solicitudes_de_Primer_Ingreso', 'Primer_Ingreso_Total',
           'Matrícula_Total', 'Egresados_Total', 'Titulados_Total'],
        title=f'Datos académicos por Programa de Estudios en {selected_muni}, {selected_estado} ({selected_year})',
        labels={'variable': 'Datos', 'value': 'Cantidad'},
        template='plotly',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_xaxes(
        tickangle=45,
        title_text='Programa de Estudio',
        title_standoff=25
    )
    fig.update_yaxes(
        title_text='Cantidad',
        title_standoff=25
    )
    fig.update_layout(
        plot_bgcolor='white',
    )
    return fig

# Update the pie chart
@callback(
    Output('pie_chart', 'figure'),
    [Input('muni', 'value'), Input('year', 'value')]
)
def update_pie_chart(selected_municipio, selected_year):
    if selected_municipio is None:
        return px.pie(names=[], values=[], title="Distribución de Datos")
    filtered_data = df[(df['MUNICIPIO'] == selected_municipio) & (df['Año'] == selected_year)]
    programas_estudio = filtered_data['PROGRAMADEESTUDIOS'].unique()
    filtered_data['Datos'] = (
        filtered_data['Lugares_Ofertados'] +
        filtered_data['Solicitudes_de_Primer_Ingreso'] +
        filtered_data['Primer_Ingreso_Total'] +
        filtered_data['Matrícula_Total'] +
        filtered_data['Egresados_Total'] +
        filtered_data['Titulados_Total']
    )
    fig = px.pie(
        filtered_data,
        names='PROGRAMADEESTUDIOS',
        values='Datos',
        title=f'Datos académicos por Programa de Estudios en {selected_municipio} ({selected_year})',
        template='plotly',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig

# Update the line chart
@callback(
    Output('line-chart', 'figure'),
    [Input('w_estado', 'value'), Input('muni', 'value'), Input('year', 'value')]
)
def update_line_chart(selected_estado, selected_municipio, selected_year):
    if not selected_municipio:
        return px.line(title="Datos Académicos por Programa de Estudio")
    filtered_data = df[(df['ENTIDAD_FEDERATIVA'] == selected_estado) & (df['MUNICIPIO'] == selected_municipio) & (df['Año'] == selected_year)]
    fig = px.line(
        filtered_data,
        x='PROGRAMADEESTUDIOS',
        y=['Lugares_Ofertados', 'Solicitudes_de_Primer_Ingreso', 'Primer_Ingreso_Total', 'Matrícula_Total', 'Egresados_Total', 'Titulados_Total'],
        labels={'value': 'Datos', 'variable': 'Tipo de Datos'},
        title=f"Datos Académicos por Programa de Estudio en {selected_municipio}, {selected_estado} ({selected_year})",
        template='plotly_dark'
    )
    fig.update_layout(
        xaxis_title='Programa de Estudio',
        yaxis_title='Cantidad',
        font=dict(family='Arial', size=12),
        legend=dict(orientation='h'),
    )
    return fig

# Update the scatter chart
@callback(
    Output('scatter_chart', 'figure'),
    [Input('muni', 'value'), Input('year', 'value')]
)
def update_scatter_chart(selected_municipio, selected_year):
    if selected_municipio is None:
        return px.scatter(title="Gráfico de Dispersión")
    filtered_data = df[(df['MUNICIPIO'] == selected_municipio) & (df['Año'] == selected_year)]
    fig = px.scatter(filtered_data, x='PROGRAMADEESTUDIOS', y='Lugares_Ofertados',
                     color='PROGRAMADEESTUDIOS', size='Solicitudes_de_Primer_Ingreso',
                     title=f'Gráfico de Dispersión en {selected_municipio} ({selected_year})',
                     template='plotly',
                     color_discrete_sequence=px.colors.qualitative.Set3,
                     labels={'PROGRAMADEESTUDIOS': 'Programa de Estudio', 'Lugares_Ofertados': 'Lugares Ofertados',
                             'Solicitudes_de_Primer_Ingreso': 'Solicitudes de Primer Ingreso'}
                     )
    return fig


