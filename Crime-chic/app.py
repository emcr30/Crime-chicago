from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

from utils.loader import cargar_datos
from components.tendencia_mensual import layout_tendencia_mensual 
from components.top_crimenes import layout_top_crimenes 
from components.correlacion import layout_correlacion

# Inicializar app
app = Dash(__name__)
server = app.server

# Cargar datos
df = cargar_datos('data/datos_crimen_chicago.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Layout
app.layout = html.Div([
    html.H1("Dashboard de Crímenes en Chicago", style={"textAlign": "center"}),

    dcc.DatePickerRange(
        id='date-range',
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        display_format='YYYY-MM-DD'
    ),

    html.Div(id='grafico-lineal'),
    layout_top_crimenes(),
    html.Div(id='grafico-correlacion') 
])

@app.callback(
    [Output('grafico-lineal', 'children'),
     Output('grafico-torta', 'figure'),
     Output('grafico-correlacion', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('dropdown-top-n', 'value')]  
)
def actualizar_graficos(start_date, end_date, top_n):
    df_filtrado = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    grafico_lineal = layout_tendencia_mensual(df_filtrado)

    top_crimenes = df_filtrado['primary_type'].value_counts().nlargest(top_n).reset_index()
    top_crimenes.columns = ['Crimen', 'Total']

    fig_torta = px.pie(
        top_crimenes,
        names='Crimen',
        values='Total',
        title=f'Top {top_n} Tipos de Crímenes',
        hole=0.4
    )

    correlacion = layout_correlacion(df_filtrado)

    return grafico_lineal, fig_torta, correlacion

# Ejecutar
if __name__ == '__main__':
    app.run(debug=True)
