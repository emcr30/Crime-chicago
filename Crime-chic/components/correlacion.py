import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io

def layout_correlacion(df):
    columnas_numericas = [
        'beat', 'district', 'ward', 'community_area',
        'x_coordinate', 'y_coordinate', 'latitude', 'longitude', 'year'
    ]

    columnas_presentes = [col for col in columnas_numericas if col in df.columns]

    # Filtrar y limpiar
    df_numerico = df[columnas_presentes].copy()
    df_numerico = df_numerico.apply(pd.to_numeric, errors='coerce')
    df_numerico = df_numerico.dropna()

    # Calcular correlación
    correlacion = df_numerico.corr(method='pearson')

    # Crear figura con Seaborn
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlacion, annot=True, fmt=".2f", cmap="coolwarm", square=True, ax=ax)
    plt.title("Matriz de Correlación (Pearson)")
    plt.tight_layout()

    # Convertir la figura a imagen base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)

    # Devolver imagen HTML para Dash
    from dash import html
    return html.Div([
        html.H4("Correlación"),
        html.Img(src='data:image/png;base64,{}'.format(imagen_base64),
                 style={'width': '100%', 'maxWidth': '800px'})
    ])
