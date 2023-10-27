import dash
from dash import dcc, html
import pandas as pd
from dash import dash_table as dt
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

df = pd.read_excel('Data.xlsx')

# Define the unique states
estadou = df['ENTIDAD_FEDERATIVA'].unique()

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div([
            html.H1('INSTITUCIONES DE EDUCACIÓN SUPERIOR'),
            html.Img(src='assets/educational.png')
        ], className='banner'),

        # Dropdown for selecting the state
        html.Div([
            html.Div([
                html.P('Selecciona el estado', className='fix_label', style={'color': 'black', 'text-align': 'center'}),
                dcc.Dropdown(id='select_estadoin',
                             multi=False,
                             clearable=True,
                             disabled=False,
                             style={'display': True},
                             value='AGUASCALIENTES',
                             placeholder='Selecciona Estado',
                             options=[{'label': c, 'value': c} for c in estadou],
                             className="dcc_compon"),

                html.P('Selecciona el municipio', className='fix_label', style={'color': 'black', 'text-align': 'center'}),
                dcc.Dropdown(id='select_municipio1',
                             multi=False,
                             clearable=True,
                             disabled=False,
                             style={'display': True},
                             # value='AGUASCALIENTES',
                             placeholder='Selecciona Municipio',
                             options=[],
                             className="dcc_compon")

            ], className='create_container1 four columns', style={'margin-bottom': '8px'})

        ], className="row flex-display"),

        # Dropdown for selecting the institution
        html.Div([
            html.Div([
                html.P('Selecciona la institución', className='fix_label', style={'color': 'black', 'text-align': 'center'}),
                dcc.Dropdown(id='select_institucion',
                             multi=False,
                             clearable=True,
                             disabled=False,
                             style={'display': True},
                             value='AGUASCALIENTES',
                             placeholder='Selecciona Institución',
                             options=[{'label': c, 'value': c} for c in df['INSTITUCION_DE_EDUCACION_SUPERIOR'].unique()],
                             className="dcc_compon")

            ], className='create_container1 four columns', style={'margin-bottom': '8px'})

        ], className="row flex-display"),

        # Dropdown for selecting the year
        html.Div([
            html.P('Selecciona el año', className='fix_label', style={'color': 'black', 'text-align': 'center'}),
            dcc.Dropdown(id='select_anio',
                         multi=False,
                         clearable=True,
                         disabled=False,
                         style={'display': True},
                         value=2023,  # Default year
                         options=[{'label': year, 'value': year} for year in df['Año'].unique()],
                         className="dcc_compon")
        ], className='create_container1 four columns', style={'margin-bottom': '8px'}),

        # Data Table
        html.Div([
            html.Div([

                dt.DataTable(id='my_datatablein',
                             columns=[{'id': c, 'name': c} for c in df.columns.values],
                             sort_action="native",
                             sort_mode="multi",
                             virtualization=True,
                             style_cell={'textAlign': 'left',
                                         'min-width': '230px',
                                         'backgroundColor': '#34495E',
                                         'color': '#34495E',
                                         'border-bottom': '0.01rem solid #313841',
                                         },
                             style_as_list_view=True,
                             style_header={
                                 'backgroundColor': '#34495E',
                                 'fontWeight': 'bold',
                                 'font': 'Lato, sans-serif',
                                 'color': 'orange',
                                 'border': '#34495E',
                             },
                             style_data={'textOverflow': 'hidden', 'color': '#34495E'},
                             fixed_rows={'headers': True}
                             )

            ], className='create_container2 thirteen columns'),

            html.Div([
                html.Div([
                    dcc.Graph(id='bar_ins',
                              config={'displayModeBar': 'hover'})
                ], className='create_container1 twelve columns')
            ], className='row flex-display'),

            html.Div([
                html.Div([
                    dcc.Graph(id='line_chart',
                              config={'displayModeBar': 'hover'})
                ], className='create_container1 twelve columns')
            ], className='row flex-display'),

        ], className='row flex-display'),

    ],
)


@dash.callback(
    Output('select_municipio1', 'options'),
    Input('select_estadoin', 'value'))
def get_municipio_options(select_estadoin):
    filtered_df = df[df['ENTIDAD_FEDERATIVA'] == select_estadoin]
    municipios = filtered_df['MUNICIPIO'].unique()
    return [{'label': i, 'value': i} for i in municipios]


@dash.callback(
    Output('select_municipio1', 'value'),
    Input('select_municipio1', 'options'))
def get_municipio(select_municipios1):
    return select_municipios1[0]['value']


