# Proyecto integrador — Módulo I (MovieLens)

Diplomado *Métodos estadísticos y matemáticos para la ciencia de datos* (DMEMCDM 2026) · Módulo I: Preprocesamiento y técnicas básicas de visualización de datos.

## Objetivo

Análisis exploratorio del dataset MovieLens `ml-latest-small` para responder dos preguntas descriptivas:

1. **Popularidad vs. polarización:** ¿las películas con más calificaciones generan opiniones más divididas?
2. **Afinidades:** si a un usuario le gusta una película o un género (rating ≥ 4), ¿qué otras películas o géneros tienden a gustarle también?

## Datos

`data/raw/` contiene `movies.csv`, `ratings.csv` y el `README.txt` original de `ml-latest-small` (descargado de <https://grouplens.org/datasets/movielens/latest/>). Las tablas `links.csv` y `tags.csv` no se usan y no se incluyen.

**Licencia:** el dataset se usa con fines académicos y no comerciales, y se redistribuye bajo las mismas condiciones de GroupLens (ver `data/raw/README.txt`).

**Cita:**

> F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems (TiiS)* 5, 4: 19:1–19:19. <https://doi.org/10.1145/2827872>

## Cómo reproducir el análisis

1. Clonar la rama del proyecto:
   ```bash
   git clone -b proyecto/data-masters-movielens https://github.com/chaffrey8/DMEMCD_2026.git
   cd DMEMCD_2026
   ```
2. Crear un entorno con Python 3.10 o superior e instalar las dependencias:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate   ·   macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Abrir y ejecutar los notebooks **en orden** (*Restart & Run All*):

   | Notebook | Contenido |
   |---|---|
   | `notebooks/01_comprension_calidad.ipynb` | Descripción de los datos, validaciones y decisiones de limpieza |
   | `notebooks/02_popularidad_polarizacion.ipynb` | Pregunta 1 |
   | `notebooks/03_afinidades_peliculas.ipynb` | Pregunta 2a |
   | `notebooks/04_afinidades_generos.ipynb` | Pregunta 2b |
   | `notebooks/05_fun_facts.ipynb` | Hallazgos complementarios y conclusiones generales |

Las figuras se guardan en `results/figures/` y las tablas en `results/tables/`, incluida la bitácora de limpieza.

## Organización del código

```
src/
├── contratos.py             # columnas esperadas de cada tabla y funciones de verificación
├── rutas.py                 # rutas del proyecto y guardado de resultados
├── carga.py                 # lectura de los CSV con sus tipos
├── limpieza.py              # validaciones y limpieza de movies y ratings
├── polarizacion.py          # tabla por película (pregunta 1)
├── afinidades_peliculas.py  # matriz de gustos usuario × película (pregunta 2a)
└── afinidades_generos.py    # perfil usuario × género (pregunta 2b)
```

Los notebooks contienen el análisis, las visualizaciones y las interpretaciones. `src/` contiene las funciones que producen las tablas que comparten varios notebooks.

## Contribuciones

| Rol | Integrante | Archivos principales |
|---|---|---|
| Datos y calidad | Andrea Paulina Ibarra Salazar | `src/limpieza.py`, `notebooks/01_comprension_calidad.ipynb`, `results/tables/bitacora_limpieza.csv` |
| Pregunta 1 | Alan Mendoza Calderón | `src/polarizacion.py`, `notebooks/02_popularidad_polarizacion.ipynb` |
| Pregunta 2a | Jonathan Macario Sampedro | `src/afinidades_peliculas.py`, `notebooks/03_afinidades_peliculas.ipynb` |
| Pregunta 2b | Hugo Salazar Cedillo | `src/afinidades_generos.py`, `notebooks/04_afinidades_generos.ipynb` |
| Fun facts e integración | Andrés Sánchez Rosas | `src/rutas.py`, `src/carga.py`, `notebooks/05_fun_facts.ipynb`, `README.md`, `requirements.txt` |

### Andrea Paulina Ibarra Salazar — Datos y calidad

- Desarrollo de `src/limpieza.py`: función `validar_llave()` y funciones `movies_limpias()` (título sin espacios sobrantes, año de estreno, 18 columnas de género 0/1, bandera `es_imax` y `n_generos`) y `ratings_limpias()` (validación de la escala de ratings, fecha en UTC y año de calificación).
- **Notebook 01 — Comprensión de los datos y calidad:**
  - Procedencia, licencia, contexto, variables y unidad de observación de cada tabla; justificación de no usar `links` y `tags`.
  - Validaciones: valores vacíos, llaves, integridad entre tablas, valores de `rating` y rango de fechas.
  - Análisis de géneros y títulos, y documentación de las decisiones de limpieza 1 a 5 con su evidencia y consecuencias.
  - Distribución de calificaciones por película (`results/figures/01_distribucion_ratings.png`).
- Bitácora de limpieza (`results/tables/bitacora_limpieza.csv`) con las seis decisiones.

### Alan Mendoza Calderón — Pregunta 1

- Desarrollo de `src/polarizacion.py`, implementando la función `stats_peliculas()`, que resume los ratings por película: número de ratings (`n`), media, mediana, desviación estándar muestral (`std`) y rango intercuartílico (`ric`). Aplica el umbral mínimo de ratings (decisión 6) y agrega título y año de estreno. Esta tabla también la usa el notebook 05.
- **Notebook 02 — Pregunta 1 (popularidad vs. polarización):**
  - Justificación del umbral mínimo de ratings por película: con un solo rating la desviación estándar no existe y con pocos es ruido. Tabla de sensibilidad con umbrales de 10, 20, 50 y 100 (películas que quedan y % de ratings conservados). Umbral principal: n ≥ 20 
  - Estadística descriptiva de `n`, `media`, `std` y `ric`.
  - Cálculo de correlaciones de Spearman (medida principal, por la fuerte asimetría de `n`) y de Pearson (comparación) entre n–std, n–media y media–std, para tener en cuenta la media como factor de confusión debido a la escala acotada de 0.5 a 5.
  - Gráfico *hexbin* de `log1p(n)` contra `std`, y *boxplot* de `std` por cuartil de popularidad (`pd.qcut`).
  - Histogramas de los ratings de las tres películas con mayor desviación estándar, para distinguir entre polarización real (dos bandos) y opiniones simplemente dispersas.
  - Análisis de sensibilidad de la correlación n–std con umbrales de 10, 20 y 50 ratings.
  - Interpretación de cada gráfico (qué muestra, por qué es relevante y limitaciones) y conclusión: no se encontró relación entre popularidad y polarización, resultado que se mantiene con los otros umbrales.
  - Exportación de las figuras (`02_hexbin_n_std`, `02_boxplot_std_popularidad`, `02_histogramas_polemicas`) y de las tablas `02_*` a `results/`.

### Jonathan Macario Sampedro — Pregunta 2a

- Desarrollo de `src/afinidades_peliculas.py`, implementando la función `matriz_gustos()` para construir una matriz usuario-película a partir de las calificaciones.
- Filtrado de películas con al menos 100 calificaciones para trabajar con observaciones suficientes.
- Transformación de las calificaciones en una variable binaria de aceptación: 1 si la calificación es igual o superior a 4 y 0 en caso contrario, conservando los valores faltantes como `NaN`.
- Análisis de las diferencias en los hábitos de calificación de los usuarios mediante el porcentaje de películas que calificaron con 4 o más.
- Cálculo de correlaciones de Pearson entre películas, utilizando un mínimo de 20 observaciones compartidas.
- Identificación y ordenamiento de las parejas de películas con mayor correlación, incorporando sus títulos.
- Elaboración de un mapa de calor (*heatmap*) para visualizar las afinidades entre las películas más reseñadas.
- Comparación de las probabilidades condicionadas \(P(Y=1 \mid X=1)\) con las probabilidades generales \(P(Y=1)\) para las cinco parejas con mayor correlación.
- Interpretación de los resultados y documentación de las limitaciones del análisis, incluyendo el sesgo de calificación, los datos faltantes y la interpretación de las correlaciones.

### Hugo Salazar Cedillo — Pregunta 2b

- Desarrollo de `src/afinidades_generos.py`, implementando la función `perfil_genero()` para construir una matriz usuario+generos a partir de las calificaciones.
- Elaboración de tabla resumen con número de películas, númer de ratings, media de ratings, mediana de ratings y std de raitings agrupada por género.
- Elaboración de BoxPlot para la visualización de ratings por género.
- Elaboración de las matrices de correlación (coocurrencia y preferenica).
- Elaboración de los mapas de calor para visualizar las diferencias entre las correlaciones de coocurrencia y preferencia.
- Elaboración de gráfico scatterplot para visualizar la relación entre las correlaciones de coocurrencia y preferencias.
- Interpretación de los resultados y documentación de las limitaciones del análisis, incluyendo el sesgo de calificación y la interpretación de la relación entre las correlaciones de coocurrencia y preferencia.

### Andrés Sánchez Rosas — Fun facts e integración

- **Estructura del repositorio:** estructura de carpetas y plantillas de los notebooks, que permitieron al equipo trabajar en paralelo.
- **`src/rutas.py`:** rutas del proyecto y funciones `guardar_figura()` (acepta una Figure, un Axes o un FacetGrid de seaborn) y `guardar_tabla()`, usadas por todos los notebooks para exportar resultados.
- **`src/carga.py`:** lectura de `movies.csv` y `ratings.csv` con tipos explícitos (`userId` y `movieId` como texto, `rating` como real y `timestamp` como entero).
- **Notebook 05 — Fun facts:**
  - Función reutilizable `worst_best_n_movies()` para ordenar la tabla de la pregunta 1 por cualquier métrica. Con ella se obtienen las mejores y peores películas de todos los tiempos (n ≥ 20), las mejores y peores por década de estreno y las 10 más polémicas (mayor desviación estándar).
  - Número de ratings por género (una película con varios géneros cuenta en cada uno).
  - Serie de tiempo de ratings por año de calificación, con el año de mayor actividad y la mayor caída señalados automáticamente (`results/figures/05_ratings_por_anio.png`).
- **Documentación y reproducibilidad:** `README.md` (objetivo, datos, licencia, cita e instrucciones para reproducir), `requirements.txt` y este registro de contribuciones.

### Trabajo conjunto

- Contratos de datos (`src/contratos.py`): todo el equipo.
- Video de exposición: todo el equipo.
