# core.py — esqueleto que vale aprender de memoria (≈30 líneas)
import argparse, os, sys, pandas as pd, logging

def get_logger():
    lg = logging.getLogger("pipe")
    if lg.handlers: return lg
    lg.setLevel(logging.INFO)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter("%Y-%m-%d %H:%M:%S | %(levelname)s | %(message)s"))
    lg.addHandler(h)
    return lg

logger = get_logger()

def load_csv(path):
    if not os.path.exists(path):
        logger.error(f"No existe el archivo: {path}")
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    logger.info(f"Cargado {path} | filas={len(df)} cols={df.shape[1]}")
    return df

def save_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Guardado {path} | filas={len(df)} cols={df.shape[1]}")

# lugar para tus transformaciones
def clean_column_names(df):
    import re
    new = (c.strip().lower() for c in df.columns)
    df = df.copy()
    df.columns = [re.sub(r"[^0-9a-z_]", "", c.replace(" ", "_")) for c in new]
    return df

def run(i_path, o_path):
    logger.info("=== Inicio ===")
    df = load_csv(i_path)
    before = len(df); df = clean_column_names(df); logger.info(f"clean_column_names: {before}->{len(df)}")
    save_csv(df, o_path)
    logger.info("=== Fin ===")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    try:
        run(a.input, a.output)
    except Exception:
        logger.exception("Fallo inesperado"); sys.exit(1)
