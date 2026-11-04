# Exploratory Data Analysis of Apparel & Fashion Retail Sales

**Internship Week 2 report**  
**Prepared by:** Sharthak Singh  
**Analysis snapshot:** 04 November 2026

## Executive summary

This project explores 3,400 rows of fashion retail purchase data. The six fields are Customer Reference ID, Item Purchased, Purchase Amount (USD), Date Purchase, Review Rating, and Payment Method. The analysis covers data profiling, missing-value treatment, outlier assessment, product frequency, monthly observed amounts, payment mix, review ratings, and practical recommendations.

The dataset is useful for an educational EDA exercise, but it should not be used as an audited revenue source without further validation. Purchase amount is missing in 650 rows (19.1%) and review rating is missing in 324 rows (9.5%). Of the 2,750 observed purchase amounts, 43 exceed USD 1,000. The median is USD 110, compared with a mean of USD 156.71 and an interquartile range from USD 57 to USD 155. The large tail strongly affects the mean.

Credit card appears in 1,770 rows (52.1%) and cash in 1,630 rows (47.9%). The most frequent item names are Belt (90 rows), Skirt (88), Shorts (87), and Pants (86). Observed monthly amount totals are highest in December 2022 (USD 46,851) and May 2023 (USD 45,352). October 2023 contains only five records, so it is a partial period. The Pearson correlation between amount and rating on 2,487 complete cases is approximately 0.045, a near-zero linear relationship in this sample.

## 1. Dataset description and relevance

