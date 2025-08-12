import argparse
import sys
from utils.logger import get_logger
from pipeline.load import load_csv
from pipeline.save import save_csv
from pipeline.transform import (
    clean_column_names,
    drop_nulls,
    filter_positive_values,
    remove_empty_names,
    normalize_product_names,
)

logger = get_logger("pipeline")

def log_step(name: str, before: int, after: int):
    logger.info(f"{name}: filas {before} -> {after}")

def run(input_path: str, output_path: str):
    logger.info("=== Inicio del pipeline ===")

    # 1) Load
    df = load_csv(input_path)  # loggea error si no existe

    # 2) Transform
    before = len(df); df = clean_column_names(df);              log_step("clean_column_names", before, len(df))
    before = len(df); df = drop_nulls(df);                      log_step("drop_nulls", before, len(df))
    before = len(df); df = remove_empty_names(df, "vendedor");  log_step("remove_empty_names", before, len(df))
    before = len(df); df = filter_positive_values(df, "cantidad");        log_step("filter_positive_values(cantidad)", before, len(df))
    before = len(df); df = filter_positive_values(df, "precio_unitario"); log_step("filter_positive_values(precio_unitario)", before, len(df))
    before = len(df); df = normalize_product_names(df, "producto");       log_step("normalize_product_names", before, len(df))

    # 3) Save
    save_csv(df, output_path)

    logger.info("=== Fin del pipeline ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de limpieza y validación de ventas")
    parser.add_argument("--input", required=True, help="Ruta del CSV de entrada")
    parser.add_argument("--output", required=True, help="Ruta del CSV limpio de salida")
    args = parser.parse_args()

    try:
        run(args.input, args.output)
    except FileNotFoundError as e:
        logger.error(f"No se pudo ejecutar: {e}")
        sys.exit(1)
    except Exception:
        logger.excepti
