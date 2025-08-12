# ===============================
# CHEATSHEET.md
# ===============================
# Comandos clave
# venv
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt

# correr pipeline (por defecto con config.yaml)
python main.py
# o con rutas explícitas:
python main.py --input data/input/ventas_raw.csv --output data/output/ventas_limpias.csv

# git
git add .
git commit -m "mensaje"
git push

# Patrones de código
from utils.logger import get_logger
logger = get_logger("pipeline")

from pipeline.load import load_csv
df = load_csv("data/input/ventas_raw.csv")

from pipeline.save import save_csv
save_csv(df, "data/output/ventas_limpias.csv")

before = len(df)
df = alguna_transformacion(df)
logger.info(f"alguna_transformacion: filas {before} -> {len(df)}")


# ===============================
# config.yaml
# ===============================
paths:
  input: data/input/ventas_raw.csv
  output: data/output/ventas_limpias.csv
logging:
  level: INFO


# ===============================
# utils/config.py
# ===============================
from pathlib import Path
import yaml

def load_config(path: str | Path = "config.yaml") -> dict:
    p = Path(path)
    if not p.exists():
        return {"paths": {}, "logging": {"level": "INFO"}}
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    # sane defaults
    data.setdefault("paths", {})
    data.setdefault("logging", {"level": "INFO"})
    return data


# ===============================
# main.py  (REEMPLAZA tu main actual)
# ===============================
import argparse, sys
from utils.logger import get_logger
from utils.config import load_config
from pipeline.load import load_csv
from pipeline.save import save_csv
from pipeline.transform import (
    clean_column_names, drop_nulls, filter_positive_values,
    remove_empty_names, normalize_product_names,
)

logger = get_logger("pipeline")

def log_step(name: str, before: int, after: int):
    logger.info(f"{name}: filas {before} -> {after}")

def run(input_path: str, output_path: str):
    logger.info("=== Inicio del pipeline ===")

    # 1) Load
    df = load_csv(input_path)

    # 2) Transform
    b=len(df); df=clean_column_names(df);              log_step("clean_column_names", b, len(df))
    b=len(df); df=drop_nulls(df);                      log_step("drop_nulls", b, len(df))
    b=len(df); df=remove_empty_names(df,"vendedor");   log_step("remove_empty_names", b, len(df))
    b=len(df); df=filter_positive_values(df,"cantidad");        log_step("filter_positive_values(cantidad)", b, len(df))
    b=len(df); df=filter_positive_values(df,"precio_unitario"); log_step("filter_positive_values(precio_unitario)", b, len(df))
    b=len(df); df=normalize_product_names(df,"producto");       log_step("normalize_product_names", b, len(df))

    # 3) Save
    save_csv(df, output_path)

    logger.info("=== Fin del pipeline ===")

if __name__ == "__main__":
    cfg = load_config()
    default_in  = cfg.get("paths", {}).get("input",  "data/input/ventas_raw.csv")
    default_out = cfg.get("paths", {}).get("output", "data/output/ventas_limpias.csv")

    parser = argparse.ArgumentParser(description="Pipeline de limpieza y validación de ventas")
    parser.add_argument("--input",  default=default_in,  help="CSV de entrada (por defecto toma config.yaml)")
    parser.add_argument("--output", default=default_out, help="CSV de salida (por defecto toma config.yaml)")
    args = parser.parse_args()

    try:
        run(args.input, args.output)
    except FileNotFoundError as e:
        logger.error(f"No se pudo ejecutar: {e}"); sys.exit(1)
    except Exception:
        logger.exception("Fallo inesperado"); sys.exit(2)


# ===============================
# pipeline/save.py  (ACTUALIZA para incluir Parquet opcional)
# ===============================
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

def save_parquet(df: pd.DataFrame, path: str) -> None:
    """Requiere pyarrow. Instalar: pip install pyarrow"""
    try:
        import pyarrow  # noqa: F401
    except ImportError:
        logger.error("Falta 'pyarrow'. Instalá con: pip install pyarrow")
        raise
    _ensure_dir(os.path.dirname(path))
    df.to_parquet(path, index=False)
    logger.info(f"Guardado {path} | filas={len(df)} cols={df.shape[1]}")


# ===============================
# tests/test_transform.py
# ===============================
import pandas as pd
from pipeline.transform import (
    clean_column_names, drop_nulls, remove_empty_names,
    filter_positive_values, normalize_product_names
)

def test_clean_column_names():
    df = pd.DataFrame(columns=["Fecha", "Precio Unitario", "Producto"])
    out = clean_column_names(df)
    assert list(out.columns) == ["fecha", "precio_unitario", "producto"]

def test_remove_empty_names():
    df = pd.DataFrame({"vendedor": ["Ana", " ", None]})
    out = remove_empty_names(df)
    assert out["vendedor"].tolist() == ["Ana"]

def test_filter_positive_values():
    df = pd.DataFrame({"cantidad": [1, 0, -2, 3]})
    out = filter_positive_values(df, "cantidad")
    assert out["cantidad"].tolist() == [1, 3]


# ===============================
# requirements.txt  (actualizado para config/parquet)
# ===============================
pandas>=2.0
Unidecode>=1.3
PyYAML>=6.0
# opcional para Parquet:
pyarrow>=15.0


# ===============================
# requirements-dev.txt  (para tests)
# ===============================
pytest>=7.0


# ===============================
# .github/workflows/ci.yml  (GitHub Actions - corre tests)
# ===============================
name: CI
on:
  push:
  pull_request:
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install deps
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          source .venv/bin/activate
          pytest -q


# ===============================
# run_pipeline.bat  (Windows - opcional)
# ===============================
@echo off
IF NOT DEFINED VIRTUAL_ENV (
  call .\.venv\Scripts\activate
)
python main.py


# ===============================
# run_pipeline.sh  (Linux/Mac - opcional)
# ===============================
#!/usr/bin/env bash
source .venv/bin/activate 2>/dev/null || true
python main.py
