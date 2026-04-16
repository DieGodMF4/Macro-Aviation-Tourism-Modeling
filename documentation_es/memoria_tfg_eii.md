# Análisis y Modelización del Impacto del Crecimiento Aéreo y Económico de Polonia en los Flujos Turísticos Europeos

## Trabajo de Fin de Grado

**TITULACIÓN:** Grado en Ciencia e Ingeniería de Datos  
**AUTOR:** Diego Marrero Ferrera  
**TUTORIZADO POR:** Juan María Hernández Guerra
**Fecha:** Junio de 2026

Universidad de Las Palmas de Gran Canaria — Escuela de Ingeniería Informática (EII)

---

## Resumen

El presente Trabajo de Fin de Grado aborda la modelización y predicción de la demanda turística internacional en Polonia, medida como el número mensual de pernoctaciones de turistas extranjeros en establecimientos de alojamiento turístico. Polonia se ha consolidado en las dos últimas décadas como una de las economías de mayor crecimiento en Europa, con un incremento quintuplicado del tráfico aeroportuario desde su adhesión a la Unión Europea en 2004 y un nivel de precios aproximadamente un 30 % inferior a la media comunitaria, lo que la convierte en un caso representativo del auge económico y turístico de Europa del Este.

El trabajo integra datos armonizados de Eurostat — índices de precios al consumo (HICP), tipos de cambio bilaterales, PIB real, indicadores de confianza del consumidor y capacidad aérea — procedentes de nueve mercados emisores europeos, y sigue una aproximación progresiva de complejidad creciente: modelos estadísticos clásicos (SARIMA, Holt-Winters), algoritmos de aprendizaje automático (Random Forest, XGBoost), redes neuronales recurrentes (LSTM con variables exógenas) y modelos bayesianos (*Bayesian Structural Time Series* y *Bayesian Model Averaging*). La evaluación comparativa emplea métricas estándar (RMSE, MAE, MAPE) y el test de Diebold-Mariano, complementada con un análisis de impacto causal del COVID-19 mediante el marco *CausalImpact*.

Adicionalmente, el trabajo incorpora un enfoque de predicción bajo escenarios, en el que las proyecciones del modelo se condicionan a trayectorias futuras de variables macroeconómicas exógenas — como el PIB o la inflación — procedentes de fuentes internacionales como el *World Economic Outlook* del International Monetary Fund. Este enfoque permite generar estimaciones prospectivas de la demanda turística y de la capacidad aérea bajo distintos supuestos económicos, constituyendo una herramienta de especial relevancia para la toma de decisiones en el sector — particularmente para aerolíneas y operadores turísticos — al facilitar la planificación estratégica en horizontes temporales futuros.

**Palabras clave:** demanda turística, predicción de series temporales, Polonia, LSTM, SARIMA, estadística bayesiana, HICP, Eurostat, conectividad aérea, COVID-19.


---

## Abstract

This Bachelor's thesis addresses the modelling and forecasting of international tourism demand in Poland, measured as the monthly number of overnight stays by foreign tourists in tourist accommodation establishments. Over the past two decades, Poland has established itself as one of Europe's fastest-growing economies, with a fivefold increase in airport passenger traffic since its EU accession in 2004 and a price level approximately 30% below the EU average, making it a representative case of the economic and tourism boom in Eastern Europe.

The work integrates harmonised Eurostat data — consumer price indices (HICP), bilateral exchange rates, real GDP, consumer confidence indicators, and airline seat capacity — from nine European source markets, and follows a progressively complex approach: classical statistical models (SARIMA, Holt-Winters), machine learning algorithms (Random Forest, XGBoost), recurrent neural networks (LSTM with exogenous variables), and Bayesian methods (Bayesian Structural Time Series and Bayesian Model Averaging). The comparative evaluation employs standard metrics (RMSE, MAE, MAPE) and the Diebold-Mariano test, complemented by a causal impact analysis of COVID-19 using the CausalImpact framework. Additionally, forecasts are generated under alternative scenarios (baseline, optimistic, pessimistic) regarding the evolution of air connectivity and macroeconomic conditions.

**Keywords:** tourism demand, time series forecasting, Poland, LSTM, SARIMA, Bayesian statistics, HICP, Eurostat, air connectivity, COVID-19.

---

# Capítulo 1. Introducción

El turismo internacional constituye uno de los sectores económicos más relevantes a escala global. Según el Barómetro Mundial del Turismo publicado por Naciones Unidas (UN Tourism, 2025), las llegadas internacionales de turistas alcanzaron los 1.400 millones en 2024, lo que supuso un incremento del 11 % respecto a 2023 y una recuperación prácticamente completa de los niveles previos a la pandemia de COVID-19. En términos monetarios, los ingresos por turismo internacional ascendieron a 1,6 billones de dólares estadounidenses en 2024. El Consejo Mundial de Viajes y Turismo (WTTC, *World Travel & Tourism Council*) estimó que la contribución total del sector al Producto Interior Bruto (PIB, *Gross Domestic Product*, GDP) mundial alcanzó los 10,9 billones de dólares — equivalentes al 10 % de la economía global — generando 357 millones de empleos (WTTC, 2025). En el ámbito europeo, el sector contribuyó con casi 1,8 billones de euros al PIB de la Unión Europea, representando más del 10 % de la economía comunitaria y sustentando más de 24,5 millones de empleos.

