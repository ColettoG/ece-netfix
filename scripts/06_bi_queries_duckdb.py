import duckdb
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
db_path = BASE / "warehouse" / "netflix.duckdb"

con = duckdb.connect(str(db_path))

print("\n1) Movies vs TV Shows")
print(
    con.execute(
        """
        SELECT type, COUNT(*) AS total
        FROM titles_clean
        GROUP BY type
        ORDER BY total DESC;
        """
    ).df()
)

print("\n2) Top 10 countries")
print(
    con.execute(
        """
        SELECT country, title_count
        FROM country_summary
        ORDER BY title_count DESC
        LIMIT 10;
        """
    ).df()
)

print("\n3) Top 10 release years")
print(
    con.execute(
        """
        SELECT release_year, COUNT(*) AS total
        FROM titles_clean
        GROUP BY release_year
        ORDER BY total DESC
        LIMIT 10;
        """
    ).df()
)

print("\n4) Most common rating")
print(
    con.execute(
        """
        SELECT rating, COUNT(*) AS total
        FROM titles_clean
        GROUP BY rating
        ORDER BY total DESC
        LIMIT 1;
        """
    ).df()
)

con.close()
