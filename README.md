# Indonesia Tariff Analysis: Section 122 and the Post-SCOTUS Trade Landscape

**Policy brief and supporting analysis by the Indonesian Institute for Foreign Affairs (IIFA), UIII**

> *Teguh Yudo Wicaksono, Rima P Artha, Philips J. Vermonte*
> *February 28, 2026*

---

## What This Project Does

On February 19, 2026, Indonesia signed a bilateral trade agreement (ART) with the United States. The next day, the Supreme Court struck down the legal basis of the entire agreement. This repository contains the policy brief and underlying calculations analyzing what that means for Indonesia's exporters.

The core analytical task is computing Indonesia's **average tariff rate (ETR — effective tariff rate)** under five policy scenarios, incorporating two corrections that prior analyses had missed:

1. **Annex II exemptions for Section 122** — The S122 proclamation carries product exemptions (coffee, cocoa, semiconductors, energy, partial rubber) that mirror the IEEPA Annex II list. Not applying these overstated the S122 ETR by ~1.3 pp.
2. **2025 trade data** — Full-year 2025 US import data ($34.84B, up 24% from 2024) reflects pre-tariff front-loading and changes sector weights.

The corrected headline finding: **Section 122 at 15% produces an average tariff rate of 19.0% for Indonesia — 0.7 percentage points *below* the negotiated deal rate of 19.7%**, not above it as initially reported.

---

## Key Results

| Scenario | Period | ETR | Est. Duties |
|----------|--------|-----|-------------|
| 1. Baseline | Pre-Apr 2025 | 5.0% | $1.74B |
| 2. Liberation Day | Apr 2–9, 2025 | 36.6% | $12.75B |
| 3. Post-Deal (ART) | Aug 2025–Feb 19, 2026 | 19.7% | $6.86B |
| 4. Post-SCOTUS (10% S122) | Feb 20, 2026 | 14.5% | $5.06B |
| 5. **S122 at 15%** (current) | **Feb 21, 2026+** | **19.0%** | **$6.63B** |

*ETR = import-weighted average tariff. 2025 import base: $34.84B. S122 scenarios apply Annex II corrections.*

### Sector Winners and Losers vs. the Deal

| Sector | HS | 2025 ($B) | Deal ETR | S122 15% ETR | Change |
|--------|----|-----------|----------|--------------|--------|
| Electronics | 85 | 7.84 | 14.1% | 15.1% | +1.0 pp |
| Footwear | 64 | 2.97 | 30.0% | 26.0% | **−4.0 pp** |
| Apparel (knit) | 61 | 2.52 | 29.1% | 27.0% | **−2.1 pp** |
| Apparel (woven) | 62 | 2.21 | 29.1% | 27.0% | **−2.1 pp** |
| **Palm Oil** | **15** | **2.32** | **2.0%** | **16.5%** | **+14.5 pp** |
| **Rubber** | **40** | **1.71** | **3.0%** | **14.0%** | **+11.0 pp** |
| Furniture | 94 | 1.55 | 20.5% | 16.5% | **−4.0 pp** |
| Coffee | 09 | 0.57 | 1.5% | 1.5% | 0 pp *(exempt)* |
| Cocoa | 18 | 0.77 | 3.0% | 3.0% | 0 pp *(exempt)* |

---

## Repository Contents

```
report/
├── main.tex                  # Policy brief (LaTeX source)
├── main.pdf                  # Compiled PDF (16 pages)
├── winners_losers.png        # Sector ETR comparison chart
└── chart_winners_losers.py   # Chart generation script

data/
├── calculate_etr_2025.py          # ETR calculator (Python) — main script
├── calculate_indonesia_etr.R      # Original ETR calculator (R, Yale model)
├── etr_summary_2025.csv           # 5-scenario ETR summary
├── etrs_by_hts2_12-4.csv          # Yale model: Post-Deal HTS2 ETRs (reference)
├── etrs_by_hts2_2-20_with-s122.csv   # Yale model: S122 10%, no exemptions
├── etrs_by_hts2_2-21_with-s122-15.csv # Yale model: S122 15%, no exemptions
├── etrs_by_hts2_s122_10_corrected.csv  # Corrected: S122 10% + Annex II
├── etrs_by_hts2_s122_15_corrected.csv  # Corrected: S122 15% + Annex II
├── indonesia_us_trade_2024.csv    # 2024 HTS2-level US imports from Indonesia
├── indonesia_us_trade_2025.csv    # 2025 HTS2-level US imports (Census API)
└── etr_calculations.csv           # Manual HTS2-level hand calculations
```

---

## Methodology

### ETR Formula

$$\text{ETR} = \frac{\sum_i \text{applicable\_rate}_i \times \text{import\_value}_i}{\sum_i \text{import\_value}_i}$$

