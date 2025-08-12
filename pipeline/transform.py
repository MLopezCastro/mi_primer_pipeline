import re
import pandas as pd
from unidecode import unidecode

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """minúsculas, sin tildes, espacios->underscore, solo [a-z0-9_]"""
    df = df.copy()
    new_cols = []
    for c in df.columns:
        c2 = unidecode(str(c).strip())
        c2 = re.sub(r"\s+", "_", c2)
        c2 = re.sub(r"[^0-9a-zA-Z_]", "", c2).lower()
        new_cols.append(c2)
    df.columns = new_cols
    return df