En este contexto de recuperación y crecimiento continuado, la capacidad de predecir con precisión la demanda turística adquiere una importancia estratégica fundamental. Los productos turísticos — plazas hoteleras, asientos de avión, paquetes vacacionales — son perecederos: una habitación de hotel no ocupada en una noche determinada representa un ingreso irrecuperablemente perdido. Como señalaron Song y Li (2008) en la revisión más citada del campo, la predicción de la demanda turística ayuda tanto al sector público como al privado a mejorar la asignación de recursos escasos, y predicciones más precisas proporcionan mejores estimaciones del retorno esperado de las inversiones. Esta realidad afecta directamente a la planificación de infraestructuras, la programación de rutas aéreas, la gestión de capacidad hotelera y la formulación de políticas públicas de promoción turística.

El presente Trabajo de Fin de Grado (TFG) se enmarca en el ámbito de la ciencia e ingeniería de datos aplicada al análisis y modelización de fenómenos socioeconómicos. En las dos últimas décadas, Polonia se ha consolidado como una de las economías de mayor crecimiento en Europa, alcanzando niveles de renta, conectividad aérea y movilidad que la sitúan como un caso representativo del auge económico y demográfico de Europa del Este. Este crecimiento sostenido, junto con la expansión progresiva de la capacidad aérea del país y la entrada de nuevos operadores de bajo coste (LCC, *Low-Cost Carrier*), apunta a un cambio estructural en los patrones de movilidad y turismo en Europa. El incremento del PIB, la evolución de la población y el aumento de las plazas aéreas disponibles actúan de forma conjunta como factores clave que impulsan la propensión a viajar, tanto a nivel interno como internacional. En este contexto, el análisis de la interacción entre economía, demografía y transporte aéreo resulta especialmente relevante para comprender cómo pueden evolucionar y redistribuirse los flujos turísticos europeos en los próximos años.

## 1.1 Estructura del documento

El resto del documento se organiza de la siguiente manera. El Capítulo 2 presenta el estado actual de la investigación en modelización de demanda turística, la motivación específica para el estudio del caso polaco y los objetivos del trabajo. El Capítulo 3 describe las principales aportaciones del TFG, las competencias específicas del Grado en Ciencia e Ingeniería de Datos que se cubren y el alineamiento con los Objetivos de Desarrollo Sostenible. El Capítulo 4 constituye el núcleo del desarrollo: la metodología seguida, las fuentes de datos, la ingeniería de características, la descripción de los modelos y el análisis exploratorio. El Capítulo 5 presentará los resultados de los modelos predictivos y su evaluación comparativa. Finalmente, el Capítulo 6 recoge las conclusiones, las líneas de trabajo futuro y una declaración sobre el uso de la inteligencia artificial en la elaboración del trabajo.

---

# Capítulo 2. Estado Actual y Objetivos Iniciales

## 2.1 Motivación y antecedentes

### 2.1.1 El turismo internacional como fenómeno socioeconómico

La modelización econométrica de la demanda turística internacional tiene una tradición académica consolidada. Los trabajos seminales de Crouch (1994, 1995), que revisaron e integraron los resultados de más de 80 estudios empíricos, establecieron el conjunto de determinantes fundamentales que ha guiado la investigación durante las tres últimas décadas. La revisión posterior de Li, Song y Witt (2005), que analizó 84 estudios publicados entre 1990 y 2004, confirmó estos hallazgos. Los meta-análisis de Peng, Song, Crouch y Witt (2015), basados en 195 estudios publicados entre 1961 y 2011, coinciden en que la elasticidad-renta de la demanda turística es superior a la unidad (valores medios entre 1,5 y 2,5), lo que clasifica al turismo internacional como un bien de lujo: cuando la renta de los hogares aumenta un 1 %, la demanda turística crece más de un 1 %. La elasticidad-precio media se sitúa entre −0,6 y −0,8, indicando una demanda relativamente inelástica pero significativa (Crouch, 1994).

La contribución metodológica más influyente en la operacionalización del precio turístico la proporcionaron Song, Li, Witt y Fei (2010) con la **variable de precio turístico relativo** (*relative tourism price*):

$$P_{it} = \frac{CPI_{PL}}{CPI_i} \times \frac{EX_i}{EX_{PL}}$$

donde $CPI_{PL}$ y $CPI_i$ representan los Índices Armonizados de Precios al Consumo (HICP, *Harmonised Index of Consumer Prices*) de Polonia y del país de origen $i$, y $EX_{PL}$ y $EX_i$ los tipos de cambio bilaterales del zloty polaco (PLN) y de la moneda del país de origen frente al euro. Esta variable captura simultáneamente el diferencial de coste de vida y el efecto del tipo de cambio, midiendo la competitividad relativa en precios del destino.

