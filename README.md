# 🧪 mi\_primer\_pipeline

Pipeline local en **Python** para **limpieza y validación de datos de ventas**. Incluye modularización, ejecución por **CLI** y **logging** estructurado. Forma parte del **Desafío Semana 1** (Data Engineering).

## 🚀 Objetivo

Tomar un CSV crudo de ventas, aplicar transformaciones mínimas y guardar un CSV limpio listo para análisis.

Transformaciones implementadas:

* clean\_column\_names() → normaliza nombres de columnas (minúsculas, sin tildes, sin espacios; solo \[a–z0–9\_])
* drop\_nulls() → elimina filas con valores nulos
* remove\_empty\_names() → elimina filas sin nombre de vendedor
* filter\_positive\_values(col) → filtra filas con cantidad o precio\_unitario ≤ 0
* normalize\_product\_names() → normaliza nombres de producto (minúsculas y sin tildes)

## 📂 Estructura

* data/input → CSVs originales (ej.: ventas\_raw\.csv)
* data/output → CSVs procesados (ej.: ventas\_limpias.csv)
* pipeline/load.py → load\_csv()
* pipeline/save.py → save\_csv()
* pipeline/transform.py → funciones de transformación
* utils/logger.py → get\_logger()
* main.py → orquestación y CLI
* requirements.txt
* README.md

## 🧰 Requisitos

* Python 3.10 o superior
* venv activo
* Paquetes listados en requirements.txt (pandas, Unidecode)

## ⚙️ Instalación rápida

1. Crear y activar entorno virtual
   Windows:

* python -m venv .venv
* ..venv\Scripts\Activate
  Linux/Mac:
* python3 -m venv .venv
* source .venv/bin/activate

2. Instalar dependencias

* pip install -r requirements.txt

## ▶️ Uso (CLI)

Ejecución con rutas explícitas (ejemplo):

* python main.py --input data/input/ventas\_raw\.csv --output data/output/ventas\_limpias.csv

Caso de error controlado (input inexistente):

* python main.py --input data/input/no\_existe.csv --output data/output/ventas\_limpias.csv
  El pipeline registrará un logger.error y saldrá con código 1.

## 🧪 Datos de ejemplo (input)

Archivo: data/input/ventas\_raw\.csv
Columnas esperadas: Fecha, Vendedor, Producto, Cantidad, Precio Unitario
Ejemplos de filas válidas/ inválidas:

* 2025-07-15, Ana, Bicicleta, 2, 350 → válida
* 2025-07-15, \[vacío], Bicicleta, 1, 350 → se elimina por vendedor vacío
* 2025-07-15, Marcos, Patineta, -1, 120 → se elimina por cantidad ≤ 0
* 2025-07-15, Lucía, Monopatín, 1, NaN → se elimina por nulos

Salida esperada (data/output/ventas\_limpias.csv):

* Columnas normalizadas: fecha, vendedor, producto, cantidad, precio\_unitario
* Solo filas válidas (cantidad > 0, precio\_unitario > 0, vendedor no vacío y sin nulos)

## 📝 Logging esperado

* logger.info al inicio y fin del pipeline.
* logger.info antes y después de cada transformación (se registra cantidad de filas antes → después).
* logger.error si el archivo de entrada no existe.
  Ejemplo de mensajes:
* \=== Inicio del pipeline ===
* Cargado data/input/ventas\_raw\.csv | filas=5 cols=5
* clean\_column\_names: filas 5 → 5
* drop\_nulls: filas 5 → 4
* remove\_empty\_names: filas 4 → 4
* filter\_positive\_values(cantidad): filas 4 → 3
* filter\_positive\_values(precio\_unitario): filas 3 → 2
* normalize\_product\_names: filas 2 → 2
* Guardado data/output/ventas\_limpias.csv | filas=2 cols=5
* \=== Fin del pipeline ===

## ✅ Checklist (validación del desafío)

* [x] Ejecutable desde consola (CLI con argparse)
* [x] Logging detallado (inicio/fin + antes/después de cada paso)
* [x] Output guardado en data/output/
* [x] Funciones bien nombradas y desacopladas (load.py, transform.py, save.py, logger.py)

## 🧭 Próximos pasos

* Agregar validaciones automáticas (Semana 4)
* Ejecutarlo en AWS (Semana 2)
* Tests unitarios (Semana 8)
* Empaquetado y mejoras de producto
