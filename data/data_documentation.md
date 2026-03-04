# Data Dictionary and Source Documentation

## Tourism Demand Forecasting for Poland: A Comparative Analysis Using Econometric, Machine Learning and Deep Learning Models

**Author:** Diego Marrero Ferrera
**Institution:** University of Las Palmas de Gran Canaria, Canary Islands, Spain
**Date of last update:** March 2026
**Repository:** [github.com/DieGodMF4/Macro-Aviation-Tourism-Modeling](https://github.com/DieGodMF4/Macro-Aviation-Tourism-Modeling)

---

## 1. Overview

This document provides a comprehensive description of all data sources used in this thesis. The raw data is organised into four thematic blocks — economic, demographic, transport (aviation), and tourism — reflecting the theoretical framework of tourism demand modelling (Song et al., 2010; between other articles). All datasets are stored under `data/raw/` and remain unmodified; any transformations are applied exclusively in the `data/processed/` pipeline.

The study period spans from **2003 to 2024**, coinciding with **Poland's accession to the European Union** (May 2004) and the subsequent liberalisation of its air transport market. The destination under study is **Poland (PL)**, while the origin markets comprise western european countries such as: Germany (DE), United Kingdom (UK), France (FR), Netherlands (NL), Italy (IT), Spain (ES), Sweden (SE), Austria (AT), and Czechia (CZ). Substitute destinations for competitive price analysis include Czechia, Hungary (HU), Croatia (HR), and Greece (EL).

---

## 2. Directory Structure

```
data/
|── raw/
|   |── economic/
|   |   |── namq_10_gdp__market_prices.csv
|   |   |── namq_10_gdp__real-gdp-CLV-2010.csv
|   |   |── owid-gdp-world-regions-stacked-area.csv
|   |   |── prc_ppp_ind__price-level-indices.csv
|   |   |── prc_hicp_aind__specific-inflation.csv
|   |   |── prc_hicp_midx__relevant-countries-2003-.csv
|   |   └── ert_bil_eur_m__exchange-rates-eur-pln-usd-2003-.csv
|   |── demographic/
|   |   |── demo_pjan__population-eur-990-25.csv
|   |   |── earn_nt_net__annual-net-earnings.csv
|   |   └── ei_bsco_m__consumer-conf-indicator.csv
|   |── transport/
|   |   |── avia_tf_aca__seats-flights-pass-PL-2010-.csv
|   |   |── avia_paoc__passengers-countries.csv
|   |   └── avia_tf_apal_passengers_airports_PL-2003-.csv
|   └── tourism/
|       |── tour_occ_nights_accommodation_PL_2003-.csv
|       |── tour_cap_nat__tourism-infraestructure.csv
|       |── tour_lfsq6r2__employment-tourism-industries.csv
|       |── UN_Tourism_inbound_arrivals_by_region_12_2025.xlsx
|       └── UN_Tourism_inbound_expenditure_12_2025.xlsx
|── processed/
|   └── master_panel_monthly.csv
|── scenarios/
└── README.md
```

---

## 3. Economic Block

### 3.1 Gross Domestic Product at Market Prices (Nominal)

| Attribute | Value |
|---|---|
| **File** | `economic/namq_10_gdp__market_prices.csv` |
| **Source** | Eurostat, dataset `namq_10_gdp` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/namq_10_gdp/default/table |
| **Frequency** | Quarterly |
| **Period** | 1995-Q1 to 2025-Q2 |
| **Geography** | Poland only |
| **Unit** | Current prices, million EUR and million national currency (PLN) |
| **Adjustment** | Seasonally and calendar adjusted |
| **Dimensions** | 246 observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Nominal GDP in the selected unit |
| **Missing data** | `OBS_VALUE`: 0%; `OBS_FLAG`: 100% (no flags) |
| **Download date** | February 2026 |

**Role in the thesis:** Provides nominal GDP for Poland, used to compute tourism intensity ratios (tourist arrivals / GDP) and as a contextual macroeconomic indicator. Since the unit is nominal (current prices), it should not be used directly in log-linear demand models without deflating.

**Limitations:** Poland-only. For origin-country GDP, the real GDP dataset (_Section 3.2_) is preferred, as it covers multiple countries and is expressed in chain-linked constant-price volumes, consistent with the income variable in the demand model of Song et al. (2010).

---

### 3.2 Real GDP — Chain Linked Volumes (2010)

| Attribute | Value |
|---|---|
| **File** | `economic/namq_10_gdp__real-gdp-CLV-2010.csv` |
| **Source** | Eurostat, dataset `namq_10_gdp` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/namq_10_gdp/default/table |
| **Frequency** | Quarterly |
| **Period** | 1995-Q1 to 2025-Q3 |
| **Geography** | Austria, Czechia, Germany, Spain, Hungary, Poland, Sweden, Croatia, Italy, United Kingdom |
| **Unit** | Chain linked volumes (2010), million EUR |
| **Adjustment** | Seasonally and calendar adjusted |
| **Dimensions** | 1,214 observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Real GDP at constant 2010 prices |
| **Missing data** | `OBS_VALUE`: 0%; `OBS_FLAG`: 96.4% missing (flags present for ~3.6%) |
| **Download date** | February 2026 |

**Role in the thesis:** This is the **primary income variable** (Y_it) in the tourism demand function. Chain-linked volumes at constant prices remove the inflation effect, enabling cross-country comparisons of real purchasing power. Used directly in the log-linear specification:

$$\ln(TD_{it}) = \beta_1 + \beta_2 \ln(Y_{it}) + \beta_3 \ln(P_{it}) + \beta_4 \ln(P^s_t) + \varepsilon_{it}$$

**Processing notes:** Quarterly data will be interpolated to monthly frequency using cubic spline interpolation to match the monthly frequency of the dependent variable (overnight stays). The countries covered align with the defined origin markets. UK data extends to 2020 only (post-Brexit reporting changes); subsequent UK GDP will be sourced from the IMF WEO (Section 3.7).

---

### 3.3 Purchasing Power Parities — Price Level Indices

| Attribute | Value |
|---|---|
| **File** | `economic/prc_ppp_ind__price-level-indices.csv` |
| **Source** | Eurostat, dataset `prc_ppp_ind` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/prc_ppp_ind/default/table |
| **Frequency** | Annual |
| **Period** | 1995–2024 |
| **Geography** | 35+ European countries (all relevant origin markets included) |
| **Unit** | Price level indices (EU27_2020 = 100) |
| **Category** | Actual individual consumption |
| **Dimensions** | 1,056 observations × 10 columns |
| **Key variable** | `OBS_VALUE`: Price level index relative to EU27 average |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | February 2026 |

**Role in the thesis:** Complementary measure of relative price competitiveness. A PLI of 60 for Poland vs. 110 for Germany indicates that goods and services in Poland cost roughly 55% of German prices. Useful for the descriptive analysis (Chapter 4) and as a cross-check on the CPI-based relative price variable. Not used directly in the monthly models due to annual frequency.

---

### 3.4 Harmonised Index of Consumer Prices — Annual (HICP)

| Attribute | Value |
|---|---|
| **File** | `economic/prc_hicp_aind__specific-inflation.csv` |
| **Source** | Eurostat, dataset `prc_hicp_aind` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind/default/table |
| **Frequency** | Annual |
| **Period** | 2003–2025 |
| **Geography** | Austria, Czechia, Germany, Spain, France, Greece, Croatia, Hungary, Italy, Netherlands, Poland, Sweden, EU aggregate, United Kingdom |
| **Unit** | Annual average index (2015 = 100) |
| **COICOP categories** | All-items HICP; Restaurants and hotels; Accommodation services; Hotels, motels, inns and similar; Services related to housing |
| **Dimensions** | 1,476 observations × 10 columns |
| **Key variable** | `OBS_VALUE`: HICP index value |
| **Missing data** | `OBS_VALUE`: 0.07%; `OBS_FLAG`: 95.9% missing (flags present for ~4%) |
| **Download date** | February 2026 |

**Role in the thesis:** Used exclusively for **descriptive and contextual analysis** (Chapter 4). The sector-specific HICP categories (Restaurants & Hotels, Accommodation Services) allow narrative comparison of tourism-specific inflation in Poland versus the EU average and origin markets. For instance, Poland's accommodation services HICP rose from 100 in 2015 to 168.6 in 2025, compared to 151.5 for the EU — indicating faster tourism-sector inflation in Poland.

**Important note:** This dataset is NOT used in the forecasting models. The monthly HICP (Section 3.5) serves as the input for constructing the relative price variable.

---

### 3.5 Harmonised Index of Consumer Prices — Monthly (HICP)

| Attribute | Value |
|---|---|
| **File** | `economic/prc_hicp_midx__relevant-countries-2003-.csv` |
| **Source** | Eurostat, dataset `prc_hicp_midx` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_midx/default/table |
| **Frequency** | Monthly |
| **Period** | 2003-01 to 2025-12 |
| **Geography** | Austria, Czechia, Germany, Spain, France, Greece, Croatia, Hungary, Italy, Netherlands, Poland, Sweden, United Kingdom, EU aggregate |
| **Unit** | Index, 2015 = 100 |
| **COICOP category** | All-items HICP |
| **Dimensions** | 2,000+ observations × 10 columns |
| **Key variable** | `OBS_VALUE`: Monthly HICP index |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | February 2026 |

**Role in the thesis:** This is the **primary CPI variable** used to construct the relative tourism price (P_it) following the methodology of Song et al. (2010):

$$P_{it} = \frac{CPI_{PL,t} \;/\; EX_{PLN/EUR,t}}{CPI_{i,t} \;/\; EX_{i/EUR,t}}$$

where CPI refers to the **All-items HICP**, EX is the exchange rate, PL is Poland (destination), and i is the origin country.

**Country coverage note:** The dataset includes all required origin markets (DE, FR, ES, AT, CZ, EL, HR, IT, NL, SE, PL, UK, HU) as well as the EU aggregate, enabling full computation of the relative price variable for all origin-destination pairs. Croatia (HR) has shorter coverage (from 2023 onwards), which may limit the substitute price calculation for earlier periods.

---

### 3.6 Exchange Rates — EUR Bilateral (Monthly)

| Attribute | Value |
|---|---|
| **File** | `economic/ert_bil_eur_m__exchange-rates-eur-pln-usd-2003-.csv` |
| **Source** | Eurostat, dataset `ert_bil_eur_m` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/ert_bil_eur_m/default/table |
| **Frequency** | Monthly |
| **Period** | 2003-01 to 2026-02 |
| **Currencies** | Polish zloty (PLN), US dollar (USD), British pound (GBP), Swedish krona (SEK), Czech koruna (CZK), and Hungarian forint (HUF) against EUR |
| **Statistic** | Average |
| **Unit** | National currency per 1 EUR |
| **Dimensions** | 556 observations × 10 columns |
| **Key variable** | `OBS_VALUE`: Exchange rate (units of national currency per EUR) |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | March 2026 |

**Role in the thesis:** Essential component of the relative price variable (P_it). The exchange rates capture the price competitiveness effect: a PLN depreciation against a given currency makes Poland cheaper for tourists from that origin country. For Eurozone origin countries (DE, FR, NL, IT, ES, AT, EL), the exchange rate component cancels out in the relative price formula (both numerator and denominator are denominated in EUR), so only non-Eurozone currencies are operationally relevant.

**Currency coverage:** The dataset includes PLN/EUR, USD/EUR, GBP/EUR, SEK/EUR, CZK/EUR, and HUF/EUR, covering all non-Eurozone origin countries and substitute destinations. For Eurozone origin countries (DE, FR, NL, IT, ES, AT, EL), the exchange rate component cancels out in the relative price formula (both numerator and denominator are in EUR).

---

### 3.7 IMF World Economic Outlook — April 2025

| Attribute | Value |
|---|---|
| **File** | `economic/WEO_Data.xls` (tab-separated values) |
| **Source** | International Monetary Fund, World Economic Outlook Database, April 2025 |
| **URL** | https://www.imf.org/en/Publications/WEO/weo-database/2025/April |
| **Frequency** | Annual |
| **Period** | 1980–2027 (with projections for 2025–2027) |
| **Geography** | Poland |
| **Format** | Tab-separated XLS with wide format (years as columns) |
| **Variables included** | GDP per capita (constant prices, national currency); GDP per capita (current USD); Total investment (% GDP); CPI inflation (% change); Import/export volume growth; Unemployment rate; Population; Government expenditure (% GDP); Fiscal balance (% GDP); Government debt (% GDP); Current account balance (% GDP) |
| **Key projections** | GDP per capita 2025: 77,346 PLN; 2026: 79,901 PLN; 2027: 82,496 PLN |
| **Download date** | February 2026 |

**Role in the thesis:** Dual purpose. First, it provides **macroeconomic context** for the descriptive chapter (investment rates, fiscal indicators, trade openness). Second, and critically, it supplies **forward-looking projections** (2025–2027) that form the basis for the scenario analysis (Chapter 7). The four scenarios (boom, moderate growth, stagnation, recession) will be calibrated by applying multipliers to the IMF baseline projections.

**Processing notes:** The file uses a wide format with years as columns, which must be melted to long format. Values contain thousands separators (commas) that need stripping before numeric conversion. The `n/a` string replaces missing data.

---

### 3.8 OWID GDP — World Regions

| Attribute | Value |
|---|---|
| **File** | `economic/owid-gdp-world-regions-stacked-area.csv` |
| **Source** | Our World in Data, based on Maddison Project Database |
| **URL** | https://ourworldindata.org/ |
| **Frequency** | Annual |
| **Period** | Year 1 to 2022 |
| **Geography** | World regions and selected countries |
| **Dimensions** | 15,000+ observations × 5 columns |
| **Key variable** | `Gross domestic product (GDP)`: GDP in international dollars |
| **Download date** | February 2026 |

**Role in the thesis:** Used solely for **background contextualisation** in the introduction (Chapter 1), providing a long-run perspective on global economic growth and the historical position of Eastern Europe. Not included in any analytical model.

---

## 4. Demographic Block

### 4.1 Population — Annual

| Attribute | Value |
|---|---|
| **File** | `demographic/demo_pjan__population-eur-990-25.csv` |
| **Source** | Eurostat, dataset `demo_pjan` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/demo_pjan/default/table |
| **Frequency** | Annual (1 January reference date) |
| **Period** | 1990–2025 |
| **Geography** | 45+ European countries (all relevant origin markets and destinations) |
| **Unit** | Number of persons |
| **Filter** | Age: Total; Sex: Total |
| **Dimensions** | 1,629 observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Total population |
| **Missing data** | `OBS_VALUE`: 0%; `OBS_FLAG`: 95.3% missing |
| **Download date** | February 2026 |

**Role in the thesis:** Used to construct per-capita variables (tourist arrivals per capita, GDP per capita) for cross-country normalisation. Following Song et al. (2010), the per-capita specification is tested alongside the aggregate specification.

**Processing notes:** Annual data will be interpolated to monthly frequency (linear interpolation is acceptable for population, as changes are gradual). The series starts in 1990, providing ample pre-sample context.

---

### 4.2 Annual Net Earnings

| Attribute | Value |
|---|---|
| **File** | `demographic/earn_nt_net__annual-net-earnings.csv` |
| **Source** | Eurostat, dataset `earn_nt_net` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/earn_nt_net/default/table |
| **Frequency** | Annual |
| **Period** | 2000–2024 |
| **Geography** | 25+ European countries (AT, DE, BE, ES, EE, DK, EL, CZ, CH, FI, etc.) |
| **Unit** | EUR |
| **Structure** | Net earnings |
| **Case** | Multiple household configurations (two-earner couples, single earners, etc.) |
| **Dimensions** | 3,300+ observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Annual net earnings in EUR |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | February 2026 |

**Role in the thesis:** Provides a proxy for **disposable income** in origin countries, which is a more direct measure of tourism spending capacity than GDP. Used in the descriptive analysis and potentially as an alternative income variable in robustness checks.

**Limitations:** Annual frequency limits direct use in monthly models. Multiple household structure categories must be carefully filtered to select a consistent specification (recommended: single earner at 100% of average earnings, no children).

---

### 4.3 Consumer Confidence Indicator — Monthly

| Attribute | Value |
|---|---|
| **File** | `demographic/ei_bsco_m__consumer-conf-indicator.csv` |
| **Source** | Eurostat, dataset `ei_bsco_m` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/ei_bsco_m/default/table |
| **Frequency** | Monthly |
| **Period** | 2005-01 to 2026-02 |
| **Geography** | Austria, Belgium, Bulgaria, Czechia, Germany, Denmark, Estonia, Greece (+ others) |
| **Unit** | Balance (percentage points) |
| **Adjustment** | Seasonally adjusted, not calendar adjusted |
| **Dimensions** | 5,000+ observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Consumer confidence indicator (balance) |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | February 2026 |

**Role in the thesis:** A **leading indicator** of tourism demand. Consumer confidence captures household expectations about the economic future, which precedes actual spending decisions. A negative balance (e.g., −20) indicates pessimism; values above zero indicate optimism. The series from 2005 provides coverage for most of the study period. This variable is particularly valuable for the ML/DL models (Phase 3–4 of the methodology), where it can serve as a feature alongside GDP and prices.

**Note on interpretation:** The indicator range in the sample spans from −81.3 to +12.6 (balance), with a mean of −14.2. This negative central tendency is normal for European surveys.

---

## 5. Transport (Aviation) Block

### 5.1 Air Transport — Seats, Flights, and Passengers by Airport (PRIMARY)

| Attribute | Value |
|---|---|
| **File** | `transport/avia_tf_aca__seats-flights-pass-PL-2010-.csv` |
| **Source** | Eurostat, dataset `avia_tf_aca` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/avia_tf_aca/default/table |
| **Frequency** | Monthly |
| **Period** | 2010-01 to 2025-10 |
| **Geography** | All Polish airports (Bydgoszcz, Gdańsk, Katowice, **Kraków**, Łódź, Lublin, Poznań, Rzeszów, Szczecin, **Warsaw Chopin**, Warsaw Modlin, Wrocław) |
| **Transport measures** | `ST_PAS` (Passenger seats available), `PAS_BRD` (Passengers on board), `CAF_PAS` (Commercial passenger air flights) |
| **Units** | Seats (`SEAT`), Passengers (`PAS`), Flights (`FLIGHT`) |
| **Dimensions** | 2,000+ observations × 12 columns |
| **Key variable** | `OBS_VALUE`: Count of seats / passengers / flights |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | February 2026 |

**Role in the thesis:** This is the **primary air connectivity variable**. It contains three distinct measures in a single file, distinguished by the `tra_meas` and `unit` columns:

1. **Passenger seats available (ST_PAS):** The number of seats offered on scheduled and charter flights departing from Polish airports. This is the **core connectivity variable** (SEATS_it) in the extended demand model:

$$\ln(TD_{it}) = \beta_1 + \beta_2 \ln(Y_{it}) + \beta_3 \ln(P_{it}) + \beta_4 \ln(P^s_t) + \beta_5 \ln(SEATS_t) + \varepsilon_{it}$$

2. **Passengers on board (PAS_BRD):** Actual passengers transported. Combined with seats available, this enables the computation of the **load factor** (PAS_BRD / ST_PAS), an indicator of capacity utilisation.

3. **Commercial passenger air flights (CAF_PAS):** The number of flights operated. This provides a complementary connectivity measure (frequency of service).

**Processing notes:** Data is at the airport level. For the aggregate national model, all Polish airports should be summed by month. The data starts only in 2010, which reduces the pre-2010 period; this limitation must be acknowledged, and models using seats as an explanatory variable will have a shorter estimation window (2010–2024 ≈ 180 monthly observations).

**Limitation:** The dataset does not distinguish by partner country (i.e., we cannot observe seats between Poland and Germany specifically). For bilateral analysis, the `avia_paoc` dataset (Section 5.2) provides the country-pair dimension.

---

### 5.2 Air Passengers by Partner Country (BILATERAL)

| Attribute | Value |
|---|---|
| **File** | `transport/avia_paoc__passengers-countries.csv` |
| **Source** | Eurostat, dataset `avia_paoc` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/avia_paoc/default/table |
| **Frequency** | Monthly |
| **Period** | 2003-01 to 2025-12 |
| **Geography** | Bilateral pairs: Poland ↔ Germany, Spain, Austria, Greece, France, Czechia, Croatia, Hungary (as `geo` column) |
| **Transport measure** | Passengers on board (departures) |
| **Coverage** | Total transport |
| **Schedule** | Total (scheduled + non-scheduled) |
| **Dimensions** | 2,000+ observations × 12 columns |
| **Key variable** | `OBS_VALUE`: Number of passengers |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | February 2026 |

**Role in the thesis:** Provides the **bilateral dimension** of air connectivity. While `avia_tf_aca` gives the total seats from Polish airports, this dataset allows analysis by specific origin market (e.g., how many passengers travelled between Poland and Germany in a given month). This is essential for the panel data specification where each origin-destination pair is an observation unit.

**Processing notes:** The `geo` column indicates the partner country, not the reporting country. All data represents departures from Poland to the listed partner country (and is approximately symmetric for arrivals given round-trip travel patterns). The `tra_meas` value is "Passengers on board (departures)" for Poland-origin data and "Passengers carried" for the reciprocal observations from origin countries (e.g., Spain). Care must be taken to avoid double-counting.

**Limitation:** This dataset contains passengers (demand realised), not seats (capacity offered). For bilateral capacity analysis, OAG data would be needed (not available).

---

### 5.3 Air Passengers by Individual Polish Airport (SUPPLEMENTARY)

| Attribute | Value |
|---|---|
| **File** | `transport/avia_tf_apal_passengers_airports_PL-2003-.csv` |
| **Source** | Eurostat, dataset `avia_tf_apal` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/avia_tf_apal/default/table |
| **Frequency** | Monthly |
| **Period** | 2004-01 to 2025-08 (varies by airport) |
| **Geography** | Polish airports: Bydgoszcz, Gdańsk, Katowice, Kraków, Łódź, Lublin, Warsaw (Chopin + Modlin), Wrocław, Poznań, Rzeszów, Szczecin |
| **Transport measure** | Passengers carried |
| **Airline** | All airlines |
| **Dimensions** | 1,200 observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Number of passengers carried |
| **Missing data** | `OBS_VALUE`: 0% |
| **Download date** | December 2025 |

**Role in the thesis:** **Supplementary dataset** for descriptive analysis only (not used in forecasting models). Provides airport-level granularity to illustrate the spatial distribution of air traffic across Poland and the growth of regional airports. For example, the data shows the dramatic impact of COVID-19 on Bydgoszcz airport (from ~47,000 passengers in August 2019 to 0 in April 2020).

**Redundancy note:** The passenger counts at the airport level overlap with the PAS_BRD component of `avia_tf_aca` (Section 5.1). This file is retained for its longer historical coverage (starting 2004 vs. 2010 for `avia_tf_aca`) and for airports not covered in the other dataset.

---

## 6. Tourism Block

### 6.1 Nights Spent at Tourist Accommodation — Monthly (DEPENDENT VARIABLE)

| Attribute | Value |
|---|---|
| **File** | `tourism/tour_occ_nights_accommodation_PL_2003-.csv` |
| **Source** | Eurostat, dataset `tour_occ_nim` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/tour_occ_nim/default/table |
| **Frequency** | Monthly |
| **Period** | 2011-01 to 2025-11 |
| **Geography** | Poland; EU-28 aggregate |
| **Residency** | Foreign country (non-residents), by country of origin |
| **Unit** | Number (nights) and percentage change vs. same period previous year |
| **NACE categories** | Hotels and similar; Holiday and short-stay; Camping; Combined categories |
| **Dimensions** | 2,000+ observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Number of nights spent or YoY % change |
| **Missing data** | `OBS_VALUE`: 0%; `OBS_FLAG`: 99.9% missing |
| **Download date** | February 2026 |

**Role in the thesis:** This is the **dependent variable** (TD_it) — the measure of tourism demand to be forecasted. Overnight stays (pernoctaciones) is the preferred demand proxy in European tourism research because it captures both the volume and duration of visits, unlike simple arrival counts.

**Residency filter:** The dataset is filtered to capture **foreign/non-resident** overnight stays (`c_resid` = "Foreign country" and specific origin countries), as this thesis models inbound tourism demand from international source markets. Eurostat coverage for this variable begins in 2011, which defines the effective start of the dependent variable series.

---

### 6.2 Tourism Infrastructure — Establishments and Bed-places

| Attribute | Value |
|---|---|
| **File** | `tourism/tour_cap_nat__tourism-infraestructure.csv` |
| **Source** | Eurostat, dataset `tour_cap_nat` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/tour_cap_nat/default/table |
| **Frequency** | Annual |
| **Period** | 1990–2024 |
| **Geography** | Poland, Spain, Euro area aggregate |
| **Unit** | Number (of establishments/bedrooms/bed-places) and percentage change |
| **Accommodation types** | Hotels and similar; Camping; Holiday and short-stay; Combined categories |
| **Dimensions** | 1,885 observations × 11 columns |
| **Key variable** | `OBS_VALUE`: Number of bed-places / establishments |
| **Missing data** | `OBS_VALUE`: 0%; `OBS_FLAG`: 92.2% missing |
| **Download date** | February 2026 |

**Role in the thesis:** Provides the **supply-side context** — the evolution of accommodation capacity in Poland. Used descriptively in Chapter 4 to show how the tourism supply infrastructure has expanded alongside growing demand. Not used as an explanatory variable in the demand models (supply is not typically included in demand equations to avoid simultaneity bias).

---

### 6.3 Employment in Tourism Industries — Quarterly

| Attribute | Value |
|---|---|
| **File** | `tourism/tour_lfsq6r2__employment-tourism-industries.csv` |
| **Source** | Eurostat, dataset `tour_lfsq6r2` |
| **URL** | https://ec.europa.eu/eurostat/databrowser/view/tour_lfsq6r2/default/table |
| **Frequency** | Quarterly |
| **Period** | 2008-Q1 to 2025-Q2 |
| **Geography** | Spain, Poland |
| **Unit** | Thousand persons |
| **Sectors** | Accommodation and food services; Accommodation; Travel agencies; Air transport; Total NACE |
| **Breakdowns** | By sex, by full-time/part-time, by employment status |
| **Dimensions** | 12,000+ observations × 13 columns |
| **Key variable** | `OBS_VALUE`: Employment in thousands |
| **Missing data** | `OBS_VALUE`: 7.65%; `OBS_FLAG`: 64.8% present (many flags) |
| **Download date** | February 2026 |

**Role in the thesis:** Provides **labour market context** for the tourism sector. Useful for the socioeconomic impact discussion in the introduction and conclusions. The relatively high flag rate (35%) and non-negligible missingness (7.65%) reflect the difficulty of measuring tourism employment consistently through Labour Force Surveys.

---

### 6.4 UN Tourism — Inbound Arrivals by Region

| Attribute | Value |
|---|---|
| **File** | `tourism/UN_Tourism_inbound_arrivals_by_region_12_2025.xlsx` |
| **Source** | World Tourism Organization (UN Tourism) |
| **URL** | https://www.untourism.int/tourism-statistics/tourism-data-inbound-tourism |
| **Frequency** | Annual |
| **Period** | 1995–2024 |
| **Geography** | All countries worldwide (reporter = destination; partner = origin region) |
| **Unit** | Thousand trips |
| **Indicator** | Inbound trips by area of residence — overnight visitors (tourists) |
| **Release** | December 2025 |
| **Format** | Excel (.xlsx), two sheets: Overview + Data |

**Role in the thesis:** Provides **annual arrival figures** by origin region for Poland, serving as the reference benchmark for total inbound tourism volumes. Used in the descriptive analysis to show the long-run trend (1995–2024) and to validate the Eurostat overnight-stays data. The regional breakdown (Europe, Americas, Asia-Pacific, etc.) helps contextualise the dominance of European markets.

**Citation:** World Tourism Organization (2025). All Countries: Inbound Tourism: Arrivals by region 1995–2024 (12.2025). UN Tourism Statistics Database, Madrid.

---

### 6.5 UN Tourism — Inbound Expenditure by Purpose

| Attribute | Value |
|---|---|
| **File** | `tourism/UN_Tourism_inbound_expenditure_12_2025.xlsx` |
| **Source** | World Tourism Organization (UN Tourism) |
| **URL** | https://www.untourism.int/tourism-statistics/tourism-data-inbound-tourism |
| **Frequency** | Annual |
| **Period** | 1995–2024 |
| **Geography** | All countries worldwide |
| **Unit** | Million USD |
| **Indicator** | Inbound tourism expenditure by main purpose of trip |
| **Release** | December 2025 |
| **Format** | Excel (.xlsx), two sheets: Overview + Data |

**Role in the thesis:** Provides **tourism expenditure** data as an alternative demand measure. Following Song et al. (2010), who found that arrivals and expenditure are driven by different factors, this data enables a robustness check: do the model rankings change when forecasting expenditure instead of arrivals/nights? Used primarily in the descriptive chapter and potentially in extended analysis.

**Citation:** World Tourism Organization (2025). All Countries: Inbound Tourism: Expenditure by main purpose of the trip 1995–2024 (12.2025). UN Tourism Statistics Database, Madrid.

---

## 7. Variable Construction Guide

This section documents how the raw datasets are combined to produce the key analytical variables.

### 7.1 Relative Tourism Price (P_it)

**Formula** (Song et al., 2010):

$$P_{it} = \frac{CPI_{PL,t} / EX_{PLN/EUR,t}}{CPI_{i,t} / EX_{i/EUR,t}}$$

| Component | Source | Dataset | Variable |
|---|---|---|---|
| CPI_PL (monthly) | Eurostat | `prc_hicp_midx` | HICP All-items, geo = Poland |
| CPI_i (monthly) | Eurostat | `prc_hicp_midx` | HICP All-items, geo = origin country i |
| EX_PLN/EUR (monthly) | Eurostat | `ert_bil_eur_m` | PLN per EUR, currency = Polish zloty |
| EX_i/EUR (monthly) | Eurostat | `ert_bil_eur_m` | Currency i per EUR (= 1.0 for Eurozone countries) |

**Interpretation:** P > 1 means Poland is more expensive than the origin country (adjusted for exchange rates); P < 1 means Poland is cheaper. A rising P signals deteriorating price competitiveness.

### 7.2 Substitute Destination Price (Ps_t)

$$P^s_t = \sum_{j \neq PL} \left(\frac{CPI_{j,t}}{EX_{j/EUR,t}}\right) \cdot w_{j,t}$$

where j ∈ {Czechia, Hungary, Croatia, Greece} and weights w_{j,t} are based on each destination's share of total tourism arrivals in the previous year.

### 7.3 Load Factor

$$LF_t = \frac{PAS\_BRD_t}{ST\_PAS_t}$$

| Component | Source | Dataset | Filter |
|---|---|---|---|
| PAS_BRD | Eurostat | `avia_tf_aca` | tra_meas = "Passengers on board" |
| ST_PAS | Eurostat | `avia_tf_aca` | tra_meas = "Passengers seats available" |

Both aggregated across all Polish airports.

### 7.4 Tourism Intensity

$$TI_t = \frac{TD_t}{POP_{PL,t}}$$

where TD is total overnight stays and POP is Poland's population.

---

## 8. Data Quality Summary

### 8.1 Coverage Matrix

| Variable | Frequency | Start | End | Countries | Status |
|---|---|---|---|---|---|
| Real GDP (CLV 2010) | Quarterly | 1995-Q1 | 2025-Q3 | 10 | `!` Ready |
| Nominal GDP (market prices) | Quarterly | 1995-Q1 | 2025-Q2 | PL only | `!` Ready |
| HICP Monthly | Monthly | 2003-01 | 2025-12 | 14 + EU | `!` Ready |
| HICP Annual | Annual | 2003 | 2025 | 14 | `!` Ready (descriptive only) |
| Exchange rates (monthly) | Monthly | 2003-01 | 2026-02 | PLN, USD, GBP, SEK, CZK, HUF | `!` Ready |
| PPP Price Levels | Annual | 1995 | 2024 | 35+ | `!` Ready |
| Population | Annual | 1990 | 2025 | 45+ | `!` Ready |
| Net Earnings | Annual | 2000 | 2024 | 25+ | `!` Ready |
| Consumer Confidence | Monthly | 2005-01 | 2026-02 | 8+ | `!` Ready |
| Seats + Flights (avia_tf_aca) | Monthly | 2010-01 | 2025-10 | PL airports | `!` Ready |
| Passengers bilateral (avia_paoc) | Monthly | 2003-01 | 2025-12 | 8 pairs | `!` Ready |
| Passengers by airport (avia_tf_apal) | Monthly | 2004-01 | 2025-08 | PL airports | `?` Supplementary |
| Overnight stays (tour_occ_nim) | Monthly | 2011-01 | 2025-11 | PL, by origin | `!` Ready |
| Tourism infrastructure | Annual | 1990 | 2024 | PL, ES, EA | `!` Ready |
| Tourism employment | Quarterly | 2008-Q1 | 2025-Q2 | PL, ES | `!` Ready |
| UN Tourism arrivals | Annual | 1995 | 2024 | Global | `!` Ready |
| UN Tourism expenditure | Annual | 1995 | 2024 | Global | `!` Ready |
| IMF WEO | Annual | 1980 | 2027 | PL | `!` Ready |
| OWID GDP | Annual | 1950 | 2022 | Global | `!` Context only |

### 8.2 Known Limitations

1. **Air seat capacity (`avia_tf_aca`) starts in 2010**, while the study period begins in 2003. Models that include seats as an explanatory variable operate on a shorter estimation window (~180 monthly observations). For the 2003–2009 period, bilateral passengers from `avia_paoc` serve as a proxy for connectivity, with this methodological splice documented in the thesis.

2. **Croatia HICP coverage** is limited to 2023 onwards. The substitute price index calculation (Section 7.2) uses alternative weighting for earlier periods when Croatia CPI is unavailable.

3. **IMF WEO projections** currently cover Poland only. For the full scenario analysis, origin-country GDP trajectories (DE, UK, FR, etc.) are derived from the IMF's published regional growth forecasts applied to the Eurostat baseline.

4. **Tourism employment data** (`tour_lfsq6r2`) has relatively high missingness (7.65%) and flag rates, reflecting the inherent difficulty of measuring tourism employment through Labour Force Surveys. This dataset is used only for descriptive context, not in forecasting models.

### 8.3 Potential Enhancements

The following data sources could further enrich the analysis but are not required for the core methodology:

- **Google Trends data** for search terms such as "holidays Poland" or "flights to Krakow" — a potential leading indicator for ML models.
- **Oil price data** (Brent crude, monthly) as a proxy for transport costs affecting airfares and tourism demand. Nevertheless, Price Level Indices show decently enough the evolution in this term.
- **OAG (Official Aviation Guide)** data for bilateral seat capacity by route, if academic access becomes available. However, its license is limited and it would require a big expenditure.

---

## 9. Temporal Alignment Strategy

The datasets span different frequencies. The following alignment strategy will be applied:

| Source frequency | Target: Monthly | Method |
|---|---|---|
| Monthly | — | Direct use |
| Quarterly | Monthly | Cubic spline interpolation (GDP, employment) |
| Annual | Monthly | Cubic spline interpolation (population, PPP, earnings) |

All interpolated series will be documented and the interpolation method justified in the methodology chapter. Robustness checks using only quarterly/annual models will be conducted to verify that interpolation does not introduce artefactual results.

---

## 10. References

- Song, H., Witt, S. F., & Li, G. (2010). *The Advanced Econometrics of Tourism Demand*. Routledge.
- Eurostat (2026). Statistical Database. European Commission. https://ec.europa.eu/eurostat/data/database
- International Monetary Fund (2025). World Economic Outlook Database, April 2025. https://www.imf.org/en/Publications/WEO
- World Tourism Organization (2025). Tourism Statistics Database. UN Tourism. https://www.untourism.int/tourism-statistics
- Our World in Data (2023). Gross Domestic Product. https://ourworldindata.org/
