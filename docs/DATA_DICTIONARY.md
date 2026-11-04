# Data Dictionary and Provenance

**Source:** [Ishita95-AIML/-Fashion-Retail-Sales-Dataset](https://github.com/Ishita95-AIML/-Fashion-Retail-Sales-Dataset)  
**CSV file:** `Fashion_Retail_Sales.csv`  
**Snapshot checked:** 04 November 2026  
**Observed shape:** 3,400 rows × 6 columns

| Field | Meaning from source metadata / CSV | Type after parsing | Observed missing |
|---|---|---|---:|
| Customer Reference ID | Anonymized customer reference identifier | String | 0 |
| Item Purchased | Name of fashion item purchased | Category / string | 0 |
| Purchase Amount (USD) | Purchase amount in USD | Numeric | 650 |
| Date Purchase | Purchase date, DD-MM-YYYY | Datetime | 0 |
| Review Rating | Customer rating, expected 1–5 | Numeric | 324 |
| Payment Method | Recorded payment method (Credit Card or Cash) | Category / string | 0 |

## Provenance notes

- The dataset metadata describes the 3,400 records as simulated fashion retail sales data.
- The source repository's README lists a different schema. The actual CSV and its metadata are treated as authoritative for this project.
- Amount and rating blanks are retained as missing.
- Monthly amount sums exclude missing amounts.
- The analysis snapshot contains only five rows in October 2023.
- The 43 amount values above USD 1,000 are flagged for source verification; they are not automatically removed.
