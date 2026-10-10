# INF-8239 · U03.E05 — Motor recomendador reproducible (LAB08 + LAB09)

**Asignatura:** Ciencia de Datos II · UASD  
**Práctica:** Popularidad, contenido, factorización, ranking offline y recomendación híbrida (MovieLens Latest Small)  
**Repositorio:** https://github.com/mannixmueses-cloud/INF8239_U03

Proyecto académico basado en la plantilla proporcionada para LAB08/LAB09. LAB09 se debe realizar **después** de LAB08, con el mismo conjunto MovieLens, sin publicar sus archivos de datos.

## Requisitos
Python 3.12, Git y `uv`. Desde la carpeta raíz del proyecto:

```powershell
uv python install 3.12
uv run python --version
uv sync
uv run pytest -q
```

## Datos y auditoría
Si los datos **ya están descargados** en `data/raw/ml-latest-small/`, **no** se requiere otra descarga. Si se ejecuta en un equipo limpio:

```powershell
uv run python scripts/download_data.py
uv run python scripts/audit_data.py
```

Fuente: MovieLens Latest Small, GroupLens; respetar su licencia y condiciones. Los archivos bajo `data/raw/` están excluidos por `.gitignore` y no se redistribuyen.

## Experimento LAB08

```powershell
uv run python scripts/lab08_content.py
```

Imprime el Top-10 de popularidad y tres consultas por contenido (Toy Story, Shawshank Redemption y Matrix), y las guarda en `reports/content_recommendations_1..3.csv`. Si un título no existe, devuelve el Top-10 de popularidad como respaldo. También acepta títulos como argumentos, por ejemplo `uv run python scripts/lab08_content.py "Titanic (1997)"`.

## Experimento LAB09

```powershell
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.25
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75
uv run python scripts/lab09_hybrid.py --alpha 0.25 --seed 11 --output lab09_seed11_alpha0_25.json
uv run python scripts/lab09_hybrid.py --alpha 0.75 --seed 11 --output lab09_seed11_alpha0_75.json
uv run python scripts/lab09_hybrid.py --alpha 0.25 --seed 42 --output lab09_seed42_alpha0_25.json
uv run python scripts/lab09_hybrid.py --alpha 0.75 --seed 42 --output lab09_seed42_alpha0_75.json
uv run python scripts/lab09_hybrid.py --alpha 0.25 --seed 73 --output lab09_seed73_alpha0_25.json
uv run python scripts/lab09_hybrid.py --alpha 0.75 --seed 73 --output lab09_seed73_alpha0_75.json
uv run python scripts/lab09_pareto.py
uv run pytest tests/test_matrix_factorization.py tests/test_metrics.py -q
```

Las seis corridas repiten las dos configuraciones (alpha 0.25 y 0.75) con las semillas 11, 42 y 73 y escriben `reports/lab09_seed*_alpha*.json`. `lab09_hybrid.py` también produce `reports/cold_start_fallback.csv`. `lab09_pareto.py` lee esas corridas y escribe `reports/pareto_hibrido.csv`.

La comparación de los seis modelos (popularidad, contenido, colaborativo e híbrido con la misma partición) se hizo con un script exploratorio que no forma parte de la entrega. Sus resultados se conservan como evidencia en `reports/comparacion_modelos.csv`, `comparacion_modelos_resumen.csv`, `comparacion_perfiles.csv` y `usuario_frio.json`, pero no se regeneran con los comandos de este repositorio. Si `comparacion_modelos_resumen.csv` existe, `lab09_pareto.py` también escribe `reports/pareto_modelos.csv`.

## Tabla principal de resultados
Media de tres semillas (11, 42 y 73), top-10, 587 usuarios evaluados.

