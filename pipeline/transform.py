import re
import pandas as pd
from unidecode import unidecode

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas:
    - minúsculas, sin tildes
    - espacios -> underscore
    - solo [a-z0-9_]
    """
    df = df.copy()
    new_cols = []
    for c in df.columns:
        c2 = unidecode(str(c).strip())
        c2 = re.sub(r"\s+", "_", c2)
        c2 = re.sub(r"[^0-9a-zA-Z_]", "", c2).lower()
        new_cols.append(c2)
    df.columns = new_cols
    return df

def drop_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas que tengan valores nulos en cualquier campo."""
    return df.dropna(how="any")

def filter_positive_values(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Elimina filas donde la columna indicada es <= 0.
    Convierte a numérico antes (valores no convertibles -> NaN -> se filtran).
    """
    df = df.copy()
    if col not in df.columns:
        return df
    df[col] = pd.to_numeric(df[col], errors="coerce")
    return df[df[col] > 0]

def remove_empty_names(df: pd.DataFrame, col: str = "vendedor") -> pd.DataFrame:
    """Elimina filas sin nombre de vendedor (NaN o espacios)."""
    df = df.copy()
    if col not in df.columns:
        return df
    mask = df[col].notna() & df[col].astype(str).str.strip().ne("")
    return df[mask]

def normalize_product_names(df: pd.DataFrame, col: str = "producto") -> pd.DataFrame:
    """Convierte los nombres de producto a minúsculas y sin tildes."""
    df = df.copy()
    if col not in df.columns:
        return df
    df[col] = df[col].astype(str).map(
        lambda x: unidecode(x).lower().strip() if pd.notna(x) else x
    )
    return df
