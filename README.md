# INF-8239 · Unidad 03 · Sistemas recomendadores

Autor académico: Edwin Ramón José Nolasco

Proyecto inicial de LAB08 y LAB09. El dataset de muestra prueba el código; la evidencia final usa MovieLens.

## Inicio
```bash
uv python install 3.12
uv sync
uv run pytest -q
uv run python scripts/download_data.py
uv run python scripts/audit_data.py
```

## Laboratorios
```bash
uv run python scripts/lab08_content.py
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75
uv run streamlit run app/streamlit_app.py
```

## Interpretación
No presente una recomendación como verdad. Documente datos, candidatos, puntuación, métricas, fallback y límites.

## Resultado principal:
El recomendador por contenido (LAB08) devuelve Top-10 coherentes en género. Para
"Toy Story (1995)" recomienda títulos de animación familiar como Toy Story 2,
Antz y Monsters, Inc. Los 10 resultados tienen content_score = 1.0, por lo que
el orden entre ellos es arbitrario y no hay un ranking real.

## Evidencia utilizada:
Dataset Card y hash de MovieLens SHA-256  696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436, auditoría de datos,
Top-10 de popularidad, tres consultas por contenido [COMPLETAR: Toy Story (1995),
título 2, título 3], pruebas  4 pruebas, resultado, README y salida
de scripts/lab08_content.py.

## Qué representa la similitud:
La similitud coseno mide cuánto se parecen dos películas en los atributos de
contenido usados (géneros). Un valor de 1.0 significa que tienen exactamente el
mismo perfil de géneros, no que sean igual de buenas ni que le gusten al mismo
usuario. Dos películas con los mismos géneros empatan aunque su calidad,
popularidad o estilo sean muy distintos.

## Problema de cold start observado:
[COMPLETAR con lo que probaste en LAB09 / usuarios fríos]. El enfoque por
contenido sí puede recomendar películas nuevas sin ratings, porque solo usa sus
atributos. Pero para un usuario nuevo sin historial no hay perfil que comparar,
y hay que recurrir a popularidad o a una consulta explícita (una película base).

## Riesgo de sobre-especialización:
Al depender solo de géneros, el sistema recomienda siempre lo mismo que la
película consultada: poca diversidad, sin novedad ni serendipia, y películas
poco conocidas que entran solo por el empate en 1.0. Esto se ve en los 10
resultados idénticos en score.

## Decisión o siguiente experimento:
1) Desempatar por popularidad o promedio de rating ponderado por número de
votos. 2) Añadir más señal de contenido (tags, genome scores, año) con TF-IDF.
3) Combinar contenido con factorización en un modelo híbrido y comparar con la
métrica y la cobertura definidas en el ejercicio, decidiendo con el criterio
Pareto. [COMPLETAR: decisión final y por qué]