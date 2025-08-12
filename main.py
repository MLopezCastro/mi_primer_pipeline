from utils.logger import get_logger
from pipeline.load import load_csv
from pipeline.save import save_csv
from pipeline.transform import clean_column_names

logger = get_logger("pipeline")

def run():
    logger.info("=== Inicio del pipeline ===")
    df = load_csv("data/input/ventas_raw.csv")

    before = len(df)
    df = clean_column_names(df)
    logger.info(f"clean_column_names: filas {before} -> {len(df)}")

    save_csv(df, "data/output/ventas_limpias.csv")
    logger.info("=== Fin del pipeline ===")

if __name__ == "__main__":
    run()
