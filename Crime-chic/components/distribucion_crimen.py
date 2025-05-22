# components/distribucion_crimen.py

from dash import html, dcc
import plotly.express as px
import pandas as pd

def layout_distribucion_crimen(df):
    # Asegurarse de que la fecha esté en formato datetime
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Extraer año y hora
    df['year'] = df['date'].dt.year
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek  # lunes=0, domingo=6

    # Agrupar por hora y año
    conteo_por_hora = df.groupby(['year', 'hour']).size().reset_index(name='count')

    # Crear gráfico de líneas por hora y año
    fig_lineal_hora = px.line(
        conteo_por_hora,
        x='hour',
        y='count',
        color='year',
        markers=True,
        title='Distribución de Crímenes por Hora del Día (Comparación por Año)',
        labels={'hour': 'Hora del Día', 'count': 'Cantidad de Crímenes', 'year': 'Año'}
    )

    # Crear mapa de calor día vs hora
    conteo_dia_hora = df.groupby(['dayofweek', 'hour']).size().reset_index(name='count')
    heatmap = px.density_heatmap(
        conteo_dia_hora,
        x='hour',
        y='dayofweek',
        z='count',
        color_continuous_scale='Viridis',
        title='Mapa de Calor: Día de la Semana vs Hora del Día',
        labels={'hour': 'Hora del Día', 'dayofweek': 'Día de la Semana', 'count': 'Cantidad'}
    )
    heatmap.update_yaxes(
        tickmode='array',
        tickvals=list(range(7)),
        ticktext=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    )

    return html.Div([
        html.H2("Distribución Temporal de Crímenes", style={"textAlign": "center", "marginTop": "30px"}),
        dcc.Graph(figure=fig_lineal_hora),
        dcc.Graph(figure=heatmap)
    ])
