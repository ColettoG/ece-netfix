import duckdb
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
db_path = BASE / "warehouse" / "netflix.duckdb"

out_dir = BASE / "outputs"
out_dir.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(db_path))

con.execute(
    """
COPY (
  SELECT type, COUNT(*) AS total
  FROM titles_clean
  GROUP BY type
  ORDER BY total DESC
) TO ? (HEADER, DELIMITER ',');
""",
    [str(out_dir / "movies_vs_tv.csv")],
)

con.execute(
    """
COPY (
  SELECT country, title_count
  FROM country_summary
  ORDER BY title_count DESC
  LIMIT 10
) TO ? (HEADER, DELIMITER ',');
""",
    [str(out_dir / "top10_countries.csv")],
)

con.execute(
    """
COPY (
  SELECT release_year, COUNT(*) AS total
  FROM titles_clean
  GROUP BY release_year
  ORDER BY total DESC
  LIMIT 10
) TO ? (HEADER, DELIMITER ',');
""",
    [str(out_dir / "top10_years.csv")],
)

con.execute(
    """
COPY (
  SELECT rating, COUNT(*) AS total
  FROM titles_clean
  GROUP BY rating
  ORDER BY total DESC
  LIMIT 1
) TO ? (HEADER, DELIMITER ',');
""",
    [str(out_dir / "most_common_rating.csv")],
)

print("Exports saved to:", out_dir)

con.close()
