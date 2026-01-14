# ece-netfix
Data Integration - ECE - Netflix Data project

# group:
Gabriel Coletto

Henrique Cox

Linus Remenyi

### Script 01 — `01_explore_raw.py` (Exploration of the raw dataset)

This script reads the raw Netflix titles CSV from `data_lake/raw/netflix_titles.csv` and performs a lightweight exploratory analysis. It prints basic diagnostics to the console (first rows, dataset shape, and `df.info()`), then computes missing-value ratios per column and reports only columns with non-zero missingness. If the `date_added` column exists, it is parsed to datetime and a derived `year_added` column is created. The script also checks whether `show_id` contains duplicates and prints the number of duplicated rows.

The main outputs are exploratory figures saved to the `outputs/` directory (created automatically if missing). These include distributions of titles by `type`, titles added per year (`year_added`), the top 10 producing countries (after splitting multi-country entries), the most common ratings, duration distributions (movie minutes vs. TV seasons parsed from the `duration` field), and the top genres (from the comma-separated `listed_in` field). The script therefore produces no transformed dataset, but generates plots and console summaries that guide subsequent cleaning decisions.

---

### Script 02 — `02_clean_staging.py` (Staging table creation)

This script reads the same raw CSV from `data_lake/raw/netflix_titles.csv` and produces a simplified staging dataset intended for downstream processing. It replaces missing values in `director`, `cast`, and `country` with `"Unknown"` when these columns exist, then reduces the table to a fixed subset of fields: `show_id`, `type`, `title`, `country`, `release_year`, `rating`, `duration`, `listed_in`, and `date_added`. The result is written to `data_lake/staging/netflix_titles_staging.csv`.

One practical detail is that the script assumes the `data_lake/staging/` directory already exists; otherwise the CSV write will fail. Apart from that, it is a straightforward “raw → staging” transformation that standardizes a subset of the schema and preserves one row per title.

---

### Script 03 — `03_curated_bi.py` (Curated layer + BI summary)

This script builds the curated (“analysis-ready”) outputs from the staging dataset. It reads `data_lake/staging/netflix_titles_staging.csv` and applies a small set of data-quality rules to stabilize key fields. Rows with missing titles are removed. The `release_year` column is coerced to numeric; rows where this conversion fails are dropped, and the remaining values are cast to integers to enforce a consistent type. Missing ratings are replaced with `"Unknown"` to avoid null categories downstream.

The script produces two curated outputs under `data_lake/curated/`. First, it writes the cleaned title-level table to `data_lake/curated/titles_clean.csv`, preserving the staging schema but with validated `title`, normalized `release_year`, and non-null `rating`. Second, it generates a BI-friendly aggregation by country: it groups by `country`, counts titles via `show_id`, sorts descending by count, and saves the result as `data_lake/curated/country_summary.csv`. The script ends by printing a confirmation message (`CURATED data ready`).

### Script 04 — `04_warehouse_duckdb.py` (Create DuckDB warehouse)

This script creates a local DuckDB “data warehouse” file at `warehouse/netflix.duckdb`. It first ensures the `warehouse/` directory exists, then opens (or creates) the database file. After that, it loads the curated CSV files from `data_lake/curated/` into two SQL tables inside DuckDB: `titles_clean` (from `titles_clean.csv`) and `country_summary` (from `country_summary.csv`). Both tables are created with `CREATE OR REPLACE`, so rerunning the script refreshes the warehouse tables from the latest curated CSVs. At the end, it prints a confirmation message showing the database path.

---

### Script 05 — `05_check_warehouse.py` (Verify warehouse content)

This script verifies that the DuckDB warehouse exists and contains data. It connects to `warehouse/netflix.duckdb`, prints the list of available tables via `SHOW TABLES`, and then runs `SELECT COUNT(*)` on both `titles_clean` and `country_summary`. The expected checkpoint is that the table names are printed and both row counts are greater than zero. It closes the database connection after printing the results.

---

### Script 06 — `06_bi_queries_duckdb.py` (BI queries inside DuckDB)

This script runs a small set of BI-oriented SQL queries directly against the DuckDB warehouse and prints the results in tabular form. It connects to `warehouse/netflix.duckdb` and executes four queries: (1) counts of titles by `type` to compare Movies vs TV Shows, (2) the top 10 countries from `country_summary` ordered by `title_count`, (3) the top 10 release years by number of titles from `titles_clean`, and (4) the single most common content rating from `titles_clean`. The results are printed to the terminal as pandas DataFrames, making them easy to copy into the report.

---

### Script 07 — `07_export_results.py` (Export BI query results to CSV)

This script exports the BI query results from DuckDB into CSV files for reporting. It ensures the `outputs/` directory exists, connects to `warehouse/netflix.duckdb`, and uses DuckDB’s `COPY (...) TO` statement to write four query results to disk: `movies_vs_tv.csv`, `top10_countries.csv`, `top10_years.csv`, and `most_common_rating.csv`. Each export includes a header row and uses comma delimiters. The script finishes by printing the output directory path where the files were saved.