En cuanto a la medición de la demanda, las **pernoctaciones** (*overnight stays*) presentan una ventaja conceptual sobre las llegadas de turistas: equivalen al producto de las llegadas por la duración media de la estancia, capturando así tanto el volumen como la duración de la actividad turística (Álvarez-Díaz et al., 2019; Gössling et al., 2018). En la investigación turística europea, las pernoctaciones son además el indicador estándar porque el Reglamento (UE) n.º 692/2011 sobre estadísticas europeas de turismo obliga a todos los Estados miembros a recopilar y transmitir mensualmente datos armonizados, publicados por Eurostat en el conjunto de datos `tour_occ_nim`.

### 2.1.2 Polonia como caso de estudio

La elección de Polonia responde a su condición de caso representativo del auge de Europa del Este en el contexto europeo. Desde su adhesión a la Unión Europea el 1 de mayo de 2004, el turismo internacional hacia el país ha experimentado una transformación profunda:

- Las llegadas de turistas internacionales crecieron de 15,7 millones (2006) a 21,4 millones (2019), situando al país como el 18.º más visitado del mundo (UN Tourism, 2019).
- En 2025, Eurostat registró 104,5 millones de pernoctaciones, un aumento del 7 %, lo que convirtió a Polonia en el país con el **segundo mayor crecimiento turístico de toda la UE**, solo por detrás de Malta (Eurostat, 2026; Notes from Poland, 2026).
- El PIB per cápita polaco pasó de aproximadamente el 50 % de la media de la UE en 2004 al 80 % en 2023 — una de las convergencias económicas más exitosas de la Unión.
- Los pasajeros en aeropuertos polacos se multiplicaron por cinco: de ~11 millones (2004) a 59,2 millones (2024) (ULC, 2025).
- Las aerolíneas de bajo coste (Wizz Air desde 2004, Ryanair desde 2005) pasaron de concentrar un ~5 % del mercado a más del 59 % en 2023 (Skift, 2023; Huderek-Glapska y Nowak, 2016).

A pesar de este crecimiento, el turismo contribuye solo aproximadamente un 4 % al PIB polaco (WTTC, 2025), cifra significativamente inferior a la media de la UE (~10 %). El gobierno polaco anunció en septiembre de 2025 el objetivo de alcanzar el 9 % para 2030, lo que subraya la necesidad de herramientas de predicción robustas. Adicionalmente, el nivel de precios polaco se sitúa un 34 % por debajo de la media comunitaria según las paridades de poder adquisitivo (PPP, *Purchasing Power Parity*) publicadas por Eurostat (2024), otorgando al país una ventaja competitiva en precios extraordinaria para el turismo receptivo.

### 2.1.3 Panorama metodológico

La predicción de la demanda turística ha experimentado una evolución metodológica acelerada. La revisión de Song, Qiu y Park (2019) sobre 211 artículos (1968–2018) documentó la transición desde los modelos ingenuos hacia la econometría (cointegración, VAR) y, más recientemente, las técnicas de inteligencia artificial. La competición de predicción turística de Athanasopoulos, Hyndman, Song y Wu (2011), con 1.311 series temporales, encontró que los modelos puramente de series temporales (ETS y ARIMA) proporcionaban predicciones más precisas que los modelos con variables explicativas en horizontes cortos, subrayando la importancia de incluir *benchmarks* simples.

En el ámbito del *deep learning*, Salamanis, Xanthopoulou, Kehagias y Tzovaras (2022) demostraron que las variantes de LSTM con variables exógenas (LSTMX) mejoraban las predicciones a largo plazo de la demanda hotelera griega. Chen, Ying, Zhang y Balezentis (2024) propusieron un modelo CNN-BiLSTM con selección de características Boruta que redujo el RMSE en un 59,93 %. La revisión sistemática de Dowlut y Gobin-Rahimbux (2023) confirmó a LSTM como la arquitectura más utilizada (48 % de los 50 estudios revisados).

La estadística bayesiana ofrece una vía complementaria: los *Bayesian Structural Time Series* (BSTS) de Scott y Varian (2014) combinan descomposición estructural con selección automática de variables, mientras que *CausalImpact* (Brodersen et al., 2015) permite estimar el impacto causal de intervenciones (como restricciones pandémicas) mediante contrafactuales bayesianos. El *Bayesian Model Averaging* (BMA), fundamentado en Hoeting, Madigan, Raftery y Volinsky (1999), permite evaluar probabilísticamente qué combinación de predictores es más probable dado los datos.

## 2.2 Objetivos

El **objetivo general** es analizar y predecir la evolución del turismo internacional asociado a Polonia mediante la integración de datos económicos, demográficos y de capacidad aérea, construyendo modelos de predicción basados en series temporales, *machine learning* y redes neuronales, y evaluando su comportamiento bajo distintos escenarios futuros.

Los **objetivos específicos** son:

1. Realizar un **análisis descriptivo y comparativo** de la evolución de las plazas aéreas, el PIB real y nominal, la población y las métricas turísticas de Polonia, identificando su posición relativa frente a los principales mercados emisores de Europa Occidental.

2. Calcular **indicadores clave** como la propensión a viajar, las plazas aéreas per cápita y los ratios entre crecimiento económico y conectividad aérea.

