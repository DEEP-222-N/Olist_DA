# Olist E-Commerce Data Analysis

An end-to-end data analysis project on the **Brazilian E-Commerce (Olist)** dataset covering exploratory data analysis, SQL analysis, data cleaning, feature engineering, and interactive Power BI dashboards.

## Table of Contents

- [About Olist](#about-olist)
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Project Workflow](#project-workflow)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [SQL Analysis](#sql-analysis)
- [Data Cleaning & Preprocessing](#data-cleaning--preprocessing)
- [Feature Engineering](#feature-engineering)
- [Power BI Dashboards](#power-bi-dashboards)
- [Key Business Insights](#key-business-insights)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)

---

## About Olist

**Olist** is the largest department store in Brazilian marketplaces. It operates as a **B2C e-commerce platform** that connects small and medium-sized businesses to major online marketplaces like Mercado Livre, Amazon Brazil, and others — all through a single contract and logistics pipeline.

### How Olist Works

```
Seller (Small Business) → Olist Platform → Marketplace (Mercado Livre, Amazon, etc.) → Customer
```

1. **Sellers** register on Olist and upload their product catalogs
2. **Olist** lists these products across multiple marketplaces under the Olist store name
3. **Customers** place orders on marketplaces (they see "Olist Store" as the seller)
4. **Sellers** receive the order, package it, and hand it to Olist's logistics partner for delivery
5. **Customers** receive the product and leave a review

### Key Facts

| Metric | Detail |
|---|---|
| Founded | 2015, Curitiba, Brazil |
| Business Model | Marketplace aggregator (SaaS for sellers) |
| Revenue Source | Commission per sale + subscription fee from sellers |
| Logistics | Partners with carriers for last-mile delivery |
| Marketplaces | Mercado Livre, Amazon, Americanas, and others |
| Data Period | September 2016 — October 2018 |
| Total Orders | ~100K across 99K+ unique customers |

### Why This Dataset is Valuable for Analysis

- **Multi-dimensional:** Orders, payments, reviews, products, sellers, customers, and geolocation — all linked
- **Real-world complexity:** Missing values, duplicates, Portuguese text, date inconsistencies
- **Business-rich:** Enables sales analysis, customer segmentation (RFM), churn prediction, delivery performance, and sentiment analysis — all from one dataset
- **Interview-ready:** Covers the exact types of analysis asked in DA/BI interviews

---

## Project Overview

This project analyzes **100K+ orders** from the Olist marketplace (2016-2018) to uncover business insights across sales, customer behavior, delivery logistics, and customer satisfaction. The analysis pipeline follows the standard data analytics workflow: **EDA → SQL Analysis → Cleaning → Feature Engineering → Visualization**.

The final output is **5 interactive Power BI dashboards** that provide actionable insights for business stakeholders.

---

## Dataset

**Source:** [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

| File | Description | Rows |
|---|---|---|
| `olist_orders_dataset.csv` | Order timestamps and delivery status | 99,441 |
| `olist_customers_dataset.csv` | Customer location data | 99,441 |
| `olist_order_items_dataset.csv` | Product-level order details with price | 112,650 |
| `olist_products_dataset.csv` | Product catalog with dimensions | 32,951 |
| `olist_order_payments_dataset.csv` | Payment details per order | 103,886 |
| `olist_order_reviews_dataset.csv` | Customer review scores and comments | 99,224 |
| `olist_sellers_dataset.csv` | Seller location data | 3,095 |
| `olist_geolocation_dataset.csv` | Zip code coordinates | 1,000,163 |
| `product_category_name_translation.csv` | Portuguese to English category mapping | 71 |

---

## Project Workflow

```
Raw CSVs (9 files)
      │
      ▼
 EDA (eda.ipynb)
 ── Data loading & shape inspection
 ── Missing values analysis
 ── Data types check
 ── Statistical summaries
 ── Univariate & bivariate analysis
 ── Time series trends
 ── Key observations documented
      │
      ▼
 SQL Analysis (sql_analysis.ipynb)
 ── 25 analytical queries on SQLite
 ── JOINs, CTEs, Window Functions
 ── RFM, Pareto, cohort analysis
 ── Business insights via SQL
      │
      ▼
 Data Cleaning (clean_data.py)
 ── Null handling
 ── Date conversion
 ── Category translation
 ── City standardization
 ── Geolocation deduplication
 ── Payment aggregation
      │
      ▼
 Feature Engineering (clean_data.py)
 ── Master orders table (6-way merge)
 ── RFM customer segmentation
 ── Churn classification
 ── Delivery delay metrics
      │
      ▼
 Cleaned CSVs (11 files)
      │
      ▼
 Power BI Dashboards (5 dashboards)
 ── Sales Performance
 ── Customer Churn Analysis
 ── RFM Customer Segmentation
 ── Delivery Performance
 ── Customer Sentiment & Reviews
```

---

## Exploratory Data Analysis (EDA)

**File:** `eda.ipynb` (Jupyter Notebook — 38 cells)

The EDA was performed **before** any data cleaning to understand the raw data and identify issues. Key analyses include:

### Missing Values Identified

| Dataset | Column | Missing | % |
|---|---|---|---|
| Orders | `order_approved_at` | 160 | 0.2% |
| Orders | `order_delivered_carrier_date` | 1,783 | 1.8% |
| Orders | `order_delivered_customer_date` | 2,965 | 3.0% |
| Products | `product_category_name` | 610 | 1.9% |
| Products | `product_weight_g` (and other dimensions) | 2-610 | 0.0-1.9% |
| Reviews | `review_comment_title` | 87,656 | 88.3% |
| Reviews | `review_comment_message` | 58,247 | 58.7% |

### Data Type Issues Found
- All 5 date columns in Orders stored as `object` (string) instead of `datetime`
- Product categories in Portuguese — need translation
- Geolocation table had **1M rows** but only **19K unique zip codes** (~50x duplication)

### Distributions Observed
- **Price:** Right-skewed, median 120 BRL, max 6,735 BRL
- **Review Scores:** Heavily skewed toward 5 stars (57.8% of all reviews)
- **Order Status:** 96.5% delivered, 0.6% cancelled
- **Payment Types:** Credit card 74%, Boleto (bank slip) 19%

### Visualizations Created
- Missing values heatmaps (Orders, Products)
- Order status and payment type bar charts
- Price distribution histogram with median line
- Review score distribution
- Top 15 product categories (horizontal bar)
- Top 10 customer states and cities
- Boxplots for outlier detection (price, freight, weight)
- Correlation heatmap (price vs freight)
- Average payment value by review score
- Delivery days vs review score (bivariate)
- Monthly order volume trend line
- Monthly revenue trend line
- Orders by day of week
- Seller state distribution
- Geolocation duplication analysis

---

## SQL Analysis

**File:** `sql_analysis.ipynb` (Jupyter Notebook — 25 queries)

Loaded all cleaned CSVs into an **in-memory SQLite database** and ran 25 analytical queries covering every major SQL concept tested in DA interviews.

### Queries by Category

| # | Query | SQL Concepts Used |
|---|---|---|
| Q1 | Total orders, revenue, avg order value | COUNT, SUM, AVG, ROUND |
| Q2 | Revenue by state — Top 10 | GROUP BY, ORDER BY, LIMIT, 3-table JOIN |
| Q3 | Order count by status with percentage | Scalar subquery, GROUP BY |
| Q4 | Top 10 product categories by revenue | JOIN, GROUP BY, ORDER BY |
| Q5 | Full order details — 5-table JOIN | INNER JOIN across 5 tables |
| Q6 | Avg review score per seller city | JOIN, GROUP BY, HAVING |
| Q7 | Rank states by revenue | RANK() OVER, window SUM for percentage |
| Q8 | Monthly revenue with running total & MoM growth | LAG(), Running SUM(), derived table |
| Q9 | Top 3 categories per state | ROW_NUMBER() OVER (PARTITION BY) |
| Q10 | Pareto analysis — cumulative revenue % | Cumulative SUM window function |
| Q11 | RFM analysis with recency buckets | Multi-CTE, CASE, julianday(), GROUP BY |
| Q12 | Late delivery impact on reviews | Multi-CTE, CASE, conditional aggregation |
| Q13 | Seller performance with revenue rank | Multi-CTE, RANK(), HAVING |
| Q14 | Orders above average payment | Correlated subquery in WHERE |
| Q15 | States worse than national avg delay | Subquery in HAVING |
| Q16 | Customer spend tier segmentation | CTE, CASE bucketing |
| Q17 | Review sentiment with delivery context | CASE, conditional SUM, percentage calc |
| Q18 | Hourly order distribution | strftime(), CAST, date extraction |
| Q19 | Quarter-over-quarter revenue | CTE, CASE for quarters, LAG() for QoQ growth |
| Q20 | Processing time by day of week | julianday() arithmetic, CASE for ordering |
| Q21 | Repeat vs one-time buyers | CTE, CASE, percentage of total |
| Q22 | Freight cost as % of price by category | HAVING, calculated percentages |
| Q23 | Payment installments vs spend | JOIN, GROUP BY, range filter |
| Q24 | Cross-state shipping analysis | 4-table JOIN, CASE, same vs cross state |
| Q25 | Product weight impact on delivery | CASE bucketing, multi-metric aggregation |

### SQL Skills Covered

| Skill | Queries |
|---|---|
| Basic Aggregations (COUNT, SUM, AVG, ROUND) | Q1-Q4 |
| Multi-table JOINs (up to 5 tables) | Q5, Q6, Q24 |
| Window Functions (RANK, ROW_NUMBER, LAG, Running SUM) | Q7-Q10 |
| Common Table Expressions (CTEs) | Q11-Q13 |
| Subqueries (scalar, correlated, in HAVING) | Q14, Q15 |
| CASE Statements (bucketing, conditional logic) | Q16, Q17, Q25 |
| Date Functions (strftime, julianday) | Q18-Q20 |
| PARTITION BY | Q9 |
| Business Analysis (RFM, Pareto, cohort, churn) | Q11, Q21-Q24 |

---

## Data Cleaning & Preprocessing

**File:** `clean_data.py`

### Operations Performed

| Table | Operation | Details |
|---|---|---|
| **Orders** | Date conversion | 5 date columns converted from string to `datetime` |
| **Orders** | Null handling | `order_approved_at` filled with purchase date; delivery dates filled with "Not Delivered"; delay days filled with 0 |
| **Products** | Category translation | Merged `product_category_name_translation.csv` — Portuguese to English |
| **Products** | Null handling | 610 missing categories filled with "other"; dimensions filled with median values |
| **Reviews** | Null handling | 87,656 empty titles and 58,247 empty messages filled with empty string |
| **Reviews** | Date conversion | `review_creation_date` and `review_answer_timestamp` converted to `datetime` |
| **Customers** | City standardization | Stripped whitespace, converted to Title Case |
| **Sellers** | City standardization | Stripped whitespace, converted to Title Case |
| **Geolocation** | Deduplication | 1,000,163 rows reduced to 19,015 (one entry per zip code) |
| **Order Items** | Date conversion | `shipping_limit_date` converted to `datetime` |
| **Payments** | Aggregation | 103,886 rows grouped to 99,440 (one row per order) with SUM of payment value, MAX installments, FIRST payment type |

### Output Files (11 cleaned CSVs — all 0 nulls)

| File | Rows | Size | Purpose |
|---|---|---|---|
| `master_orders.csv` | 114,092 | 47.9 MB | Main table — 6-way merge for Dashboards 1, 4, 5 |
| `churn_customers.csv` | 93,358 | 7.5 MB | Churn analysis — Dashboard 2 |
| `rfm_customers.csv` | 93,358 | 5.7 MB | RFM segmentation — Dashboard 3 |
| `orders_cleaned.csv` | 99,441 | 19.0 MB | Standalone cleaned orders |
| `products_cleaned.csv` | 32,951 | 3.1 MB | Standalone cleaned products |
| `reviews_cleaned.csv` | 99,224 | 13.4 MB | Standalone cleaned reviews |
| `customers_cleaned.csv` | 99,441 | 8.3 MB | Standalone cleaned customers |
| `sellers_cleaned.csv` | 3,095 | 0.2 MB | Standalone cleaned sellers |
| `geolocation_cleaned.csv` | 19,015 | 1.1 MB | Deduplicated geolocation |
| `items_cleaned.csv` | 112,650 | 15.3 MB | Standalone cleaned order items |
| `payments_cleaned.csv` | 99,440 | 5.1 MB | Aggregated payments per order |

---

## Feature Engineering

### Master Orders Table
A single denormalized table created by merging 6 datasets:
```
Orders + Customers + Order Items + Products + Payments + Reviews
→ 114,092 rows × 32 columns
```

### New Columns Created

| Column | Formula | Purpose |
|---|---|---|
| `order_year` | Extracted from purchase timestamp | Year-level filtering |
| `order_month` | Extracted as period (YYYY-MM) | Monthly trend analysis |
| `order_day_of_week` | Day name from purchase date | Weekday vs weekend analysis |
| `delivery_delay_days` | Actual delivery date - Estimated delivery date | Delivery performance |
| `actual_delivery_days` | Delivered date - Purchase date | Total delivery time |
| `is_late` | 1 if `delivery_delay_days > 0`, else 0 | Late delivery flag |
| `total_price` | `price + freight_value` | Total item cost |

### RFM Customer Segmentation
Calculated for 93,358 unique customers (delivered orders only):

| Metric | Calculation |
|---|---|
| **Recency** | Days since last purchase (from snapshot date) |
| **Frequency** | Number of unique orders |
| **Monetary** | Total spend (price + freight) |

Scores assigned using quintile-based binning (`pd.qcut`, 1-5 scale), then summed into an `rfm_score`. Segments assigned as:

| Segment | RFM Score | Count |
|---|---|---|
| Champion | 12-15 | 15,485 |
| Loyal | 9-11 | 38,018 |
| At Risk | 6-8 | 31,996 |
| Lost | 3-5 | 7,859 |

### Churn Classification
- **Definition:** Customer with no orders in the last 90 days = Churned
- **Churn Rate:** 90.1% (expected — most Olist customers are one-time buyers on a marketplace)

---

## Power BI Dashboards

**File:** `Olist_PBI.pbix`

**Theme:** Dark Professional (Background: `#1B1F3B`, Cards: `#252A4A`)

### Dashboard 1: Sales Performance
**Data Source:** `master_orders.csv`

| Visual | Type |
|---|---|
| Total Revenue | KPI Card |
| Total Orders | KPI Card |
| Avg Order Value | KPI Card |
| Total Customers | KPI Card |
| Monthly Revenue Trend | Line Chart |
| Top 10 Categories by Revenue | Bar Chart |
| City Wise Sales | Map |
| Payment Type Split | Donut Chart |
| Orders by Day of Week | Column Chart |
| State Wise Revenue | Bar Chart |
| Slicers | Year, Month, Category, State |

### Dashboard 2: Customer Churn Analysis
**Data Source:** `churn_customers.csv`

| Visual | Type |
|---|---|
| Total Customers | KPI Card |
| Churned Customers | KPI Card (DAX Measure) |
| Active Customers | KPI Card (DAX Measure) |
| Churn Rate % | KPI Card (DAX Measure) |
| Active vs Churned | Donut Chart |
| State Wise Churn | Bar Chart |
| Top 10 Churned Cities | Bar Chart |
| Days Since Last Order Distribution | Column Chart (Bins = 30) |
| Total Orders by Churn Status | Clustered Bar |
| Slicers | Churn Status, State |

**Key DAX Measures:**
```dax
Active Customers = CALCULATE(COUNT(churn_customers[customer_unique_id]), churn_customers[is_churned] = 0)
Churned Customers = CALCULATE(COUNT(churn_customers[customer_unique_id]), churn_customers[is_churned] = 1)
Churn Rate % = DIVIDE([Churned Customers], COUNT(churn_customers[customer_unique_id])) * 100
```

### Dashboard 3: RFM Customer Segmentation
**Data Source:** `rfm_customers.csv`

| Visual | Type |
|---|---|
| Total Customers | KPI Card |
| Champions / Loyal / At Risk / Lost Count | KPI Cards (DAX Measures) |
| Segment Distribution | Donut Chart |
| Avg Revenue per Segment | Bar Chart |
| Avg Recency per Segment | Bar Chart |
| RFM Scatter Plot | Scatter (X: Recency, Y: Monetary, Size: Frequency) |
| Score Distribution | Stacked Bar |
| Slicers | Segment, R/F/M Scores |

**Segment Colors:** Champion `#00B894`, Loyal `#4A90D9`, At Risk `#FF8C42`, Lost `#FF4C4C`

### Dashboard 4: Delivery Performance
**Data Source:** `master_orders.csv`

| Visual | Type |
|---|---|
| Total Delivered | KPI Card (DAX Measure) |
| On Time % | KPI Card (DAX Measure) |
| Late Deliveries | KPI Card (DAX Measure) |
| Avg Delay Days | KPI Card (DAX Measure) |
| On Time vs Late | Donut Chart |
| Monthly On Time Trend | Line Chart |
| State Wise Avg Delay | Bar Chart |
| Top 10 Late Cities | Bar Chart |
| Delay vs Review Score | Scatter Chart |
| Delivery Days Distribution | Column Chart (Bins = 5) |
| Slicers | Year, Month, State, Delivery Status |

**Key DAX Measures:**
```dax
Total Delivered = CALCULATE(COUNT(master_orders[order_id]), master_orders[order_status] = "delivered")
On Time % = DIVIDE([On Time Deliveries], [Total Delivered]) * 100
Delivery Status = IF(master_orders[is_late] = 1, "Late", "On Time")
```

### Dashboard 5: Customer Sentiment & Reviews
**Data Source:** `master_orders.csv`

| Visual | Type |
|---|---|
| Avg Review Score | KPI Card (DAX Measure) |
| 5 Star Reviews | KPI Card (DAX Measure) |
| 1 Star Reviews | KPI Card (DAX Measure) |
| Total Reviews | KPI Card |
| Score Distribution | Column Chart |
| Category Wise Avg Rating (Top 10) | Bar Chart |
| Rating vs Delivery Delay | Scatter Chart |
| Monthly Avg Rating Trend | Line Chart |
| Low Rating + Late Delivery Count | KPI Card (DAX Measure) |
| Slicers | Review Score, Category, Year |

**Key DAX Measure:**
```dax
Low Rating Late Delivery = CALCULATE(COUNT(master_orders[order_id]), master_orders[review_score] <= 2, master_orders[is_late] = 1)
```

---

## Key Business Insights

### Sales
1. **Revenue is growing** — consistent upward trend from 2017 to mid-2018 with a clear Black Friday spike in November 2017.
2. **Sao Paulo is the revenue engine** — SP state accounts for ~42% of all customers and the highest revenue contribution.
3. **Credit card dominates payments** — 74% of transactions use credit cards; Boleto (Brazilian bank slip) is second at 19%.
4. **Weekdays drive orders** — Monday and Tuesday are peak ordering days; Sunday sees the lowest volume.

### Customer Behavior
5. **90.1% churn rate** — the vast majority of Olist customers are one-time buyers, which is typical for marketplace platforms. Retention strategies (loyalty programs, personalized follow-ups) could significantly improve this.
6. **RFM segmentation reveals opportunity** — 38,018 Loyal customers (40.7%) are the largest segment and prime targets for upselling. 31,996 At Risk customers (34.3%) need re-engagement campaigns before they become Lost.
7. **Champions are a small but high-value group** — only 16.6% of customers but they represent the highest monetary value per customer.

### Delivery & Logistics
8. **Late delivery is the #1 driver of bad reviews** — this is the strongest correlation in the entire dataset. 1-star reviews average 20+ delivery days vs ~10 days for 5-star reviews.
9. **Delivery delays directly destroy customer satisfaction** — customers who receive their orders after the estimated delivery date are significantly more likely to leave 1-star or 2-star reviews.

### Customer Sentiment
10. **Review scores skew positive** — 57.8% of reviews are 5-star, but the 11.5% of 1-star reviews correlate strongly with delivery issues.
11. **Higher-spending customers who receive late deliveries leave the worst reviews** — they expected a premium experience for the price they paid.
12. **Fixing delivery performance would improve review scores** — this is the single highest-leverage improvement Olist could make.

### Actionable Recommendations
- **Invest in logistics for non-SP states** — delivery delays are higher in Northern and Northeastern Brazil.
- **Implement proactive delivery notifications** — alert customers before an order becomes late to manage expectations.
- **Launch a retention program** — even converting 5% of At Risk customers to Loyal would significantly boost lifetime value.
- **Prioritize high-value orders for on-time delivery** — high spenders who get late deliveries become the most vocal detractors.

---

## Tech Stack

| Tool | Usage |
|---|---|
| **Python 3.13** | Data cleaning, preprocessing, feature engineering |
| **Pandas** | Data manipulation, merging, aggregation |
| **NumPy** | Numerical computations |
| **Matplotlib** | Static visualizations in EDA |
| **Seaborn** | Statistical visualizations in EDA |
| **SQLite** | SQL analysis on in-memory database |
| **Jupyter Notebook** | Interactive EDA & SQL environment |
| **Power BI Desktop** | Interactive dashboard creation |
| **DAX** | Calculated measures in Power BI |

---

## Project Structure

```
DA_OLIST/
├── README.md                              # This file
├── eda.ipynb                              # Exploratory Data Analysis notebook
├── sql_analysis.ipynb                     # SQL Analysis (25 queries on SQLite)
├── clean_data.py                          # Data cleaning & feature engineering script
├── Olist_PBI.pbix                         # Power BI dashboard file
│
├── olist_orders_dataset.csv               # Raw data (9 files)
├── olist_customers_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_sellers_dataset.csv
├── olist_geolocation_dataset.csv
├── product_category_name_translation.csv
│
└── cleaned/                               # Cleaned output files (11 files)
    ├── master_orders.csv
    ├── churn_customers.csv
    ├── rfm_customers.csv
    ├── orders_cleaned.csv
    ├── products_cleaned.csv
    ├── reviews_cleaned.csv
    ├── customers_cleaned.csv
    ├── sellers_cleaned.csv
    ├── geolocation_cleaned.csv
    ├── items_cleaned.csv
    └── payments_cleaned.csv
```

---

## How to Run

### Prerequisites
- Python 3.10+
- Power BI Desktop (Windows)

### Step 1: Install Python Dependencies
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### Step 2: Run EDA Notebook
```bash
jupyter notebook eda.ipynb
```
Or open `eda.ipynb` in VS Code with the Jupyter extension and click **Run All**.

### Step 3: Run Data Cleaning Script
```bash
python clean_data.py
```
This generates 11 cleaned CSV files in the `cleaned/` folder.

### Step 4: Open Power BI Dashboard
Open `Olist_PBI.pbix` in Power BI Desktop. The dashboard connects to the cleaned CSV files in the `cleaned/` folder.

---

**Author:** Deep Naidu