| Modelo | HitRate@10 (IC95 %) | Cobertura | RMSE | Costo total (s) | Pareto |
|---|---|---|---|---|---|
| Popularidad por cantidad | 4.3 % (2.9–6.2) | 1.2 % | n/a | 0.005 | No dominado |
| Popularidad ponderada | 3.2 % (2.1–5.0) | 0.6 % | n/a | 0.002 | Dominado por popularidad por cantidad |
| Contenido (perfil de géneros) | 0.2 % (0.0–1.0) | 7.8 % | n/a | 3.1 | No dominado |
| Colaborativo (factorización) | 3.4 % (2.2–5.1) | 7.5 % | 1.028 | 44.0 | No dominado |
| Híbrido, alpha 0.25 | 3.1 % (2.0–4.9) | 10.6 % | 1.028 | 48.2 | No dominado |
| Híbrido, alpha 0.75 | 3.3 % (2.1–5.1) | 7.9 % | 1.028 | 48.8 | No dominado |

Evidencia: `reports/comparacion_modelos_resumen.csv` (comparación exploratoria, ver LAB09) y `reports/pareto_modelos.csv`. Las filas del híbrido se pueden contrastar con `reports/lab09_seed*_alpha*.json`, que sí se regeneran. Los tiempos varían entre corridas.

## Cómo interpretar
- **RMSE:** error de valoración (menor suele ser mejor).
- **HitRate@10:** fracción de usuarios cuyo ítem retenido aparece en Top-10 (mayor es mejor).
- **Precision@10:** con una sola película retenida por usuario, es HitRate@10/10.
- **Cobertura:** variedad de películas distintas recomendadas respecto al catálogo entrenado.
- **Pareto:** `scripts/lab09_pareto.py` marca un modelo como dominado si otro tiene igual o mejor HitRate@10 y cobertura con igual o menor costo en segundos, y es estrictamente mejor en algo. Costos que difieren menos de 1 s se consideran iguales por el ruido de tiempo. Escribe `reports/pareto_hibrido.csv` y `reports/pareto_modelos.csv`.
- **Usuarios nuevos:** popularidad, fallback no personalizado.

## Documentación
- `docs/DATASET_CARD.md`: fuente, versión, hash, condiciones de uso y limitaciones del dataset.
- `docs/SYSTEM_CARD.md`: propósito, modelos, evaluación, cold start, riesgos y costo.
- `docs/USO_IA.md`: declaración de herramientas de IA, verificaciones y correcciones.
- `notebooks/09_comparacion_hibrido.ipynb`: notebook ejecutado de la comparación del híbrido.

## Limitaciones
La selección de candidatos del híbrido procede de los 100 títulos colaborativos principales. El corte es por última interacción de cada usuario y no asegura una frontera temporal global. La RMSE omite valoraciones test de películas desconocidas al modelo. No se infieren diferencias demográficas. El tiempo depende del equipo.

## Cierre interpretativo · LAB08

### Resultado principal
La línea base de popularidad produce un Top-10 de clásicos muy valorados (Shawshank Redemption 4.40, The Godfather 4.24, Fight Club 4.23 según weighted_score), igual para todos los usuarios. El recomendador por contenido devuelve películas coherentes en género con la semilla (Toy Story, Shawshank, Matrix), pero con empates totales (content_score 1.0), por lo que su orden interno es arbitrario.

### Evidencia utilizada
Dataset Card, hash SHA-256 696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436, auditoría de MovieLens (100,836 ratings, 9,742 películas, 610 usuarios, 9,724 ítems valorados, densidad 1.70 %), Top-10 de popularidad, tres consultas por contenido (Toy Story 1995, Shawshank Redemption 1994, Matrix 1999), una consulta con título inexistente, 9 pruebas en verde (10 tras añadir la prueba del respaldo), README y esta conclusión.

### Qué representa la similitud
La similitud representa coincidencia de géneros entre películas, no gustos de usuarios. Dos películas son similares si comparten las mismas etiquetas de género. No incorpora ratings, sinopsis, época ni calidad.

### Problema de cold start observado
Al consultar un título que no está en el catálogo ("Pelicula Inventada (2030)"), el recomendador original lanzaba un KeyError y no ofrecía alternativa, ni siquiera el Top-10 de popularidad. Se corrigió con `ContentRecommender.recommend_or_popular`: ahora un título desconocido recibe el Top-10 de popularidad ponderada (columna `source = popularidad`). El modelo sigue sin personalizar para usuarios sin historial.

