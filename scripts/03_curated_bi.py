import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
staging = base_dir / '..' / 'data_lake' / 'staging' / 'netflix_titles_staging.csv'
titles_out = base_dir / '..' / 'data_lake' / 'curated' / 'titles_clean.csv'
country_out = base_dir / '..' / 'data_lake' / 'curated' / 'country_summary.csv'

df = pd.read_csv(staging)
df = df[df['title'].notna()]

df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
df = df.dropna(subset=['release_year'])
df['release_year'] = df['release_year'].astype(int)

df['rating'] = df['rating'].fillna('Unknown')
df.to_csv(titles_out, index=False)

country = df.groupby('country')['show_id'].count().reset_index(name='title_count')
country = country.sort_values('title_count', ascending=False)
country.to_csv(country_out, index=False)

print('CURATED data ready')
