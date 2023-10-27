# Importa las bibliotecas necesarias
import dash
from dash import dcc, html, callback
import pandas as pd
import statsmodels.api as sm
import plotly.express as px
from dash.dependencies import Input, Output
from dash import html

# Cargar tus datos
df = pd.read_excel('Data.xlsx')

# Crear una aplicación Dash
dash.register_page(__name__, name='/Estado RL')

# Obtener la lista de años únicos en la variable "Año" del DataFrame
available_years = df['Año'].unique()

# Define la página EstadoRL como un contenedor HTML Div
layout = html.Div([
    html.H1('Gráficos de Regresión Lineal'),

    # Dropdown para seleccionar el año
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in available_years],
        value=available_years[0]
    ),

    # Gráfico 1: Matrícula Total vs. Lugares Ofertados
    dcc.Graph(id='regression-plot1'),

    # Gráfico 2: Egresados Total vs. Solicitudes de Primer Ingreso
    dcc.Graph(id='regression-plot2'),

    # Gráfico 3: Matrícula Total vs. Primer Ingreso
    dcc.Graph(id='regression-plot3'),

    # Gráfico 4: Egresados Total vs. Titulados Total
    dcc.Graph(id='regression-plot4'),

    # Gráfico 5: Matrícula Total vs. Egresados Total
    dcc.Graph(id='regression-plot5'),

    # Gráfico 6: Solicitudes de Primer Ingreso vs. Lugares Ofertados
    dcc.Graph(id='regression-plot6')
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

# Función para crear un gráfico de regresión lineal con mejoras visuales
def create_regression_plot(x, y, selected_year):
    filtered_df = df[df['Año'] == selected_year]
    model = sm.OLS(filtered_df[y], sm.add_constant(filtered_df[x])).fit()
    title = f'{y} vs. {x}<br>R-squared: {model.rsquared:.2f}<br>Slope: {model.params[x]:.2f}<br>Intercept: {model.params["const"]:.2f}'
    
    fig = px.scatter(filtered_df, x=x, y=y, trendline="ols")
    fig.update_xaxes(title_text=x)
    fig.update_yaxes(title_text=y)

    # Cambiar colores y estilos
    fig.update_traces(marker=dict(size=5, opacity=0.6))

    # Agregar coeficientes de regresión
    annotation = [
        dict(
            x=0.7,
            y=0.9,
            xref='paper',
            yref='paper',
            showarrow=False,
            text=title,
        )
    ]
    fig.update_layout(annotations=annotation)

    return fig

# Actualizar todos los gráficos en la aplicación Dash
@callback(
    [Output('regression-plot1', 'figure'),
     Output('regression-plot2', 'figure'),
     Output('regression-plot3', 'figure'),
     Output('regression-plot4', 'figure'),
     Output('regression-plot5', 'figure'),
     Output('regression-plot6', 'figure')],
    [Input('year-dropdown', 'value')]
)
def update_regression_plots(selected_year):
    x1 = 'Lugares_Ofertados'
    y1 = 'Matrícula_Total'

    x2 = 'Solicitudes_de_Primer_Ingreso'
    y2 = 'Egresados_Total'

    x3 = 'Primer_Ingreso_Total'
    y3 = 'Matrícula_Total'

    x4 = 'Titulados_Total'
    y4 = 'Egresados_Total'

    x5 = 'Egresados_Total'
    y5 = 'Matrícula_Total'

    x6 = 'Lugares_Ofertados'
    y6 = 'Solicitudes_de_Primer_Ingreso'

    fig1 = create_regression_plot(x1, y1, selected_year)
    fig2 = create_regression_plot(x2, y2, selected_year)
    fig3 = create_regression_plot(x3, y3, selected_year)
    fig4 = create_regression_plot(x4, y4, selected_year)
    fig5 = create_regression_plot(x5, y5, selected_year)
    fig6 = create_regression_plot(x6, y6, selected_year)

    return fig1, fig2, fig3, fig4, fig5, fig6

# Ejecutar la aplicación Dash
