

---


```markdown
# 🧪 mi_primer_pipeline

Pipeline local en **Python** para **limpieza y validación de datos de ventas**.  
Incluye modularización, ejecución por **CLI**, y **logging** estructurado.  
Forma parte del **Desafío Semana 1** (Data Engineering).

---

## 🚀 Objetivo
Tomar un CSV crudo de ventas, aplicar transformaciones mínimas y guardar un CSV limpio para análisis.

**Transformaciones implementadas:**
- `clean_column_names()` — normaliza nombres de columnas (minúsculas, sin tildes, sin espacios)
- `drop_nulls()` — elimina filas con valores nulos
- `remove_empty_names()` — elimina filas sin nombre de vendedor
- `filter_positive_values(col)` — filtra filas con `cantidad` o `precio_unitario` ≤ 0
- `normalize_product_names()` — normaliza nombres de producto (minúsculas, sin tildes)

---

## 📂 Estructura
```

mi\_primer\_pipeline/
├── data/
│   ├── input/                  # CSVs originales
│   │   └── ventas\_raw\.csv
│   └── output/                 # CSVs procesados
│       └── ventas\_limpias.csv
├── pipeline/
│   ├── load.py                 # load\_csv()
│   ├── save.py                 # save\_csv()
│   └── transform.py            # funciones de transformación
├── utils/
│   └── logger.py               # get\_logger()
├── main.py                     # orquestación + CLI
├── requirements.txt
└── README.md

````

---

## 🧰 Requisitos
- Python 3.10+
- venv activo
- Paquetes de `requirements.txt`

---

## ⚙️ Instalación rápida
```bash
# 1) crear/activar venv (Windows)
python -m venv .venv
.\.venv\Scripts\Activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# 2) instalar dependencias
pip install -r requirements.txt
````

---

## ▶️ Uso (CLI)

Ejecutar con rutas explícitas:

```bash
python main.py --input data/input/ventas_raw.csv --output data/output/ventas_limpias.csv
```

**Ejemplo de error controlado** (input inexistente):

```bash
python main.py --input data/input/no_existe.csv --output data/output/ventas_limpias.csv
# -> logger.error(...) y salida con código 1
```

---

## 🧪 Datos de ejemplo (para `data/input/ventas_raw.csv`)

```csv
Fecha,Vendedor,Producto,Cantidad,Precio Unitario
2025-07-15,Ana,Bicicleta,2,350
2025-07-15,,Bicicleta,1,350
2025-07-15,Marcos,Patineta,-1,120
2025-07-15,Lucía,Monopatín,1,NaN
2025-07-16,Pedro,Patín Electrico,3,500
```

**Salida esperada** (`data/output/ventas_limpias.csv`): solo filas válidas, columnas normalizadas:

```
fecha,vendedor,producto,cantidad,precio_unitario
...
```

---

## 📝 Logging esperado

* `logger.info()` al inicio/fin y antes/después de cada transformación
* `logger.error()` si el archivo de entrada no existe

Salida típica:

```
YYYY-MM-DD HH:MM:SS | INFO | pipeline | === Inicio del pipeline ===
YYYY-MM-DD HH:MM:SS | INFO | pipeline.load | Cargado data/input/ventas_raw.csv | filas=5 cols=5
YYYY-MM-DD HH:MM:SS | INFO | pipeline | clean_column_names: filas 5 -> 5
YYYY-MM-DD HH:MM:SS | INFO | pipeline | drop_nulls: filas 5 -> 4
YYYY-MM-DD HH:MM:SS | INFO | pipeline | remove_empty_names: filas 4 -> 4
YYYY-MM-DD HH:MM:SS | INFO | pipeline | filter_positive_values(cantidad): filas 4 -> 3
YYYY-MM-DD HH:MM:SS | INFO | pipeline | filter_positive_values(precio_unitario): filas 3 -> 2
YYYY-MM-DD HH:MM:SS | INFO | pipeline | normalize_product_names: filas 2 -> 2
YYYY-MM-DD HH:MM:SS | INFO | pipeline.save | Guardado data/output/ventas_limpias.csv | filas=2 cols=5
YYYY-MM-DD HH:MM:SS | INFO | pipeline | === Fin del pipeline ===
```

---

## ✅ Checklist (validación del desafío)

* [x] Ejecutable desde consola (CLI con `argparse`)
* [x] Logging detallado (inicio/fin + antes/después de cada paso)
* [x] Output guardado en `data/output/`
* [x] Funciones bien nombradas y desacopladas (`load.py`, `transform.py`, `save.py`, `logger.py`)

---

## 🧭 Próximos pasos

* Validaciones automáticas (Semana 4)
* Ejecución en AWS (Semana 2)
* Tests unitarios (Semana 8)
* Empaquetado y mejoras de producto

---

````

---

# requirements.txt (final)

```txt
pandas>=2.0
Unidecode>=1.3
````

---

# (Opcional) Atajos para correr por defecto

## Windows — `run_pipeline.bat`

Guárdalo en la raíz del repo:

```bat
@echo off
REM Activa venv si hace falta (opcional)
IF NOT DEFINED VIRTUAL_ENV (
  call .\.venv\Scripts\activate
)

python main.py --input data\input\ventas_raw.csv --output data\output\ventas_limpias.csv
```

Ejecutás con doble click o:

```powershell
.\run_pipeline.bat
```

## Linux/Mac — `run_pipeline.sh`

```bash
#!/usr/bin/env bash
source .venv/bin/activate 2>/dev/null || true
python main.py --input data/input/ventas_raw.csv --output data/output/ventas_limpias.csv
```

Y luego:

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

# Último paso: commitear y subir

```bash
git add README.md requirements.txt run_pipeline.bat run_pipeline.sh
git commit -m "README + requirements + scripts de ejecución"
git push
```


