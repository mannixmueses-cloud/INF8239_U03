# Dataset Card · MovieLens Latest Small

## Fuente
GroupLens, MovieLens Latest Small: https://grouplens.org/datasets/movielens/latest/
Descarga automatizada por `scripts/download_data.py` desde la URL indicada en `src/inf8239_u03/config.py`.

## Referencia
Harper, F. M., & Konstan, J. A. (2015). *The MovieLens Datasets: History and Context*. ACM Transactions on Interactive Intelligent Systems. https://doi.org/10.1145/2827872

## Datos y diccionario
`ratings.csv`: `userId`, `movieId`, `rating`, `timestamp`. `movies.csv`: `movieId`, `title`, `genres`.

Cantidades reales (auditoría con `scripts/audit_data.py`):
- 100,836 valoraciones y 9,742 películas.
- 610 usuarios y 9,724 películas con al menos una valoración.
- Densidad de la matriz usuario-película: 1.70 %.
- Ratings de 0.5 a 5.0 (media 3.50, desviación estándar 1.04).
- Marcas de tiempo entre 1996 y 2018.

## Versión, fecha y SHA-256
MovieLens Latest Small, descargado con `scripts/download_data.py` el 9 de octubre de 2026.
SHA-256 informado por el script: `696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436`

## Condiciones de uso
Consultar los términos incluidos en el archivo descargado y las condiciones de GroupLens. No redistribuir los CSV de MovieLens en el repositorio: `data/raw/` está excluido por `.gitignore`.

## Partición temporal
Se retiene la última valoración de cada usuario como prueba (leave-one-out por usuario) y el resto es entrenamiento. El corte es por usuario y no asegura una frontera temporal global. Se evalúan 587 de los 610 usuarios; los demás quedan fuera porque su película retenida no aparece en el entrenamiento.

## Limitaciones
Interacciones observadas por autoselección y sesgo de exposición; no permiten generalizar a toda la población. No hay atributos demográficos utilizables para evaluar equidad entre grupos.