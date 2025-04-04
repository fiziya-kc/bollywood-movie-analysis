#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd 
file_path = "BollywoodMovieDetail.csv"
df = pd.read_csv(file_path)


# Step 1: Handle Missing Values
df.fillna({
    'releaseDate': 'Unknown',
    'genre': 'Unknown',
    'writers': 'Unknown',
    'actors': 'Unknown',
    'directors': 'Unknown',
    'sequel': 0  # Assuming 0 means "not a sequel"
}, inplace=True)

# Step 2: Convert releaseDate to datetime (if not "Unknown")
df['releaseDate'] = pd.to_datetime(df['releaseDate'], errors='coerce')

# Step 3: Convert sequel column to integer
df['sequel'] = df['sequel'].astype(int)

# Step 4: Remove duplicates based on title and releaseYear
df.drop_duplicates(subset=['title', 'releaseYear'], keep='first', inplace=True)

# Step 5: Normalize text data (convert "|" separated values into lists)
df['writers'] = df['writers'].apply(lambda x: x.split(' | ') if x != 'Unknown' else [])
df['actors'] = df['actors'].apply(lambda x: x.split(' | ') if x != 'Unknown' else [])
df['directors'] = df['directors'].apply(lambda x: x.split(' | ') if x != 'Unknown' else [])

# Show cleaned dataset summary
df.info(), df.head()


# In[6]:


# Step 1: Standardize Genre Format (lowercase for consistency)
df['genre'] = df['genre'].str.lower().str.strip()

# Step 2: Extract Year from releaseDate (if valid)
df['extractedYear'] = df['releaseDate'].dt.year

# Step 3: Analyze Outliers in 'hitFlop' & 'sequel' (check value counts)
hitflop_counts = df['hitFlop'].value_counts()
sequel_counts = df['sequel'].value_counts()

# Step 4: Map 'hitFlop' categories to readable labels
hitflop_mapping = {
    1: "Flop", 2: "Average", 3: "Semi-Hit", 4: "Hit", 5: "Super-Hit", 6: "Blockbuster"
}
df['hitFlop'] = df['hitFlop'].map(hitflop_mapping)

# Step 5: Count Most Frequent Actors & Directors
from collections import Counter

# Flatten lists of actors & directors
all_actors = [actor for sublist in df['actors'] for actor in sublist]
all_directors = [director for sublist in df['directors'] for director in sublist]

# Count occurrences
top_actors = Counter(all_actors).most_common(10)
top_directors = Counter(all_directors).most_common(10)

# Step 6: Count Most Popular Genres
top_genres = df['genre'].value_counts().head(10)

# Step 7: Count Movies Released Per Year
movies_per_year = df['extractedYear'].value_counts().sort_index()

# Return analysis results
hitflop_counts, sequel_counts, top_actors, top_directors, top_genres, movies_per_year