### Riesgo de sobre-especialización
En las tres consultas, los 10 resultados repiten exactamente los géneros de la semilla con content_score 1.0. No hay variedad, no se distingue calidad dentro del empate y aparecen títulos poco conocidos que comparten etiqueta pero no necesariamente gusto (por ejemplo, Tattooed Life para Shawshank). El usuario recibe más de lo mismo.

### Decisión o siguiente experimento
Se añadió el respaldo a popularidad cuando el título no existe (prueba `test_unknown_title_falls_back_to_popularity`). La combinación de contenido con señal colaborativa y su comparación con popularidad se hizo en LAB09 (ver el cierre siguiente).

## Cierre interpretativo · LAB09 (Ejercicio 05)

### Resultado de ratings
La factorización (20 factores, 12 épocas) obtuvo un RMSE de 1.025, 1.026 y 1.033 en las semillas 11, 42 y 73 (media 1.028), estable entre corridas. El RMSE no cambia con alpha porque alpha solo afecta el ranking. Es cercano a la desviación estándar de los ratings (1.04 en la auditoría), por lo que la mejora sobre predecir un valor constante es pequeña. Popularidad y contenido no predicen ratings, por lo que no tienen RMSE.

### Resultado de ranking
Con 587 usuarios y la partición temporal leave-one-out, el HitRate@10 medio fue: popularidad por cantidad 4.3 % (IC95 2.9–6.2), colaborativo 3.4 % (2.2–5.1), híbrido alpha 0.75 3.3 %, híbrido alpha 0.25 3.1 % (2.0–4.9), popularidad ponderada 3.2 % y contenido 0.2 %. La precision@10 es HitRate/10 (0.003 a 0.004). Los intervalos se solapan: el modelo personalizado no demuestra superar a popularidad, ni quedar por debajo de ella.

### Cobertura del catálogo
Popularidad por cantidad cubre 1.2 % del catálogo, la ponderada 0.6 %, contenido 7.8 %, colaborativo 7.5 %, híbrido alpha 0.75 7.9 % y alpha 0.25 10.6 %, unas 8.7 veces la cobertura de popularidad. Dar más peso al contenido (alpha 0.25 frente a 0.75) aumentó la cobertura relativa alrededor de un 35 % en las tres semillas, con un hit rate equivalente.

### Comportamiento del usuario frío
Como todos los usuarios del conjunto tienen historial, se simuló un usuario nuevo: recibe el Top-10 por cantidad y media, que acierta el 2.0 % (12 de 587 usuarios) y cubre el 0.1 % del catálogo, porque todos reciben las mismas 10 películas. Con poco historial, popularidad (5.6 %) y el híbrido alpha 0.25 (5.4 %) rinden de forma similar y mejor que el colaborativo solo (3.7 %), aunque con unos 197 usuarios por grupo la diferencia es una tendencia.

### Configuración seleccionada y evidencia
Se selecciona el híbrido (factors=20, epochs=12, alpha=0.25) con popularidad por cantidad como respaldo. Con HitRate@10, cobertura y costo total (tolerancia de 1 s), cinco de seis modelos quedan en el frente de Pareto; solo popularidad ponderada es dominada por popularidad por cantidad. Como ningún otro modelo domina a otro, la elección depende de la prioridad: popularidad tiene el mayor hit rate nominal pero cubre el 1.2 % del catálogo; el híbrido alpha 0.25 cubre el 10.6 %, con una diferencia de hit rate no concluyente (unos 7 de 587 usuarios). Evidencia: reports/pareto_modelos.csv.

### Costo computacional
Entrenar toma unos 20 s en CPU y el modelo ocupa 1,649,760 bytes. El costo total de entrenar y recomendar a 587 usuarios es de 44 s con el colaborativo y 48 s con el híbrido; popularidad tarda milisegundos y contenido unos 3 s. Los tiempos varían entre corridas.

### Riesgo principal y mitigación
El motor personalizado cuesta decenas de segundos y no demuestra acertar más que el baseline de popularidad, mientras que popularidad concentra las recomendaciones en 10 títulos. El híbrido reordena únicamente los 100 mejores candidatos del colaborativo, lo que limita su cobertura (entre 8 % y 11 %). Mitigación: mantener popularidad como respaldo y línea base de referencia, usar alpha bajo, ampliar los candidatos y evaluar con más de un ítem retenido por usuario.