3. Construir un **panel de datos mensual** que integre la variable objetivo (pernoctaciones extranjeras) con variables exógenas de precios (HICP, tipos de cambio), renta (PIB real), sentimiento (confianza del consumidor) y conectividad aérea (asientos disponibles), incorporando la variable de precio turístico relativo de Song et al. (2010).

4. Desarrollar y comparar una **batería progresiva de modelos predictivos**: modelos estadísticos clásicos (Naïve estacional, Holt-Winters, SARIMA), algoritmos de *machine learning* (Random Forest, XGBoost), modelos de *deep learning* (LSTM con y sin variables exógenas; opcionalmente BiLSTM o CNN-LSTM) y modelos bayesianos (BSTS con *CausalImpact* y BMA para selección probabilística de variables).

5. Evaluar formalmente la **significación estadística** de las diferencias entre modelos mediante el test de Diebold-Mariano, y cuantificar el valor marginal que aportan las variables exógenas.

6. Generar **predicciones bajo escenarios alternativos** (tendencial, optimista, pesimista) sobre el crecimiento aéreo y económico y su impacto en la demanda turística.

---

# Capítulo 3. Aportaciones del Trabajo

## 3.1 Principales aportaciones

Este TFG realiza las siguientes aportaciones:

1. **Integración de múltiples fuentes de datos armonizadas.** Se construye un panel de datos mensual que integra, por primera vez en un estudio sobre Polonia, variables de precios (HICP), tipos de cambio, PIB real, confianza del consumidor y conectividad aérea procedentes de nueve mercados emisores europeos, todas extraídas de fuentes Eurostat armonizadas que garantizan la comparabilidad entre países.

2. **Comparación sistemática de paradigmas de predicción.** Se implementa y compara una batería de modelos que abarca cuatro paradigmas metodológicos — estadística clásica, aprendizaje automático, redes neuronales profundas y estadística bayesiana — evaluados con métricas estándar y tests de significación estadística, lo que permite cuantificar formalmente el valor marginal de cada nivel de complejidad.

3. **Análisis de impacto causal del COVID-19.** Mediante el marco *CausalImpact* (Brodersen et al., 2015), se estima el contrafactual bayesiano de cuántas pernoctaciones se habrían producido en ausencia de la pandemia, proporcionando una cuantificación rigurosa del impacto que complementa los enfoques puramente descriptivos.

4. **Análisis prospectivo bajo escenarios.** Se generan predicciones bajo escenarios alternativos de crecimiento económico y conectividad aérea, dotando al análisis de una dimensión prospectiva útil para la planificación de infraestructuras turísticas y la formulación de políticas.

5. **Reproducibilidad completa.** Todo el código, datos procesados y figuras se publican en un repositorio abierto de GitHub, organizado en notebooks secuenciales numerados que permiten la replicación íntegra del análisis.

## 3.2 Competencias específicas

Las competencias específicas del Grado en Ciencia e Ingeniería de Datos cubiertas de forma más directa por este TFG son:

- **CE1 — Capacidad para resolver problemas con iniciativa, toma de decisiones, creatividad, razonamiento crítico.** El diseño del estudio requiere decisiones metodológicas fundamentadas sobre la selección de variables (endogeneidad de la capacidad aérea), la especificación de modelos (elección de lags, tratamiento del COVID-19) y la interpretación de resultados contradictorios entre paradigmas.

- **CE5 — Conocimiento de las materias básicas y tecnologías que capacitan para el aprendizaje y desarrollo de nuevos métodos y tecnologías.** El trabajo integra fundamentos de econometría de series temporales, aprendizaje automático supervisado y estadística bayesiana, requiriendo la asimilación autónoma de técnicas como BSTS y *CausalImpact* no cubiertas directamente en el plan de estudios.

- **CE8 — Capacidad para la modelización estadística de datos, incluyendo técnicas de aprendizaje automático y métodos bayesianos.** Se implementan modelos SARIMA, Random Forest, XGBoost, LSTM, BSTS y BMA, abarcando los principales paradigmas de la ciencia de datos aplicada.

- **CE10 — Capacidad para el análisis, diseño y gestión de sistemas de información.** La construcción del panel de datos mensual a partir de múltiples conjuntos de datos Eurostat con distintas frecuencias, coberturas y formatos requiere un diseño cuidadoso del flujo de datos y la gestión de su integridad.

## 3.3 Alineamiento con los Objetivos de Desarrollo Sostenible

| ODS | Descripción | Grado | Justificación |
|-----|-------------|-------|---------------|
| 8 | Trabajo decente y crecimiento económico | **Alto (3)** | El turismo genera el 10 % del empleo mundial. La predicción de demanda contribuye directamente a la planificación del empleo turístico y al crecimiento económico sostenible. |
| 9 | Industria, innovación e infraestructuras | **Alto (3)** | El análisis de conectividad aérea y su relación con la demanda turística aporta evidencia para la planificación de infraestructuras de transporte. |
| 11 | Ciudades y comunidades sostenibles | **Medio (2)** | La predicción de flujos turísticos permite anticipar presiones sobre la capacidad de acogida de las ciudades destino, contribuyendo a una gestión urbana más sostenible. |
| 12 | Producción y consumo responsables | **Medio (2)** | Una predicción precisa reduce el despilfarro de recursos perecederos (habitaciones vacías, asientos no vendidos), alineándose con patrones de consumo más eficientes. |
| 17 | Alianzas para lograr objetivos | **Bajo (1)** | El uso exclusivo de datos abiertos de Eurostat y la publicación del código en acceso abierto fomentan la cooperación estadística internacional y la ciencia abierta. |

