# Calculating Indonesia's Effective Tariff Rate Under U.S. Tariff Policy Scenarios

## 1. Overview

The [Yale Budget Lab](https://budgetlab.yale.edu/) at Yale University maintains a publicly available model for calculating **Effective Tariff Rates (ETRs)** under various U.S. tariff policy scenarios. The model source code is hosted at:

> <https://github.com/Budget-Lab-Yale/Tariff-ETRs>

ETRs represent **import-weighted average tariff rates** across all product lines for a given country. They provide a single summary measure of the tariff burden faced by a trading partner, accounting for the composition of its exports to the United States.

**Indonesia** (Census country code **5600**) is classified in the **"Rest of World" (ROW)** partner group within the model's configuration. This means Indonesia receives the default tariff rates specified for non-individually-named countries, unless a product-level or country-level override applies.

Three tariff scenarios were analyzed in this workflow:

| Scenario | Label | Description |
|----------|-------|-------------|
| `12-4` | December 4, 2025 | IEEPA reciprocal tariffs active at 19% for Indonesia |
| `2-20_with-s122` | February 20, 2025 | Section 122 flat 10% tariff; IEEPA zeroed out |
| `11-17` | November 17, 2025 | Same effective rates as 12-4 for Indonesia |

---

## 2. Model Architecture

The Tariff-ETR model is an **R-based analysis pipeline** that combines U.S. import data with tariff configuration files to produce weighted average tariff rates at the country, sector, and product-chapter levels.

### Data Inputs

- **Import data**: U.S. Census Bureau International Trade import data (2024, HS10-level). These are consumption import values disaggregated by 10-digit Harmonized System codes and partner country.
- **Tariff configuration**: YAML files specifying tariff rates by tariff authority (Section 232, IEEPA, Section 122), country, and product.
- **Crosswalk**: HS10 codes mapped to GTAP (Global Trade Analysis Project) sectors for sector-level aggregation.

### Processing Pipeline

1. **Config parsing** reads YAML tariff schedules and expands them into HS10-by-country rate matrices.
2. **Rate stacking rules** determine how multiple tariff authorities interact (e.g., whether Section 232 supersedes IEEPA, or whether Section 122 stacks on top).
3. **Import-weighted averaging** produces ETRs at the desired level of aggregation.

### Key Source Files

| File | Role |
|------|------|
| `src/main.R` | Entry point; orchestrates the full pipeline |
| `src/config_parsing.R` | Loads Section 232 and IEEPA YAML configs into HS10-by-country rate matrices |
| `src/calculations.R` | `calc_weighted_etr()` applies stacking rules; `calc_overall_etrs()` aggregates to country-level ETRs |
| `src/data_processing.R` | Reads Census Bureau fixed-width import files and prepares the import dataset |

---

## 3. Tariff Scenarios Analyzed

### Scenario 12-4 (December 4, 2025)

This scenario reflects a regime where IEEPA reciprocal tariffs are active for most countries.

| Tariff Authority | Rate for Indonesia | Notes |
|------------------|--------------------|-------|
| IEEPA Reciprocal | **19%** (0.19) | Applied to all HS10 codes not covered by Section 232 |
| IEEPA Fentanyl | **0%** | Only China, Canada, and Mexico have non-zero fentanyl rates |
| Section 232 - Steel | **50%** | Default rate applies to Indonesia |
| Section 232 - Aluminum | **50%** | Default rate applies to Indonesia |
| Section 232 - Autos | **25%** | Default rate applies to Indonesia |
| Section 232 - Furniture | **25%** | Default rate applies to Indonesia |
| Section 232 - Copper | **50%** | Default rate applies to Indonesia |
| Section 232 - Softwood | **10%** | Default rate applies to Indonesia |
| Section 122 | **Not applicable** | Not active in this scenario |

**Stacking rule (non-China):** If a Section 232 tariff covers the HS10 code, use the Section 232 rate. Otherwise, use the IEEPA reciprocal rate plus the IEEPA fentanyl rate.

### Scenario 2-20_with-s122 (February 20, 2025)

This scenario reflects a regime where Section 122 authority is invoked with a flat tariff, while IEEPA tariffs are zeroed out.

| Tariff Authority | Rate for Indonesia | Notes |
|------------------|--------------------|-------|
| IEEPA Reciprocal | **0%** | Zeroed out |
| IEEPA Fentanyl | **0%** | Zeroed out |
| Section 232 | Same as 12-4 | Steel 50%, Aluminum 50%, Autos 25%, etc. |
| Section 122 | **10%** | Flat rate for all countries; **stacks on top of everything** |

**Stacking rule:** Section 122 is additive. Products under Section 232 face 232 rate + 10%; all other products face 0% + 10% = 10%.

### Scenario 11-17 (November 17, 2025)

This scenario produces **identical effective rates to scenario 12-4** for Indonesia. The underlying configuration may differ for other countries, but for Indonesia the same tariff authorities and rates apply.

---

## 4. Data Collection

### Source

Import data were downloaded from the **Census Bureau International Trade API**:

> **API endpoint:** `https://api.census.gov/data/timeseries/intltrade/imports/hs`

### Query Parameters

- **Country filter:** `CTY_CODE=5600` (Indonesia)
- **Time period:** Monthly data for all 12 months of 2024 (January--December)
- **Detail level:** HS10 (10-digit Harmonized System codes)
- **Value field:** `CON_VAL_MO` (consumption import value, monthly)

### Summary Statistics

| Metric | Value |
|--------|-------|
| Unique HS10 product lines | **4,921** |
| Total imports (2024) | **$27,878,045,171** (~$27.88 billion) |
| Months covered | 12 (January--December 2024) |
| Data aggregation | Summed across all 12 months per HS10 code |

---

## 5. Calculation Methodology

### Step 1: Rate Matrix Construction

**Section 232 rates** are loaded from `232.yaml` and expanded into an HS10-by-country tibble. Across all countries in the model, this produces **293,040 combinations**. For Indonesia, the relevant 232 categories are steel, aluminum, autos, furniture, copper, and softwood, each at their respective default rates.

**IEEPA rates** are loaded from `ieepa_reciprocal.yaml` and `ieepa_fentanyl.yaml`. These files use a hierarchical override structure:

```
headline rate (default for all countries)
  -> product-level override (specific HS codes)
    -> product-by-country override (specific HS codes for specific countries)
```

Country mnemonics in the YAML files (e.g., `china`, `eu`, `row`) are resolved to Census country codes using a lookup table. Indonesia falls under the `row` (Rest of World) mnemonic.

### Step 2: Tariff Stacking Rules

The function `calc_weighted_etr()` in `src/calculations.R` implements the stacking logic. For Indonesia (a non-China, non-USMCA country), the rules are:

```
For each HS10 code:
  IF any Section 232 tariff covers this code:
    final_rate = max(applicable 232 rates)
  ELSE:
    final_rate = IEEPA_reciprocal_rate + IEEPA_fentanyl_rate

  IF Section 122 is active:
    final_rate = final_rate + Section_122_rate
```

Key points:
- Section 232 **supersedes** IEEPA for covered products (they do not stack).
- Section 122, when active, **stacks on top** of whatever the base rate is.
- USMCA exemptions are **not applicable** to Indonesia.
- For Indonesia, IEEPA fentanyl is always 0%, so the IEEPA component is simply the reciprocal rate.

### Step 3: Import-Weighted Averaging

The Effective Tariff Rate is calculated as:

$$
\text{ETR} = \frac{\sum_{i} (\text{tariff\_rate}_i \times \text{imports}_i)}{\sum_{i} \text{imports}_i}
$$

where *i* indexes HS10 product lines. This weighted average is computed at multiple levels of aggregation:

- **Overall:** single ETR for all of Indonesia's exports to the U.S.
- **GTAP sector level:** ETR per GTAP sector (using HS10-to-GTAP crosswalk)
- **HTS 2-digit chapter level:** ETR per HTS chapter (first 2 digits of the HS10 code)

---

## 6. Results

### Overall ETR Summary

| Scenario | Overall ETR (pp) | Total Imports (USD) | Under 232 | Under IEEPA | Exempt |
|----------|:----------------:|--------------------:|:---------:|:-----------:|:------:|
| 12-4 | **17.96** | $27,878,045,171 | 8.8% | 80.5% | 10.8% |
| 2-20_with-s122 | **12.68** | $27,878,045,171 | 8.8% | 0.0% | 91.2% |
| 11-17 | **17.96** | $27,878,045,171 | 8.8% | 80.5% | 10.8% |

**Interpretation:**
- Under the IEEPA reciprocal scenario (12-4 and 11-17), Indonesia faces an average tariff of **17.96 percentage points** across all product lines.
- Under the Section 122 scenario (2-20), the average drops to **12.68 percentage points** because the baseline rate falls from 19% to 10%.
- The share of imports under Section 232 is constant at **8.8%** across all scenarios, as 232 coverage is determined by product, not by the policy regime.

### Top Sectors by Import Value (Scenario 12-4)

| GTAP Sector | Description | Imports (USD) | ETR (pp) |
|:-----------:|-------------|:-------------:|:--------:|
| `wap` | Wearing apparel | $4,403,456,981 | 19.00 |
| `lea` | Leather products | $3,290,771,993 | 19.00 |
| `eeq` | Electronic equipment | $2,946,830,718 | 22.16 |
| `omf` | Other manufactures | $2,766,213,714 | 19.86 |
| `ofd` | Other food products | $2,756,521,543 | 15.07 |
| `ele` | Electrical equipment | $2,523,089,468 | 12.66 |
| `rpp` | Rubber and plastic | $1,991,567,004 | 14.36 |
| `vol` | Vegetable oils | $1,985,913,180 | 18.39 |
| `chm` | Chemical products | $1,244,536,048 | 16.75 |
| `lum` | Wood products | $742,321,905 | 18.47 |
| `ome` | Other machinery | $676,861,689 | 22.36 |
| `fmp` | Fabricated metals | $207,609,527 | 38.61 |
| `mvh` | Motor vehicles | $183,827,893 | 24.64 |
| `nfm` | Non-ferrous metals | $169,037,296 | 25.84 |
| `i_s` | Iron and steel | $152,582,577 | 20.30 |

### Key Observations

1. **Most Indonesian exports face the baseline IEEPA reciprocal rate of 19%.** Wearing apparel ($4.4B) and leather products ($3.3B)---Indonesia's two largest export sectors---are both entirely at 19.00 pp, indicating no Section 232 coverage in these categories.

2. **Sectors with Section 232 coverage face significantly higher effective rates.** The impact is most pronounced in:
   - **Fabricated metals** (`fmp`): 38.61 pp --- the highest ETR among major sectors
   - **Non-ferrous metals** (`nfm`): 25.84 pp --- reflecting aluminum and copper tariffs
   - **Motor vehicles** (`mvh`): 24.64 pp --- reflecting the 25% auto tariff
   - **Iron and steel** (`i_s`): 20.30 pp --- reflecting the 50% steel tariff, though many steel products are also exempt

3. **Some sectors face substantially lower effective rates due to zero-rated product exemptions:**
   - Other crops: 0.5 pp
   - Basic pharmaceuticals: 0.7 pp
   - Vegetables and fruits: 0.3 pp
   - These reflect HS10 codes that are exempt from all tariff authorities (the 10.8% "exempt" share)

4. **Only 8.8% of Indonesian imports by value fall under Section 232.** Despite the high rates on 232-covered products (25--50%), the limited product coverage means 232 tariffs have a modest impact on the overall ETR.

5. **Under the Section 122 scenario (2-20), the baseline rate drops from 19% to 10%**, reducing the overall ETR from 17.96 to 12.68 pp---a reduction of 5.28 percentage points.

6. **The Section 122 scenario shifts the burden across sectors:**
   - Sectors with no 232 coverage (e.g., wearing apparel) drop from 19% to 10%
   - Sectors with heavy 232 coverage (e.g., fabricated metals) *increase* from 38.6% to 43.6%, because Section 122's 10% stacks on top of Section 232 rates

---

## 7. Technical Notes

### Bug Fix in Sector Aggregation

A **dplyr sequential evaluation bug** was discovered during this analysis. In `summarise()`, column expressions are evaluated left-to-right within a single call. This creates a subtle trap when a computed column shares a name with an input column:

**Buggy code:**
```r
summarise(
  imports = sum(imports),            # Evaluated first; 'imports' now a scalar
  weighted_etr = sum(etr * imports), # 'imports' here refers to the scalar!
)
```

In this version, `weighted_etr` becomes `sum(etr) * sum(imports)` instead of the correct `sum(etr * imports)`, because by the time the second expression is evaluated, `imports` has been overwritten by the scalar result of `sum(imports)`.

**Fixed code:**
```r
summarise(
  weighted_etr = sum(etr * imports), # Evaluated first with original column vector
  imports = sum(imports),            # Now safe to shadow the column name
)
```

By reordering the expressions so that `weighted_etr` is computed before `imports` is shadowed, the element-wise product `etr * imports` uses the original column vector as intended.

### Data Source Details

- The Census Bureau API returns **monthly consumption import values** (`CON_VAL_MO`).
- These are **true monthly values**, not year-to-date cumulative totals.
- Total 2024 imports of **$27.88 billion** is consistent with known Indonesia--U.S. trade volumes reported by the U.S. Trade Representative and the World Bank.

### Reproducibility

The R script `calculate_indonesia_etr.R` in the repository root can be re-run to reproduce all results. The script performs the following steps:

1. **Downloads** import data from the Census Bureau API for Indonesia (CTY_CODE=5600), all months of 2024.
2. **Sources** the model's native functions from `src/config_parsing.R`, `src/calculations.R`, and `src/data_processing.R`.
3. **Calculates** ETRs across all three scenarios by applying the appropriate tariff configuration files.
4. **Outputs** CSV files to `output/indonesia/`.

To run:
```bash
cd /path/to/Tariff-ETRs
Rscript calculate_indonesia_etr.R
```

---

## 8. Output Files

All output files are written to the `output/indonesia/` directory within the repository.

| File | Description |
|------|-------------|
| `output/indonesia/summary_across_scenarios.csv` | Overall ETR comparison across all three scenarios |
| `output/indonesia/etrs_by_sector_{scenario}.csv` | Sector-level (GTAP) ETRs for each scenario |
| `output/indonesia/etrs_by_hts2_{scenario}.csv` | HTS 2-digit chapter-level ETRs for each scenario |
| `calculate_indonesia_etr.R` | Complete R script for reproducing all results |

---

*This workflow report documents the analysis conducted using the Yale Budget Lab Tariff-ETR model applied to Indonesia's trade data. For questions about the underlying model, refer to the [Yale Budget Lab GitHub repository](https://github.com/Budget-Lab-Yale/Tariff-ETRs).*
