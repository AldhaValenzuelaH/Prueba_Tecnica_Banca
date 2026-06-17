#!/bin/bash
# Punto de entrada único del pipeline.
# Ejecuta cada notebook en orden: ingesta -> limpieza -> analytics -> reporte.
# "set -e" hace que el script se detenga inmediatamente si algún paso falla,
# en vez de seguir corriendo con un error silencioso.
set -e

echo "Iniciando pipeline completo..."

jupyter nbconvert --to notebook --execute --inplace notebooks/01_ingesta.ipynb
echo "Paso 1 (Ingesta) completado."

jupyter nbconvert --to notebook --execute --inplace notebooks/02_limpieza.ipynb
echo "Paso 2 (Limpieza) completado."

jupyter nbconvert --to notebook --execute --inplace notebooks/03_capa_analytics.ipynb
echo "Paso 3 (Analytics) completado."

jupyter nbconvert --to notebook --execute --inplace notebooks/04_reporte.ipynb
echo "Paso 4 (Reporte) completado."

jupyter nbconvert --to notebook --execute --inplace notebooks/05_practica_SQL_Python.ipynb
echo "Paso 5 (SQL) completado."

echo "Pipeline completo ejecutado sin errores."