Los restantes ODS (1–7, 10, 13–16) no presentan una relación directa significativa con el contenido del trabajo (grado 0).

---

# Capítulo 4. Desarrollo

## 4.1 Metodología

### 4.1.1 Marco metodológico: CRISP-DM

El trabajo sigue la metodología **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*), un marco estándar para proyectos de ciencia de datos que estructura el trabajo en seis fases iterativas. Su elección se justifica porque permite un proceso flexible y adaptativo, especialmente adecuado para trabajos donde la exploración de datos, el tratamiento de valores faltantes y la experimentación con múltiples modelos son parte esencial del proceso.

Las fases de CRISP-DM se adaptan al presente trabajo de la siguiente manera:

1. **Comprensión del negocio (*Business Understanding*).** Revisión de la literatura académica sobre modelización de demanda turística, definición del problema de predicción, identificación de los determinantes teóricos de la demanda (renta, precios, tipos de cambio, sentimiento, conectividad) y de las fuentes de datos disponibles.

2. **Comprensión de los datos (*Data Understanding*).** Carga, inspección estructural y verificación de todos los conjuntos de datos brutos. Correspondencia con el Notebook 00 del repositorio.

3. **Preparación de los datos (*Data Preparation*).** Limpieza, integración de múltiples fuentes, tratamiento de valores faltantes, interpolación de series trimestrales a mensuales, creación de variables derivadas (precio turístico relativo, indicadores per cápita, dummies estacionales y de COVID-19). Correspondencia con los Notebooks 01–04.

4. **Modelado (*Modeling*).** Implementación de modelos estadísticos (SARIMA, Holt-Winters), algoritmos de aprendizaje automático (Random Forest, XGBoost), redes neuronales recurrentes (LSTM) y modelos bayesianos (BSTS, BMA). Correspondencia con los Notebooks 05–07.

5. **Evaluación (*Evaluation*).** Comparación de modelos con métricas RMSE, MAE y MAPE, validación temporal con los últimos 12 meses como conjunto de test, *TimeSeriesSplit* para validación cruzada en modelos de aprendizaje automático, test de Diebold-Mariano para significación estadística y análisis de impacto causal del COVID-19. Correspondencia con el Notebook 08.

6. **Comunicación (*Deployment*).** Elaboración de la presente memoria, publicación del repositorio de código en GitHub y generación de figuras y tablas reproducibles.

### 4.1.2 Herramientas tecnológicas

Todo el desarrollo se realiza en **Python 3.12**, con las siguientes bibliotecas principales:

- **Manipulación de datos:** pandas, NumPy.
- **Visualización:** Matplotlib, Seaborn.
- **Estadística y series temporales:** statsmodels (SARIMA, tests ADF, Granger), SciPy.
- **Aprendizaje automático:** scikit-learn (Random Forest, métricas), XGBoost.
- **Redes neuronales:** PyTorch (LSTM).
- **Métodos bayesianos:** CausalImpact (análisis contrafactual), implementaciones de BSTS y BMA.
- **Control de versiones:** Git, con repositorio público en GitHub.

El código se organiza en **notebooks de Jupyter** numerados secuencialmente (00 a 08), cada uno correspondiente a una fase del análisis, más un directorio `src/` con módulos reutilizables.

## 4.2 Fases de desarrollo

### 4.2.1 Fase 1 — Comprensión y verificación de los datos (Notebook 00)

La primera fase del desarrollo consistió en la carga e inspección estructural de los 16 conjuntos de datos brutos descargados de Eurostat. El objetivo fue verificar que todos los archivos existían, se cargaban correctamente y contenían las columnas, filtros y coberturas temporales esperadas antes de iniciar cualquier análisis.

**Fuente de datos: Eurostat.** La totalidad de los datos empleados en este trabajo procede de Eurostat, la Oficina Estadística de la Unión Europea. Eurostat no recopila datos directamente: los Institutos Nacionales de Estadística de cada Estado miembro recogen y validan los datos nacionales, que son transmitidos a Eurostat para su consolidación bajo metodologías armonizadas. La elección de Eurostat como fuente única responde a tres razones: la armonización metodológica que garantiza la comparabilidad entre países, la cobertura temporal consistente para el período 2011–2025 y la frecuencia mensual (o trimestral para el PIB) requerida por los modelos.

Los conjuntos de datos se organizan en cuatro bloques temáticos:

**Variable dependiente.** El número mensual de pernoctaciones de turistas extranjeros en Polonia se extrae del conjunto de datos `tour_occ_nim`, publicado con arreglo al Reglamento (UE) n.º 692/2011. Los filtros aplicados son: `geo = 'Poland'`, `c_resid = 'Foreign country'`, `unit = 'Number'` y `nace_r2` correspondiente al total de tipos de alojamiento. Una limitación importante es que la columna `c_resid` solo distingue entre residentes nacionales, extranjeros y total — no proporciona un desglose por país de origen específico. La dimensión de mercados emisores entra en el modelo a través de las variables exógenas medidas en cada país de origen.

