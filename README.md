# Internship Week 2 — Apparel & Fashion Retail EDA

Exploratory data analysis (EDA) of a public fashion retail sales dataset. The project examines purchase amounts, product mix, purchase dates, customer review ratings, and payment methods, with explicit attention to data-quality limitations.

## Project files

- `report/Week_2_EDA_Report.md` — detailed, standalone findings and business recommendations.
- `notebooks/apparel_eda.ipynb` — reproducible notebook (loads the CSV from the source URL).
- `src/eda_analysis.py` — reusable EDA and chart-generation script.
- `visualizations/` — generated charts.
- `requirements.txt` — Python dependencies.

## Dataset

The analysis uses **Fashion_Retail_Sales.csv** from [Ishita95-AIML/-Fashion-Retail-Sales-Dataset](https://github.com/Ishita95-AIML/-Fashion-Retail-Sales-Dataset). The dataset metadata describes 3,400 simulated fashion retail records and six columns: Customer Reference ID, Item Purchased, Purchase Amount (USD), Date Purchase, Review Rating, and Payment Method.

Source CSV: https://github.com/Ishita95-AIML/-Fashion-Retail-Sales-Dataset/blob/main/Fashion_Retail_Sales.csv

The CSV is not bundled here; the notebook and script download it from the public source. A copy of the source attribution and dataset schema is retained in the report.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/eda_analysis.py
```

Open `notebooks/apparel_eda.ipynb` in Jupyter for the step-by-step workflow.

## Important data-quality note

The CSV has 650 missing purchase amounts (19.1%) and 324 missing ratings (9.5%). Of the 2,750 observed purchase amounts, 43 values are above USD 1,000, while the median is USD 110 and the third quartile is USD 155. These extreme values are treated as potential anomalies requiring source verification, not silently deleted or assumed to be genuine sales. Monthly totals use observed amounts only and can understate actual revenue; the final month in the extract is sparse and should not be compared directly with full months.

The source repository's overview README describes a different field schema; this project follows the actual six-column CSV and its metadata instead.

## Scope and ethics

This is descriptive analysis of an educational/simulated dataset. It does not identify real customers or establish causal relationships. Recommendations are hypotheses for a retailer to validate against operational data.

## Author

Prepared for an internship Week 2 EDA task.