where *i* is each HTS 2-digit chapter. The applicable rate is:

```
applicable_rate = MFN_rate + max(section_232_rate, reciprocal_or_s122_rate)
```

with a **stacking rule**: Section 232 and reciprocal/S122 are mutually exclusive — the higher rate governs. Products are not double-charged.

### Annex II Correction

The Section 122 proclamation carries an Annex II of exempt products mirroring the IEEPA Annex II (pharmaceuticals, semiconductors, energy, coffee, cocoa, critical minerals). For each HTS 2-digit chapter *c*, the exempt fraction is estimated from the Yale Budget Lab's 12-4 scenario output:

$$\alpha_c = \max\!\left(0,\; 1 - \frac{\text{ETR}^{12\text{-}4}_c}{0.19}\right) \quad \text{if } \text{ETR}^{12\text{-}4}_c \leq 0.19$$

Chapters where the 12-4 ETR exceeds 19% are Section 232-dominated and receive no correction. The corrected S122 ETR is:

$$\text{ETR}^{S122,\text{corrected}}_c = \text{ETR}^{S122,\text{current}}_c - \alpha_c \times r_{S122}$$

### Data Sources

| Source | What | Where |
|--------|------|--------|
| US Census Bureau API | 2024 and 2025 monthly US imports from Indonesia (HTS2, CTY_CODE=5600) | `https://api.census.gov/data/timeseries/intltrade/imports/hs` |
| Yale Budget Lab Tariff-ETR model | HTS10-level incremental ETR by scenario | [GitHub](https://github.com/Budget-Lab-Yale/Tariff-ETRs) |
| USITC HTS | MFN tariff rates | [usitc.gov](https://hts.usitc.gov) |
| WTO Tariff Profiles | Trade-weighted average MFN rates | [wto.org](https://www.wto.org/english/res_e/statis_e/daily_update_e/tariff_profiles.zip) |

**Note on Census API**: The annual endpoint (`time=2025`) does not reliably filter by `CTY_CODE`. Always use monthly summation (`time=2025-01` through `time=2025-12`) for country-specific data.

---

## Reproducing the Results

### Requirements

```bash
# Python
pip install requests pandas numpy

# LaTeX (for compiling the brief)
# Requires: pdflatex with booktabs, tabularx, longtable, hyperref, setspace
```

### Run the ETR Calculator

```bash
cd data/
python3 calculate_etr_2025.py
```

This will:
1. Download 2025 Census Bureau trade data for Indonesia (HTS2 level, ~45 sec)
2. Load Yale model HTS2 ETR outputs
3. Apply Annex II exemption corrections
4. Output corrected CSVs and a 5-scenario summary

Expected output:
```
2025 annual total: $34.84B
Corrected S122 10% ETR: 14.5%
Corrected S122 15% ETR: 19.0%
S122 15% is BELOW deal by 0.7 pp
```

### Compile the Policy Brief

```bash
cd report/
pdflatex main.tex
pdflatex main.tex   # Run twice to resolve cross-references
```

---

## Policy Context

**What happened (in 72 hours):**

| Date | Event |
|------|-------|
| Feb 19, 2026 | US–Indonesia ART signed; 1,819 product lines exempted; Freeport MoU signed |
| Feb 20, 2026 | SCOTUS rules 6–3 IEEPA does not authorize tariffs; Trump invokes S122 at 10% |
| Feb 21, 2026 | Trump raises S122 to 15% — the statutory maximum |

**Key constraints of Section 122 (19 USC § 2132):**
- Maximum rate: **15%** (already reached)
- Maximum duration: **150 days** without Congress (~expires July 20, 2026)
- No country differentiation — Indonesia faces the same rate as Vietnam, EU, etc.

**Indonesia's concessions under the ART** — \$33B in US purchase commitments, 99% tariff elimination on US exports, PT Freeport mining license extended to 2061 — were made in exchange for tariff terms that can no longer be legally delivered.

---

## Authors and Affiliation

**Teguh Yudo Wicaksono** — Senior Fellow, Faculty of Economics and Business, UIII
**Rima P Artha** — Senior Fellow, IIFA, UIII
**Philips J. Vermonte** — Convenor, Faculty of Social Science, UIII

Indonesian Institute for Foreign Affairs (IIFA)
Universitas Islam Internasional Indonesia (UIII)

---

## License

This analysis is released for academic and policy use. Please cite as:

> Wicaksono, T.Y., Artha, R.P., and Vermonte, P.J. (2026). *Indonesia's Tariff Agreement After the US Supreme Court Ruling: What It Means for Indonesia*. Indonesian Institute for Foreign Affairs (IIFA), UIII. February 28, 2026.
