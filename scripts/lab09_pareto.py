"""Pareto de LAB09: marca configuraciones y modelos dominados.

Ejecutar desde la raíz: uv run python scripts/lab09_pareto.py
Lee reports/lab09_seed*_alpha*.json (generados por scripts/lab09_hybrid.py) y, si existe,
reports/comparacion_modelos_resumen.csv (comparación de popularidad, contenido,
colaborativo e híbrido). Objetivos: maximizar HitRate@10 y cobertura; minimizar el costo
en segundos. Costos que difieren menos de COST_TOL segundos se consideran iguales,
porque el tiempo de ejecución varía entre corridas.
"""
from __future__ import annotations

import json

import pandas as pd

from inf8239_u03.config import ROOT

REPORTS = ROOT / "reports"
COST_TOL = 1.0


def mark_pareto(table: pd.DataFrame, cost_column: str, label_column: str) -> pd.DataFrame:
    """Añade dominado_por y pareto_optimo: dominado = otro no es peor en nada y mejora algo."""
    table = table.reset_index(drop=True).copy()
    dominated_by = []
    for i, row in table.iterrows():
        culprit = ""
        for j, other in table.iterrows():
            if i == j:
                continue
            no_worse = (
                other["hit_rate_at_10"] >= row["hit_rate_at_10"]
                and other["catalog_coverage"] >= row["catalog_coverage"]
                and other[cost_column] <= row[cost_column] + COST_TOL
            )
            better = (
                other["hit_rate_at_10"] > row["hit_rate_at_10"]
                or other["catalog_coverage"] > row["catalog_coverage"]
                or other[cost_column] < row[cost_column] - COST_TOL
            )
            if no_worse and better:
                culprit = str(other[label_column])
                break
        dominated_by.append(culprit)
    table["dominado_por"] = dominated_by
    table["pareto_optimo"] = table["dominado_por"].eq("")
    return table


pd.set_option("display.width", None, "display.max_columns", None)

# 1) Configuraciones del híbrido (promedio entre semillas)
files = sorted(REPORTS.glob("lab09_seed*_alpha*.json"))
if not files:
    raise SystemExit("No hay corridas lab09_seed*_alpha*.json; ejecute primero scripts/lab09_hybrid.py")
runs = pd.DataFrame([json.loads(path.read_text(encoding="utf-8")) for path in files])
configs = (
    runs.groupby(["factors", "epochs", "alpha"])
    .agg(
        semillas=("seed", "nunique"),
        rmse=("rmse", "mean"),
        hit_rate_at_10=("hit_rate_at_10", "mean"),
        catalog_coverage=("catalog_coverage", "mean"),
        train_seconds=("train_seconds", "mean"),
        model_kb=("model_size_bytes", lambda sizes: sizes.mean() / 1024),
    )
    .reset_index()
)
configs["config"] = [
    f"f{int(r.factors)}_e{int(r.epochs)}_a{r.alpha:.2f}" for r in configs.itertuples()
]
configs = mark_pareto(configs, "train_seconds", "config")
configs.to_csv(REPORTS / "pareto_hibrido.csv", index=False)
print(f"Pareto de configuraciones del híbrido (costo = segundos de entrenamiento, tolerancia {COST_TOL} s):\n")
print(configs.round(4).to_string(index=False))

# 2) Modelos (popularidad, contenido, colaborativo, híbrido), si existe el resumen
summary_path = REPORTS / "comparacion_modelos_resumen.csv"
if summary_path.exists():
    models = pd.read_csv(summary_path)[["modelo", "hit_rate_at_10", "catalog_coverage", "costo_total_seconds"]]
    models = mark_pareto(models, "costo_total_seconds", "modelo")
    models.to_csv(REPORTS / "pareto_modelos.csv", index=False)
    print("\nPareto de modelos (costo = entrenar + recomendar, en segundos):\n")
    print(models.round(4).to_string(index=False))
else:
    print("\nNo existe reports/comparacion_modelos_resumen.csv; solo se evaluó el híbrido.")