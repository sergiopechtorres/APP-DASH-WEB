import dash
from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback, Input, Output

df = pd.read_excel('Data.xlsx')

# Agrupa los datos por estado y realiza la suma de los indicadores
df_grouped = df.groupby(['Año', 'ENTIDAD_FEDERATIVA']).sum().reset_index()

# Obtiene la lista de años únicos de tu DataFrame
available_years = df['Año'].unique()

dash.register_page(__name__, name='Estado')

layout = html.Div([
    html.Div([
        html.H1('ANUIES DASH'),
        html.Img(src='assets/estados.png')
    ], className='banner'),

    html.Div([
        html.P('Selecciona el año', className='fix_label', style={'color': 'black', 'text-align': 'center'}),

        dcc.Dropdown(

            id='select-year',
            options=[
                {'label': str(year), 'value': year}
                for year in available_years  # Usar los años disponibles en tu DataFrame
            ],
            value=available_years[-1]  # Año inicial seleccionado (último año en la lista)
        )
    ], className='create_container nine columns', style={'margin-bottom': '10px'}),

    html.Div([
        html.Div([
            html.P('Selecciona el indicador', className='fix_label', style={'color': 'black', 'margin-top': '2px'}),
            dcc.RadioItems(id='dosis-radioitems',
                           labelStyle={
                               'display': 'inline-block',
                               'margin-right': '6px',
                               'font-weight': 300
                           },
                           options=[
                               {'label': 'Lugares Ofertados', 'value': 'Lugares_Ofertados'},
                               {'label': 'Solicitudes de Primer ingreso', 'value': 'Solicitudes_de_Primer_Ingreso'},
                               {'label': 'Primer Ingreso', 'value': 'Primer_Ingreso_Total'},
                               {'label': 'Matriculados', 'value': 'Matrícula_Total'},
                               {'label': 'Egresados', 'value': 'Egresados_Total'},
                               {'label': 'Titulados', 'value': 'Titulados_Total'},
                           ],
                           value='Lugares_Ofertados',
                           style={'text-align': 'center', 'align-items': 'center', 'justify-content': 'center',
                                  'color': 'black'},
                           className='dcc_compon'
                           ),
        ], className='create_container2 nine columns', style={'margin-bottom': '10px'}),
    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='my_graph', figure={})
        ], className='create_container2 eleven columns'),

        html.Div([
            dcc.Graph(id='pie_graph', figure={})
        ], className='create_container2 eleven columns'),

    ], className='row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id='scatter_graph', figure={})
        ], className='create_container2 eleven columns')
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id='lin_graph', figure={})
        ], className='create_container2 eleven columns')
    ])
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

@callback(
    [Output('my_graph', 'figure'),
     Output('pie_graph', 'figure'),
     Output('scatter_graph', 'figure'),
     Output('lin_graph', 'figure')],
    [Input('dosis-radioitems', 'value'),
     Input('select-year', 'value')]
)
def update_graph(value, selected_year):
    # Filtra los datos del DataFrame agrupado según el año seleccionado
    filtered_df = df_grouped[df_grouped['Año'] == selected_year]

    title_text = 'Gráfico de Barras'

    if value == 'Lugares_Ofertados':
        fig = px.bar(filtered_df, x="ENTIDAD_FEDERATIVA", y="Lugares_Ofertados",
                     color="ENTIDAD_FEDERATIVA", text="Lugares_Ofertados")
        title_text = 'Gráfico de Barras - Lugares Ofertados'
    elif value == 'Solicitudes_de_Primer_Ingreso':
        fig = px.bar(filtered_df, x="ENTIDAD_FEDERATIVA", y="Solicitudes_de_Primer_Ingreso",
                     color="ENTIDAD_FEDERATIVA", text="Solicitudes_de_Primer_Ingreso", color_discrete_sequence=px.colors.qualitative.Set3)
        title_text = 'Gráfico de Barras - Solicitudes de Primer Ingreso'
    elif value == 'Primer_Ingreso_Total':
        fig = px.bar(filtered_df, x="ENTIDAD_FEDERATIVA", y='Primer_Ingreso_Total',
                     color="ENTIDAD_FEDERATIVA", text="Primer_Ingreso_Total")
        title_text = 'Gráfico de Barras - Primer Ingreso Total'
    elif value == 'Matrícula_Total':
        fig = px.bar(filtered_df, x="ENTIDAD_FEDERATIVA", y='Matrícula_Total',
                     color="ENTIDAD_FEDERATIVA", text="Matrícula_Total")
        title_text = 'Gráfico de Barras - Matrícula Total'
    elif value == 'Egresados_Total':
        fig = px.bar(filtered_df, x="ENTIDAD_FEDERATIVA", y='Egresados_Total',
                     color="ENTIDAD_FEDERATIVA", text="Egresados_Total")
        title_text = 'Gráfico de Barras - Egresados Total'
    else:
        fig = px.bar(filtered_df, x="ENTIDAD_FEDERATIVA", y='Titulados_Total',
                     color="ENTIDAD_FEDERATIVA", text="Titulados_Total")
        title_text = 'Gráfico de Barras - Titulados Total'

    fig.update_layout(
        font_family="verdana",
        font_color="blue",
        title_font_family="Arial Black",
        title_font_color="red",
        legend_title_font_color="green",
        font=dict(
            family="verdana",
            size=10,
            color="RebeccaPurple"
        )
    )
    fig.update_traces(textfont_size=8, textangle=0, textposition="inside", cliponaxis=False)
    fig.update_xaxes(title_font_family="Arial")
    fig.update_layout(title={'text': title_text})

    # Gráfico de pastel (pie chart)
    fig2 = px.pie(
        data_frame=filtered_df,
        names='ENTIDAD_FEDERATIVA',
        values=value,  # Usa el indicador seleccionado como valor
        title='Gráfico circular (Pie chart)',
        hover_data=[value],
        labels='ENTIDAD_FEDERATIVA'
    )
    fig2.update_layout(title={'text': f'Gráfico Circular - {value}', 'x': 0.5}, uniformtext_minsize=12,
                       uniformtext_mode='hide')

    # Gráfico de dispersión (scatter plot)
    fig3 = px.scatter(
        data_frame=filtered_df,
        x=value,  # Usa el indicador seleccionado como eje x
        y="ENTIDAD_FEDERATIVA",
        title=f'Diagrama de Dispersión - {value}'
    )
    fig3.update_yaxes(showline=False, showgrid=False, zeroline=False, title='')

    # Gráfico de líneas (line chart)
    fig4 = px.line(filtered_df, x="ENTIDAD_FEDERATIVA", y=value, text=value, markers=True, line_shape="linear",
                   title=f'Gráfico de Líneas - {value}')

    return fig, fig2, fig3, fig4

