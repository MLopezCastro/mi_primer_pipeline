import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def _ensure_dir(dirpath: str):
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

def save_csv(df: pd.DataFrame, path: str) -> None:
    _ensure_dir(os.path.dirname(path))
    df.to_csv(path, index=False)
    logger.info(f"Guardado {path} | filas={len(df)} cols={df.shape[1]}")
