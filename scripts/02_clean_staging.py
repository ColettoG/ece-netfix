import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
raw_path = base_dir / ".." / "data_lake" / "raw" / "netflix_titles.csv"
stage_path = base_dir / ".." / "data_lake" / "staging" / "netflix_titles_staging.csv"

df = pd.read_csv(raw_path)

for col in ["director", "cast", "country"]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

keep = ['show_id','type','title','country','release_year','rating','duration','listed_in','date_added']
df = df[keep]

df.to_csv(stage_path, index=False)
print("Saved to STAGING:", stage_path)
