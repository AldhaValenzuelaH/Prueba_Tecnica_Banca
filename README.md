# Prueba Técnica - Practicante Data Engineer

Pipeline de datos end-to-end que ingiere, limpia y transforma datos de clientes, 
productos y pedidos, siguiendo una arquitectura de capas (RAW → STAGE → ANALYTICS) 
sobre una base de datos local DuckDB.

## Stack utilizado

- **Python 3.9** + Pandas para manipulación y limpieza de datos
- **DuckDB** como base de datos local (capa On-Premise)
- **Seaborn / Matplotlib** para visualizaciones
- **Jupyter Notebooks** como entorno de desarrollo y entregable
- **Git** para control de versiones

## Estructura del proyecto
```
prueba-tecnica-lakehouse/

├── data/raw/              # CSVs originales (no versionados en Git)

├── notebooks/

│   ├── 01_ingesta.ipynb       # Carga de CSVs a capa RAW

│   ├── 02_limpieza.ipynb      # Transformación RAW → STAGE

│   ├── 03_capa_analytics.ipynb # Construcción de FACT/DIM

│   ├── 04_reporte.ipynb       # Visualizaciones de negocio

│   └── 05_practica_sql.ipynb  # Queries de análisis (Paso 5)

├── lakehouse.duckdb        # Base de datos DuckDB (generada al correr 01)

├── .gitignore

└── README.md
```

## Cómo ejecutar el proyecto

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas duckdb seaborn matplotlib jupyter

# Ejecutar los notebooks en orden: 01 → 02 → 03 → 04 → 05
```

## Arquitectura de capas

- **RAW**: datos originales tal como llegan, sin ninguna transformación.
- **STAGE**: datos limpios (sin duplicados, sin nulos totales, tipos correctos, 
  fechas normalizadas, valores inválidos tratados).
- **ANALYTICS**: tablas finales listas para consumo (FACT y DIM), con métricas 
  calculadas, listas para un dashboard o análisis directo.

## Decisiones de limpieza relevantes

- Se detectaron 3 formatos de fecha distintos (`YYYY-MM-DD`, `DD/MM/YYYY`, 
  `MM-DD-YYYY`) y se implementó un parser que prueba cada formato antes de 
  descartar un valor como inválido, evitando pérdida innecesaria de datos.
- Valores estructuralmente imposibles (precios negativos, descuentos >100%, 
  edades fuera de rango) se trataron caso por caso: se eliminó la fila cuando 
  el dato roto invalidaba el registro completo (ej. precio negativo), o se 
  marcó como nulo cuando el resto de la fila seguía siendo válido (ej. edad).

## Esquema de la capa ANALYTICS

### DIM_CLIENTE
| Columna | Tipo | Descripción |
|---|---|---|
| customer_id | INTEGER | Identificador único del cliente |
| full_name | VARCHAR | Nombre completo |
| email | VARCHAR | Correo electrónico |
| city | VARCHAR | Ciudad de residencia |
| age | INTEGER | Edad del cliente |
| registration_date | DATE | Fecha de registro |

### DIM_PRODUCTO
| Columna | Tipo | Descripción |
|---|---|---|
| product_id | INTEGER | Identificador único del producto |
| product_name | VARCHAR | Nombre del producto |
| category | VARCHAR | Categoría del producto |
| price | DOUBLE | Precio unitario |

### FACT_CLIENTE
| Columna | Tipo | Descripción |
|---|---|---|
| customer_id | INTEGER | FK a DIM_CLIENTE |
| total_pedidos | INTEGER | Cantidad de pedidos del cliente |
| monto_total_gastado | DOUBLE | Suma total gastada |
| ticket_promedio | DOUBLE | Promedio de gasto por pedido |
| fecha_ultimo_pedido | DATE | Fecha del pedido más reciente |

### FACT_PRODUCTO
| Columna | Tipo | Descripción |
|---|---|---|
| product_id | INTEGER | FK a DIM_PRODUCTO |
| unidades_vendidas | DOUBLE | Total de unidades vendidas |
| ingresos_totales | DOUBLE | Ingresos generados por el producto |
| num_pedidos | INTEGER | Cantidad de pedidos con este producto |

## Autor

Aldhair Valenzuela Huillcaya