@dash.callback(
    Output('select_institucion', 'options'),
    [Input('select_estadoin', 'value'), Input('select_municipio1', 'value')]
)
def get_institucion_options(select_estadoin, select_municipio1):
    filtered_df = df[(df['ENTIDAD_FEDERATIVA'] == select_estadoin) & (df['MUNICIPIO'] == select_municipio1)]
    instituciones = filtered_df['INSTITUCION_DE_EDUCACION_SUPERIOR'].unique()
    return [{'label': institucion, 'value': institucion} for institucion in instituciones]


@dash.callback(
    Output('my_datatablein', 'data'),
    [Input('select_estadoin', 'value'), Input('select_municipio1', 'value'), Input('select_institucion', 'value')]
)
def display_table(select_estadoin, select_municipio1, select_institucion):
    filtered_df = df[(df['ENTIDAD_FEDERATIVA'] == select_estadoin) & (df['MUNICIPIO'] == select_municipio1) & (
            df['INSTITUCION_DE_EDUCACION_SUPERIOR'] == select_institucion)]
    return filtered_df.to_dict('records')


# Define a custom color palette
colors = px.colors.qualitative.Set1  # You can change 'Set1' to another palette if desired

@dash.callback(
    Output('bar_ins', 'figure'),
    [Input('select_estadoin', 'value'), Input('select_municipio1', 'value'), Input('select_institucion', 'value'), Input('select_anio', 'value')]
)
def update_bar_chart(select_estadoin, select_municipio1, select_institucion, select_anio):
    data = df[(df['ENTIDAD_FEDERATIVA'] == select_estadoin) & (df['MUNICIPIO'] == select_municipio1) & (df['INSTITUCION_DE_EDUCACION_SUPERIOR'] == select_institucion) & (df['Año'] == select_anio)]

    # Sum total of each variable by institution
    data_grouped = data.groupby('INSTITUCION_DE_EDUCACION_SUPERIOR').sum().reset_index()

    fig = px.bar(data_grouped, x=['Lugares_Ofertados', 'Solicitudes_de_Primer_Ingreso', 'Primer_Ingreso_Total',
                                  'Matrícula_Total', 'Egresados_Total', 'Titulados_Total'], y='INSTITUCION_DE_EDUCACION_SUPERIOR',
                 title=f'Sum total of academic data by INSTITUCIÓN DE EDUCACIÓN SUPERIOR in {select_municipio1}, {select_estadoin} - {select_institucion} - Year {select_anio}',
                 labels={'x': 'Values', 'y': 'Institution of Higher Education'},
                 color_discrete_sequence=colors,
                 barmode='group',
                 text=[f"{int(val):,}" for val in data_grouped['Lugares_Ofertados']]
                 )

    fig.update_traces(texttemplate='%{text}', textposition='outside')

    fig.update_layout(
        xaxis_title="Values",
        yaxis_title="Institution of Higher Education",
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font_color='white'
    )

    fig.update_xaxes(title_font=dict(size=16, color='white'))
    fig.update_yaxes(title_font=dict(size=16, color='white'))

    return fig


@dash.callback(
    Output('line_chart', 'figure'),
    [Input('select_estadoin', 'value'), Input('select_municipio1', 'value'), Input('select_institucion', 'value'), Input('select_anio', 'value')]
)
def update_line_chart(select_estadoin, select_municipio1, select_institucion, select_anio):
    data = df[(df['ENTIDAD_FEDERATIVA'] == select_estadoin) & (df['MUNICIPIO'] == select_municipio1) & (df['INSTITUCION_DE_EDUCACION_SUPERIOR'] == select_institucion) & (df['Año'] == select_anio)]

    # Sum total of each variable by institution
    data_grouped = data.groupby('INSTITUCION_DE_EDUCACION_SUPERIOR').sum().reset_index()

    fig = px.line(data_grouped, x=['Lugares_Ofertados', 'Solicitudes_de_Primer_Ingreso', 'Primer_Ingreso_Total',
                                  'Matrícula_Total', 'Egresados_Total', 'Titulados_Total'],
                 y='INSTITUCION_DE_EDUCACION_SUPERIOR',
                 title=f'Sum total of academic data by institution in {select_municipio1}, {select_estadoin} - {select_institucion} - Year {select_anio}',
                 labels={'x': 'Values', 'y': 'Institution of Higher Education'},
                 color_discrete_sequence=colors)

    fig.update_layout(
        xaxis_title="Values",
        yaxis_title="Institution of Higher Education",
        plot_bgcolor='#1e2130',
        paper_bgcolor='#1e2130',
        font_color='white'
    )

    fig.update_xaxes(title_font=dict(size=16, color='white'))
    fig.update_yaxes(title_font=dict(size=16, color='white'))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

