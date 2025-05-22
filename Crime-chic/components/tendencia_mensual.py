from dash import html, dcc
import plotly.express as px
import pandas as pd

def layout_tendencia_mensual(df):
    # Asegurar que la columna 'date' esté en formato datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Crear columna de mes (año-mes)
    df['mes'] = df['date'].dt.to_period('M').astype(str)

    # Agrupar por mes y contar
    tendencia = df.groupby('mes').size().reset_index(name='total_crimenes')

    # Crear figura
    fig = px.line(
        tendencia,
        x='mes',
        y='total_crimenes',
        title='Tendencia Mensual de Crímenes',
        markers=True
    )

    return html.Div([
        html.H2("Crímenes por Mes"),
        dcc.Graph(figure=fig)
    ])
