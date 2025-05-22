import pandas as pd

def cargar_datos(ruta_csv):
    df = pd.read_csv(ruta_csv, parse_dates=['date'])
    df = df[(df['date'].dt.year >= 2020) & (df['date'].dt.year <= 2025)]
    df['mes'] = df['date'].dt.to_period('M').astype(str)  # Ej: 2024-05
    
    return df
