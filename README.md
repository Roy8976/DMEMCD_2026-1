# Análisis de los patrones de movilidad urbana: una exploración temporal, espacial y sociodemográfica del sistema ECOBICI en la Ciudad de México

**Proyecto integrador, Módulo I.** Diplomado en Métodos Estadísticos y Matemáticos para la Ciencia de Datos (UNAM)
**Equipo:** Sala 13

* Abril Helena Ortiz Soto
* Aranza Fernanda Ortiz Lozada
* Rodrigo Perez Perez
* Diego Morando Pérez
* Rosalinda Hernández Crotte

## Objetivo

Nuestra pregunta principal es: **¿qué patrones podemos detectar en el uso de ECOBICI como medio de transporte?** En particular, nos interesa conocer los horarios de mayor demanda, las estaciones con mayor actividad y los trayectos más frecuentes entre zonas de la ciudad.

A partir de esta primera pregunta, que nos ayuda a conocer el panorama general de nuestro conjunto de datos, profundizamos en tres aspectos:

* ¿Los patrones de uso cambian de acuerdo con el género registrado de las personas usuarias?
* ¿Podemos identificar comportamientos distintos por grupos de edad?
* ¿Qué relación existe entre la infraestructura de estaciones de ECOBICI y la demanda del servicio?


## Datos

Los datos se extrajeron de fuentes oficiales 
| Dataset | Descripción | Fuente |
|---|---|---|
| ecobici_2026_%% | Cada fila es un viaje de la estación de retiro (A) a la estación de arribo (B), con género, fecha y hora| <https://ecobici.cdmx.gob.mx/en/open-data/> |
| Estaciones | Georreferenciación (nombre, latitud, longitud) de cada estación por ID. | <https://datos.cdmx.gob.mx/dataset/cicloestaciones-ecobici-nuevo-sistema/resource/e764a27c-2043-42e8-a17f-5a04674b0f1b?view_id=91c9d729-4d80-43c3-ac38-f234bdb147ea> |

- **Periodo analizado:** <01/2026 – 03/2026>
- **Unidad de observación:** Viajes por hora

## Procedencia
Datos abiertos de viajes de Ecobici (CDMX), meses 2026-01 a 2026-03.
Fuente: https://ecobici.mx/datos-abiertos/ (consultado el 21/nov/2026).
Se descargan con `src/descarga.py`.

## Licencia y condiciones de uso
El sitio de la fuente no especifica una licencia para los datos históricos.
Los archivos se incluyen sin modificar y con fines académicos, con atribución
a Ecobici como fuente original. Los derechos sobre los datos pertenecen a sus
publicadores.


## Estructura del repositorio

```
ecobici-eda/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/               # datos originales 
├── notebooks/
│   └── 01_eda_ecobici.ipynb
├── Resultados/

## Cómo reproducir el análisis

**Requisitos:** Python 3.12 o superior y Git.

1. Clonar el repositorio:
   ```bash
   https://github.com/Roy8976/DMEMCD_2026-1/tree/proyecto/equipo_sala_13
   cd proyecto_ecobici
   ```
2. Crear y activar un entorno virtual:
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   python --version     # debe mostrar 3.12 o superior       # Windows: .venv\Scripts\activate
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Abrir y ejecutar el notebook completo (*Kernel → Restart & Run All*):
   ```bash
   jupyter lab notebooks/01_eda_ecobici.ipynb
   ```

Las figuras y tablas se guardan en `results/` 

## Contenido del análisis

0. Entorno de ejecución y ubicación de los datos
1. Comprensión de los datos
2. Exploración y estadística descriptiva
3. Calidad, limpieza y transformación
4. Análisis por pregunta de investigación
5. Conclusiones y limitaciones
6. Reproducibilidad

## Resultados principales

<RESUMIR EN 2-3 VIÑETAS LOS HALLAZGOS Y ENLAZAR UNA FIGURA DE `results/figures/`>

## Limitaciones

<EJ.: periodo acotado, registros sin género, no se infiere causalidad>


