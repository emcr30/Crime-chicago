import folium
from folium.plugins import HeatMap
from dash import html
import io

def layout_mapa_calor(df):
    # Si no hay datos o faltan las columnas, mostramos un mensaje
    if df.empty or 'latitude' not in df.columns or 'longitude' not in df.columns:
        return html.P("No hay datos disponibles para el rango seleccionado.")

    # Crear mapa centrado en Chicago
    mapa = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

    # Añadir capa de calor
    heat_data = df[['latitude', 'longitude']].dropna().values.tolist()
    HeatMap(heat_data, radius=10).add_to(mapa)

    # Serializar mapa a HTML para incrustar en un Iframe
    mapa_bytes = io.BytesIO()
    mapa.save(mapa_bytes, close_file=False)
    mapa_html = mapa_bytes.getvalue().decode()

    return html.Iframe(
        srcDoc=mapa_html,
        width='100%',
        height='600',
        style={'border': 'none'}
    )
