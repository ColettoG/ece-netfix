import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

base_dir = Path(__file__).resolve().parent
raw_path = base_dir / ".." / "data_lake" / "raw" / "netflix_titles.csv"
out_dir = base_dir / ".." / "outputs"
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(raw_path)

print("Head:\n", df.head())
print("Shape:", df.shape)
print("\nInfo:")
df.info()

missing = df.isna().mean().sort_values(ascending=False)
missing = missing[missing > 0]
print("\nMissing ratio:\n", missing)

# Date added
if "date_added" in df.columns:
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year

# Duplicates check
if "show_id" in df.columns:
    dupes = df[df["show_id"].duplicated(keep=False)].sort_values("show_id")
    print("\nDuplicated show_id rows:", len(dupes))

# Titles by type + titles added per year
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
if "type" in df.columns:
    sns.countplot(x="type", data=df, ax=ax[0])
    ax[0].set_title("Titles by Type")
if "year_added" in df.columns:
    sns.histplot(df["year_added"].dropna(), bins=20, ax=ax[1])
    ax[1].set_title("Titles Added per Year")
plt.tight_layout()
fig.savefig(out_dir / "explore_type_year.png", dpi=150)
plt.close(fig)

# Top countries
if "country" in df.columns:
    country_counts = (
        df["country"]
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(y=country_counts.index, x=country_counts.values, ax=ax)
    ax.set_title("Top 10 Countries")
    ax.set_xlabel("Count")
    ax.set_ylabel("Country")
    plt.tight_layout()
    fig.savefig(out_dir / "explore_top_countries.png", dpi=150)
    plt.close(fig)

# Top ratings
if "rating" in df.columns:
    rating_counts = df["rating"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(y=rating_counts.index, x=rating_counts.values, ax=ax)
    ax.set_title("Top Ratings")
    ax.set_xlabel("Count")
    ax.set_ylabel("Rating")
    plt.tight_layout()
    fig.savefig(out_dir / "explore_top_ratings.png", dpi=150)
    plt.close(fig)

# Duration distributions

def parse_duration(s):
    if pd.isna(s):
        return np.nan, np.nan
    parts = s.split(" ")
    if len(parts) < 2:
        return np.nan, np.nan
    value = pd.to_numeric(parts[0], errors="coerce")
    unit = parts[1].lower()
    if unit.startswith("season"):
        unit = "season"
    elif unit.startswith("min"):
        unit = "min"
    return value, unit

if "duration" in df.columns:
    duration = df["duration"].apply(parse_duration)
    df["duration_value"] = duration.apply(lambda x: x[0])
    df["duration_unit"] = duration.apply(lambda x: x[1])

    movies = df[df["duration_unit"] == "min"]
    tv = df[df["duration_unit"] == "season"]

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(movies["duration_value"].dropna(), bins=30, ax=ax[0])
    sns.histplot(tv["duration_value"].dropna(), bins=20, ax=ax[1])

    ax[0].set_title("Movie Duration (minutes)")
    ax[1].set_title("TV Seasons")
    plt.tight_layout()
    fig.savefig(out_dir / "explore_duration.png", dpi=150)
    plt.close(fig)

# Top genres
if "listed_in" in df.columns:
    genres = df["listed_in"].dropna().str.split(", ").explode()
    genre_counts = genres.value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(y=genre_counts.index, x=genre_counts.values, ax=ax)
    ax.set_title("Top Genres")
    ax.set_xlabel("Count")
    ax.set_ylabel("Genre")
    plt.tight_layout()
    fig.savefig(out_dir / "explore_top_genres.png", dpi=150)
    plt.close(fig)

print("Explore outputs saved to", out_dir)
