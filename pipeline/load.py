import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        logger.error(f"No existe el archivo: {path}")
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    logger.info(f"Cargado {path} | filas={len(df)} cols={df.shape[1]}")
    return df
