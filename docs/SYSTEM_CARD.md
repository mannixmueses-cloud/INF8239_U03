# System Card · Motor recomendador MovieLens (LAB08 + LAB09)

## Usuarios y propósito
Sistema académico de recomendación de películas sobre MovieLens Latest Small. Sirve para comparar métodos offline; no es una aplicación de decisiones críticas y no se ha probado con usuarios reales.

## Catálogo, candidatos y exclusiones
Películas con valoraciones en el conjunto de entrenamiento. Se excluyen las películas ya vistas al generar el Top-10. La última valoración de cada usuario se reserva como prueba; el corte es por usuario, no una frontera temporal global.

## Señales y modelos
- Popularidad: por cantidad y media (línea base y respaldo de usuario nuevo) y ponderada (LAB08).
- Contenido: géneros con TF-IDF y coseno; por película (LAB08) y por perfil de usuario ponderado por rating (LAB09).
- Colaborativo: factorización matricial (20 factores, 12 épocas, tasa de aprendizaje 0.01, regularización 0.05).
- Híbrido: `alpha * colaborativo + (1 - alpha) * contenido`, normalizado entre los 100 mejores candidatos colaborativos. Esto limita la recuperación de títulos solo por contenido.
- Configuración seleccionada: híbrido con alpha 0.25 y popularidad por cantidad como respaldo para usuarios sin historial.

## Evaluación
Leave-one-out temporal por usuario; se evalúan 587 de 610 usuarios (en los demás, la película retenida no aparece en el entrenamiento). Métricas: RMSE, HitRate@10, Precision@10 (= HitRate/10, un ítem retenido por usuario) y cobertura del catálogo. Tres semillas (11, 42, 73).

| Modelo | HitRate@10 | Cobertura | Costo total (s) |
|---|---|---|---|
| Popularidad por cantidad | 4.3 % | 1.2 % | 0.005 |
| Colaborativo | 3.4 % | 7.5 % | 44.0 |
| Híbrido alpha 0.25 | 3.1 % | 10.6 % | 48.2 |
| Híbrido alpha 0.75 | 3.3 % | 7.9 % | 48.8 |

RMSE de la factorización: 1.028. Las diferencias de hit rate equivalen a 2 a 7 usuarios y los intervalos del 95 % se solapan, por lo que no son concluyentes. Estos resultados offline no prueban satisfacción real del público.

## Cold start
Un usuario nuevo no tiene factores colaborativos y recibe el Top-10 por cantidad y media (`reports/cold_start_fallback.csv`). En simulación acierta el 2.0 % (12 de 587 usuarios) y cubre el 0.1 % del catálogo. Con poco historial, popularidad (5.6 %) y el híbrido alpha 0.25 (5.4 %) superan al colaborativo solo (3.7 %), con unos 197 usuarios por grupo (tendencia). Un título fuera del catálogo en la consulta por contenido recibe el Top-10 de popularidad ponderada como respaldo (antes lanzaba un KeyError).

## Riesgos, mitigaciones y monitoreo
- Concentración en lo popular: popularidad cubre solo el 1.2 % del catálogo. Mitigación: alpha bajo y monitoreo de cobertura.
- Sobre-especialización del contenido: devuelve películas con los mismos géneros y puntajes empatados. Mitigación: diversidad de géneros y más de 100 candidatos.
- Sesgo de selección y exposición, y lazo de retroalimentación. No hay demografía para evaluar diferencias entre grupos.
- Monitoreo: cobertura y HitRate@10 frente a la línea base de popularidad en cada reentrenamiento.

## Límite computacional
Entrenar toma unos 20 s en CPU (19.7 a 22.5 s entre repeticiones) y los factores ocupan 1,649,760 bytes (sin memoria auxiliar). Costo total de entrenar y recomendar a 587 usuarios: 44 s el colaborativo y 48 s el híbrido; popularidad, milisegundos.