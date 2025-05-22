from dash import html, dcc
import plotly.express as px

from dash import html, dcc

def layout_top_crimenes():
    return html.Div([
        html.H2("Crímenes Más Frecuentes"),

        html.Label("Selecciona cuántos tipos de crimen mostrar:"),
        dcc.Dropdown(
            id='dropdown-top-n',
            options=[{'label': str(i), 'value': i} for i in range(3, 16)],
            value=10, 
            clearable=False,
            style={'width': '200px', 'marginBottom': '20px'}
        ),

        dcc.Graph(id='grafico-torta')  
    ])