**Source:** [Fashion Retail Sales Dataset](https://github.com/Ishita95-AIML/-Fashion-Retail-Sales-Dataset)  
**CSV:** [Fashion_Retail_Sales.csv](https://github.com/Ishita95-AIML/-Fashion-Retail-Sales-Dataset/blob/main/Fashion_Retail_Sales.csv)  
**Metadata:** `fashion-retail-sales-metadata.json` in the same repository.

The metadata describes the file as 3,400 simulated fashion retail sales records. It is a six-column CSV:

| Field | Type | Use |
|---|---|---|
| Customer Reference ID | Identifier | Customer reference; not a customer profile |
| Item Purchased | Categorical | Product-name frequency |
| Purchase Amount (USD) | Numeric | Observed purchase amount |
| Date Purchase | DD-MM-YYYY | Time-based summaries |
| Review Rating | Numeric, 1–5 | Customer feedback |
| Payment Method | Categorical | Cash/card comparison |

The period runs from 02 October 2022 to 01 October 2023. The dataset is relevant for basic retail analysis because it joins purchase value, item name, date, rating, and payment type. It does not include quantity, transaction ID, product category, discount, cost or margin, returns, inventory, store/channel, promotions, or customer demographics. Those gaps constrain demand and profitability conclusions.

A documentation mismatch exists: the source repository README describes a different schema (including Transaction_ID, Quantity_Sold, and Store_Location), while the actual CSV and metadata expose the six fields above. This project follows the actual CSV and its metadata.

## 2. Data understanding and cleaning

The CSV was loaded and inspected for dimensions, names, data types, sample rows, and null counts. Purchase Amount (USD) and Review Rating were converted to numeric values; blanks were preserved as missing. Date Purchase was parsed explicitly using day-month-year format. All non-missing ratings fall within the expected 1–5 range, and the date parser yields the period stated above.

| Field | Missing rows | Missing rate |
|---|---:|---:|
| Purchase Amount (USD) | 650 | 19.1% |
| Review Rating | 324 | 9.5% |
| Other four fields | 0 each | 0.0% |

Missing purchase amounts were not changed to zero and were not mean-imputed. Monthly sums exclude rows with missing amounts, so they are **observed amount totals**, not complete revenue. Ratings are analysed only where present. The absence of evidence about the missingness mechanism makes imputation risky.

### Outlier assessment

For 2,750 observed purchase amounts, the minimum is USD 10, Q1 is USD 57, median USD 110, Q3 USD 155, and maximum USD 4,932. IQR is USD 98, giving a 1.5×IQR upper fence of USD 302. There are 43 values above USD 1,000 (1.56% of observed amounts); all are well beyond the central range.

These values were flagged, not deleted. The fields do not reveal whether they are data-entry errors, alternate units/currency, bundled purchases, or legitimate high-value purchases. They should be checked against original order records. The CSV has no explicit transaction ID, so potential duplicate transactions cannot be reliably identified from repeated customer references alone.

## 3. Exploratory findings

### 3.1 Purchase amount distribution

The observed amount total is USD 430,952, the mean USD 156.71, and the median USD 110. Since 43 extreme values exceed USD 1,000, the median and quartiles better represent the centre than the mean. The dataset does not clarify whether amount refers to a single item or the whole basket, so average basket value should not be claimed.

### 3.2 Product mix

The top row counts are Belt 90, Skirt 88, Shorts 87, Pants 86, Tank Top 82, and T-shirt 82. The differences are small relative to the full dataset. These are transaction-row counts, not units sold, because quantity is absent. The item list mixes apparel, accessories, and footwear, so a controlled category taxonomy is needed before category-level decisions.

### 3.3 Monthly pattern

The observed monthly sums (missing amounts excluded) are:

| Month | Rows | Rows with amount | Observed sum (USD) |
|---|---:|---:|---:|
| Oct 2022 | 309 | 246 | 30,812 |
| Nov 2022 | 238 | 198 | 35,129 |
| Dec 2022 | 306 | 248 | 46,851 |
| Jan 2023 | 292 | 237 | 29,887 |
| Feb 2023 | 251 | 198 | 33,879 |
| Mar 2023 | 277 | 232 | 39,380 |
| Apr 2023 | 295 | 235 | 40,220 |
| May 2023 | 308 | 250 | 45,352 |
| Jun 2023 | 262 | 209 | 35,542 |
| Jul 2023 | 303 | 246 | 33,176 |
| Aug 2023 | 301 | 248 | 35,809 |
| Sep 2023 | 253 | 198 | 24,492 |
| Oct 2023* | 5 | 5 | 423 |

December 2022 is the highest observed total and May 2023 the next highest. October 2023 is an incomplete month and is not comparable with the full months. The one partial year cannot establish reliable seasonality. Missing amounts may also understate each monthly total.

### 3.4 Payment method

Credit card represents 52.1% of rows; cash represents 47.9%. The observed mean amount is USD 160.37 for credit-card rows and USD 152.70 for cash rows. Mean ratings are 3.003 and 2.995, respectively. The differences are small and do not justify a strong claim about payment method and spend or satisfaction.

### 3.5 Ratings and relationship with amount

There are 3,076 non-missing ratings; the mean and median are approximately 3.0, with values from 1 to 5. There are 1,488 ratings below 3, 69 equal to 3, and 1,519 above 3. For 2,487 records with both amount and rating, Pearson r is 0.045. This indicates a near-zero linear association in this sample, not proof that price never affects satisfaction. Missing reviews, nonlinear patterns, and confounding variables may still matter.

## 4. Visualization choices

Four visuals are included and regenerated by the analysis script:

1. **Box plot of purchase amount:** useful for median, quartiles, and spread in a skewed numeric variable. Extreme observations are called out separately so they do not compress the central range.
2. **Horizontal bar chart of product counts:** suitable for ranking categorical item names; counts are rows, not units.
3. **Monthly line chart:** reveals peaks and troughs in the time sequence; observed totals are incomplete when amount is missing, and the last month is partial.
4. **Donut chart of payment mix:** communicates shares for two mutually exclusive categories without implying profitability.

## 5. Business implications and recommendations

### Opportunities

- Use item-level counts as an initial merchandising signal, then validate with units sold, stock-outs, margin, and returns before changing replenishment.
- Investigate December and May peaks against promotion calendars, holidays, and operational records; gather at least two full years before seasonal planning.
- Analyse low ratings by item and date after adding review text, product attributes, and return/exchange outcomes.
- Retain both cash and card options; examine differences by store, channel, or segment only after those fields are collected.

### Risks

- Missing purchase amounts in 19.1% of rows make observed totals incomplete; blanks treated as zero would bias revenue down.
- The 43 values above USD 1,000 pull the mean upward and require source checks.
- Five records in October 2023 create partial-period bias.
- A simulated dataset without quantity, margin, store, channel, and promotions cannot support causal claims, profitability conclusions, or stand-alone inventory optimization.

### Recommended actions

1. Verify the 43 extreme amounts against receipts/order records, including currency, decimal placement, and amount definition.
2. Investigate missingness by month, item, and payment method before deciding whether any imputation is appropriate.
3. Add stable transaction IDs and document the row grain; include quantity, category, discounts, returns, margin, store/channel, and promotion fields.
4. Create an item taxonomy and distinguish complete periods from partial periods in dashboards.
5. Publish medians and validated/trimmed means alongside totals, and include a data-quality panel.
6. Extend the history to at least two complete years before forecasting or claiming seasonality.

## 6. Limitations and conclusion

The source metadata identifies the records as simulated. Results therefore demonstrate an EDA workflow, not verified performance of a real retailer. Row counts are a proxy for item frequency, not unit demand. Missingness may be systematic, extreme values may be genuine or erroneous, and ratings represent only submitted reviews. Correlation is not causation, and monthly observed totals are not audited revenue.

The main value of this project is a data-quality-aware baseline: clear missing-value treatment, flagged anomalous amounts, a view of product and payment mix, monthly observed patterns, and concrete validation steps for a future retail dataset with richer operational fields.

## Reproducibility

Install the dependencies and run the analysis from the repository root:

```bash
pip install -r requirements.txt
python src/eda_analysis.py
```

The script creates `outputs/eda_summary.json`, monthly and payment summary CSVs, and PNG/SVG charts in `visualizations/`. The notebook provides the same workflow in stages. Re-run it if the upstream CSV changes; reported values refer to the retrieved 3,400-row file snapshot.