**Bloque económico / de precios.** Incluye el HICP mensual (`prc_hicp_midx`, base 2015 = 100) para todos los países, los tipos de cambio bilaterales frente al euro (`ert_bil_eur_m`) para las divisas no pertenecientes a la Eurozona (PLN, GBP, SEK, CZK, HUF), y el PIB real trimestral (`namq_10_gdp`) en volúmenes encadenados con año de referencia 2010. El uso del HICP — en lugar de los índices de precios al consumo nacionales (IPC) — es una decisión metodológica fundamental: a diferencia de los IPC nacionales, el HICP se calcula siguiendo una metodología uniforme establecida por el Reglamento (UE) 2016/792, garantizando la comparabilidad directa entre países.

**Bloque de sentimiento.** El indicador de confianza del consumidor (`ei_bsco_m`) proporciona un balance mensual desestacionalizado basado en encuestas a ~32.000 hogares en la UE.

**Bloque de conectividad aérea.** Los asientos de aerolíneas disponibles (`avia_tf_aca`) y los pasajeros aéreos por país par (`avia_paoc`) — estos últimos utilizados exclusivamente para validación descriptiva, no como predictores, debido a su endogeneidad.

La inspección confirmó que los 16 archivos se cargaban correctamente, con cero valores ausentes en la variable objetivo (179 observaciones mensuales, enero 2011 – noviembre 2025), cobertura completa para 12 de los 13 países requeridos (la serie del Reino Unido presenta discontinuidades post-Brexit) y los filtros esperados en todas las columnas categóricas. Los resultados detallados se documentan en el Notebook 00 del repositorio.

### 4.2.2 Fase 2 — Análisis exploratorio descriptivo (Notebook 01)

La segunda fase consistió en un análisis exploratorio de datos (EDA, *Exploratory Data Analysis*) exhaustivo de cada bloque de variables, generando las tablas y figuras para el análisis descriptivo.

**Variable objetivo: pernoctaciones de turistas extranjeros.** La serie presenta las siguientes características:

- **Tendencia creciente sostenida** desde 2011 hasta 2019, con un máximo pre-pandemia de 2.260.446 pernoctaciones en julio de 2019.
- **Colapso del COVID-19:** el mínimo de abril de 2020 (83.695 pernoctaciones) representa una caída del 96,3 % respecto al pico — entre las más severas del turismo europeo.
- **Recuperación lenta y asimétrica:** la suma móvil de 12 meses muestra que la demanda anualizada no regresó a niveles pre-pandemia hasta mediados de 2023, dos años completos después de la relajación de las restricciones.
- **Estacionalidad pronunciada pero moderada:** ratio pico-a-valle de 2,4 veces (agosto: media de 1,87 millones; enero: media de 783.000). El ratio relativamente contenido refleja el perfil mixto de Polonia como destino de turismo cultural urbano, de negocios y de ocio. Un rasgo notable es la desaceleración gradual tras el verano: septiembre y octubre mantienen niveles elevados, probablemente impulsados por el turismo cultural de otoño, el inicio del curso académico (~90.000 estudiantes internacionales) y la concentración de viajes de negocios.
- **Distribución próxima a la normalidad:** asimetría de 0,011, curtosis de −0,036, test de Shapiro-Wilk no significativo (W = 0,992, p = 0,43).
- **Proporción de turistas extranjeros:** media del 18,8 % del total de pernoctaciones (rango: 7,1 %–25,7 %), con una caída drástica durante la pandemia que sugiere que el turismo doméstico se recuperó más rápidamente que el internacional.

**Variables económicas.** El HICP polaco creció más rápido que el de todos los países de origen desde 2021, alcanzando un pico de inflación interanual del 17,2 % en febrero de 2023 — la más alta de la muestra. En diciembre de 2025 se había moderado al 2,5 %. El tipo de cambio PLN/EUR fluctuó entre 3,26 y 4,86, con la debilitación del zloty durante 2022–2023 actuando como posible amortiguador de la pérdida de competitividad en precios. El nivel de precios polaco (índice PPP) se sitúa en 70,2 (EU27 = 100), confirmando que los precios son aproximadamente un 30 % inferiores a la media comunitaria. El PIB real de los principales países de origen muestra una recuperación en forma de V tras la pandemia.

**Conectividad aérea.** La capacidad de asientos ha superado los niveles pre-COVID: la última observación (octubre 2025: 6.999.227 asientos) supera el pico anterior (agosto 2019: 5.850.139) en un 19,6 %. Los datos de pasajeros aéreos por país par revelan una distribución de mercados emisores equilibrada: España (19,8 %), Alemania (19,5 %), Reino Unido (18,8 %), Francia (14,4 %), Italia (13,5 %). La distribución aeroportuaria confirma a Varsovia Chopin como el aeropuerto principal (21,3 millones de pasajeros en 2024), con tráfico significativo en aeropuertos regionales dominados por LCC (Cracovia, Gdańsk, Katowice, Wrocław).

