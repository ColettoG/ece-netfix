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

### Script 03 — “Curated BI” (as provided)

In the code you pasted, the “curated BI” script is functionally identical to Script 02: it reads the raw CSV, performs the same missing-value fill, keeps the same subset of columns, and writes the same staging output file (`data_lake/staging/netflix_titles_staging.csv`). As written, it does not create a curated layer or BI-oriented aggregates, and it overwrites/updates the staging file instead.

If the intended design is a curated BI step, the typical behavior would be to read from the staging file, enforce types and key-field validity, and output curated tables and summary aggregations (e.g., cleaned titles plus country/rating/year summaries). In that case, the report section should match the actual `03_curated_bi.py` that exists in the repository.
