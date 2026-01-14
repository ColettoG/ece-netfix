import duckdb
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

titles_csv = BASE / "data_lake" / "curated" / "titles_clean.csv"
country_csv = BASE / "data_lake" / "curated" / "country_summary.csv"

db_path = BASE / "warehouse" / "netflix.duckdb"
db_path.parent.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(db_path))

con.execute(
    "CREATE OR REPLACE TABLE titles_clean AS SELECT * FROM read_csv_auto(?)",
    [str(titles_csv)],
)

con.execute(
    "CREATE OR REPLACE TABLE country_summary AS SELECT * FROM read_csv_auto(?)",
    [str(country_csv)],
)

print("Warehouse created:", db_path)

con.close()
