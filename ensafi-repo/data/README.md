# Datos: ENSAFI 2023 (INEGI)

Esta carpeta contiene los microdatos de la **Encuesta Nacional sobre Salud Financiera (ENSAFI) 2023**, levantada por el INEGI en colaboración con la CONDUSEF.

| Archivo | Unidad de observación | Filas | Columnas | Factor de expansión |
|---|---|---:|---:|---|
| `TVIVIENDA.csv` | Vivienda | 20,201 | 36 | `FAC_VIV` |
| `THOGAR.csv` | Hogar | 20,448 | 55 | `FAC_HOG` |
| `TSDEM.csv` | Persona (todos los integrantes del hogar) | 67,781 | 25 | `FAC_HOG` |
| `TMODULO.csv` | Persona elegida (18 años o más, una por hogar) | 20,448 | 253 | `FAC_ELE` |

Formato: CSV, UTF-8 con BOM, separado por comas. Los archivos se usan **sin ninguna modificación**, tal como los publica el INEGI.

## Cómo obtenerlos desde la fuente original

1. Entra a la página del programa: <https://www.inegi.org.mx/programas/ensafi/2023/>
2. En la sección **Microdatos / Datos abiertos**, descarga los archivos en formato CSV.
3. Descomprime y copia `TVIVIENDA.csv`, `THOGAR.csv`, `TSDEM.csv` y `TMODULO.csv` en esta carpeta `data/`.

El notebook busca los CSV automáticamente en `../data`, `data/` o en la carpeta actual, incluidas sus subcarpetas, así que el nombre de la subcarpeta del ZIP no importa.

Documentación (cuestionario, descriptor de archivos, nota técnica): <https://www.inegi.org.mx/programas/ensafi/2023/#documentacion>

## Licencia y condiciones de uso

La información del INEGI se distribuye bajo los **Términos de Libre Uso de la Información del INEGI** (<https://www.inegi.org.mx/inegi/terminos.html>), que permiten copiarla, redistribuirla y crear trabajos derivados siempre que se **cite la fuente**:

> INEGI. Encuesta Nacional sobre Salud Financiera (ENSAFI) 2023. Microdatos. <https://www.inegi.org.mx/programas/ensafi/2023/>

Los microdatos son anónimos; el INEGI garantiza la confidencialidad de los informantes (Art. 37 de la Ley del SNIEG).