**Confianza del consumidor.** El indicador muestra patrones cíclicos altamente sincronizados entre países de origen, con hundimientos simultáneos durante la pandemia. La recuperación de la confianza precedió en varios meses a la recuperación del turismo, un patrón consistente con su papel esperado como indicador adelantado. El Reino Unido está ausente de este conjunto de datos Eurostat, lo que requerirá una fuente alternativa.

### 4.2.3 Fases pendientes

Las siguientes fases del desarrollo — análisis multivariante y correlaciones cruzadas (Notebook 02), tests estadísticos y selección de variables (Notebook 03), ingeniería de características y construcción del panel maestro (Notebook 04), modelos de referencia (Notebook 05), modelos de aprendizaje automático (Notebook 06), modelos de *deep learning* (Notebook 07) y comparación final con escenarios (Notebook 08) — se encuentran planificadas y se documentarán en las secciones correspondientes a medida que se completen.

---

# Capítulo 5. Resultados

*Este capítulo se completará con los resultados de los modelos predictivos una vez finalizadas las fases de modelado (Notebooks 05–08). Incluirá la comparación de métricas entre modelos, los tests de Diebold-Mariano, el análisis de importancia de variables, el impacto causal del COVID-19 estimado por CausalImpact y las predicciones bajo escenarios alternativos.*

---

# Capítulo 6. Conclusiones y Trabajo Futuro

## 6.1 Conclusiones

*Se completará al finalizar el trabajo.*

## 6.2 Trabajo futuro

*Se completará al finalizar el trabajo. Entre las líneas anticipadas: extensión a otros destinos de Europa del Este, incorporación de datos de búsquedas web (Google Trends) como predictores en tiempo real, y desarrollo de un dashboard interactivo en Streamlit.*

## 6.3 Uso de la IA

En la elaboración de este TFG se ha utilizado el modelo de lenguaje Claude (Anthropic) como herramienta de asistencia en las siguientes tareas:

- **Asistencia en la programación:** generación y depuración de código Python para los notebooks de análisis, incluyendo funciones de carga de datos, visualización y preprocesamiento.
- **Redacción:** apoyo en la estructuración y redacción de la presente memoria, partiendo siempre de las ideas, decisiones metodológicas y hallazgos del autor. Toda afirmación factual ha sido verificada frente a las fuentes originales.
- **Búsqueda bibliográfica:** identificación de referencias académicas relevantes, cuyos contenidos han sido verificados y citados directamente desde las fuentes primarias.

En ningún caso la IA ha tomado decisiones metodológicas autónomas ni ha sustituido el juicio crítico del autor. Todas las decisiones de diseño (selección de variables, especificación de modelos, interpretación de resultados) son responsabilidad exclusiva del autor.

---

# Bibliografía

[1] Álvarez-Díaz, M., González-Gómez, M. y Otero-Giráldez, M. S. (2019). Forecasting international tourism demand using a non-linear autoregressive neural network and genetic programming. *Forecasting*, 1(1), 90–106. https://doi.org/10.3390/forecast1010007

[2] Athanasopoulos, G., Hyndman, R. J., Song, H. y Wu, D. C. (2011). The tourism forecasting competition. *International Journal of Forecasting*, 27(3), 822–844. https://doi.org/10.1016/j.ijforecast.2010.04.009

[3] Brodersen, K. H., Gallusser, F., Koehler, J., Remy, N. y Scott, S. L. (2015). Inferring causal impact using Bayesian structural time-series models. *The Annals of Applied Statistics*, 9(1), 247–274. https://doi.org/10.1214/14-AOAS788

[4] Chen, J., Ying, Z., Zhang, C. y Balezentis, T. (2024). Forecasting tourism demand with search engine data: A hybrid CNN-BiLSTM model based on Boruta feature selection. *Information Processing & Management*, 61(3), 103699. https://doi.org/10.1016/j.ipm.2024.103699

[5] Crouch, G. I. (1994). The study of international tourism demand: A survey of practice. *Journal of Travel Research*, 32(4), 41–54. https://doi.org/10.1177/004728759403200408

[6] Crouch, G. I. (1995). A meta-analysis of tourism demand. *Annals of Tourism Research*, 22(1), 103–118.

[7] Dowlut, N. y Gobin-Rahimbux, B. (2023). Forecasting resort hotel tourism demand using deep learning techniques – A systematic literature review. *Heliyon*, 9(7), e18385.

[8] Eurostat (2024). Household consumption: price levels in 2023. DDN-20240620-2. https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20240620-2

[9] Eurostat (2026). EU tourism nights at record 3.08 billion in 2025. DDN-20260116-1. https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20260116-1

[10] Gössling, S., Scott, D. y Hall, C. M. (2018). Global trends in length of stay. *Journal of Sustainable Tourism*, 26(12), 2087–2101. https://doi.org/10.1080/09669582.2018.1529771

[11] Hoeting, J. A., Madigan, D., Raftery, A. E. y Volinsky, C. T. (1999). Bayesian model averaging: A tutorial. *Statistical Science*, 14(4), 382–417.

[12] Huderek-Glapska, S. y Nowak, H. (2016). Development of regional airports in Poland. *Mediterranean Journal of Social Sciences*, MCSER Publishing.

[13] Li, G., Song, H. y Witt, S. F. (2005). Recent developments in econometric modeling and forecasting. *Journal of Travel Research*, 44(1), 82–99. https://doi.org/10.1177/0047287505276594

[14] Notes from Poland (2026). Poland saw EU's second-fastest growth in tourism in 2025. https://notesfrompoland.com/2026/01/19/

[15] Peng, B., Song, H., Crouch, G. I. y Witt, S. F. (2015). A meta-analysis of international tourism demand elasticities. *Journal of Travel Research*, 54(5), 611–633. https://doi.org/10.1177/0047287514528283

[16] Reglamento (UE) n.º 692/2011, relativo a las estadísticas europeas sobre el turismo. *DOUE*, L 192, 22.7.2011. https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32011R0692

[17] Reglamento (UE) 2016/792, relativo a los índices armonizados de precios de consumo. https://eur-lex.europa.eu/eli/reg/2016/792/oj/eng

[18] Salamanis, A., Xanthopoulou, G., Kehagias, D. y Tzovaras, D. (2022). LSTM-based deep learning models for long-term tourism demand forecasting. *Electronics*, 11(22), 3681. https://doi.org/10.3390/electronics11223681

[19] Scott, S. L. y Varian, H. R. (2014). Predicting the present with Bayesian structural time series. *Int. J. Math. Modelling Num. Optimisation*, 5(1/2), 4–23. https://doi.org/10.1504/IJMMNO.2014.059942

[20] Skift (2023). Poland now at the center of Europe's low-cost carrier competition. https://skift.com/2023/10/18/

[21] Song, H. y Li, G. (2008). Tourism demand modelling and forecasting — A review. *Tourism Management*, 29(2), 203–220. https://doi.org/10.1016/j.tourman.2007.07.016

[22] Song, H., Li, G., Witt, S. F. y Fei, B. (2010). How should demand be measured? *Tourism Economics*, 16(1), 63–81. https://doi.org/10.5367/000000010790872213

[23] Song, H., Qiu, R. T. R. y Park, J. (2019). A review of tourism demand forecasting. *Annals of Tourism Research*, 75, 338–362. https://doi.org/10.1016/j.annals.2018.12.001

[24] Song, H., Witt, S. F. y Li, G. (2009). *The Advanced Econometrics of Tourism Demand*. Routledge. https://doi.org/10.4324/9780203891469

[25] ULC (2025). Polish airports passenger statistics Q4 2024. https://ulc.gov.pl/

[26] UN Tourism (2025). *World Tourism Barometer*, Vol. 23, No. 1. https://doi.org/10.18111/wtobarometereng.2025.23.1.1

[27] WTTC (2025). *Travel & Tourism Economic Impact 2025*. https://wttc.org/research/economic-impact

---

# Glosario

**BSTS** (*Bayesian Structural Time Series*): Modelo bayesiano de series temporales estructurales que descompone una serie en tendencia, estacionalidad y regresión con selección automática de variables mediante priors de tipo *spike-and-slab*.

**BMA** (*Bayesian Model Averaging*): Técnica que promedia las predicciones de múltiples modelos ponderándolos por su probabilidad posterior, produciendo probabilidades de inclusión posterior (PIP) para cada variable candidata.

**CRISP-DM** (*Cross-Industry Standard Process for Data Mining*): Metodología estándar para proyectos de ciencia de datos que estructura el trabajo en seis fases: comprensión del negocio, comprensión de los datos, preparación, modelado, evaluación y despliegue.

**GDP** (*Gross Domestic Product*): Producto Interior Bruto (PIB). Medida estándar de la producción económica de un país.

**HICP** (*Harmonised Index of Consumer Prices*): Índice Armonizado de Precios al Consumo. Indicador de inflación calculado con metodología uniforme en toda la UE, que permite la comparación directa entre países.

**LCC** (*Low-Cost Carrier*): Aerolínea de bajo coste. Compañía aérea que opera con un modelo de negocio de minimización de costes (p. ej., Ryanair, Wizz Air).

**LSTM** (*Long Short-Term Memory*): Tipo de red neuronal recurrente diseñada para capturar dependencias temporales a largo plazo en datos secuenciales.

**MAPE** (*Mean Absolute Percentage Error*): Error porcentual absoluto medio. Métrica de evaluación que expresa el error de predicción como porcentaje del valor real.

**PLN**: Zloty polaco. Moneda oficial de Polonia.

**PPP** (*Purchasing Power Parity*): Paridad de Poder Adquisitivo. Métrica que compara los niveles de precios entre países midiendo cuánto cuesta una cesta de bienes en cada uno.

**RMSE** (*Root Mean Square Error*): Raíz del error cuadrático medio. Métrica de evaluación que penaliza proporcionalmente más los errores grandes.

**SARIMA** (*Seasonal Autoregressive Integrated Moving Average*): Modelo estadístico de series temporales que incorpora componentes autorregresivos, de media móvil, diferenciación y estacionalidad.
