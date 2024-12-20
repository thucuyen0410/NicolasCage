import pandas as pd
import nltk
nltk.download('stopwords')
from nltk import FreqDist, pos_tag
from nltk.corpus import stopwords

#Import data
df = pd.read_csv('imdb-movies-dataset.csv')
df = df[df['Cast'].str.contains('Nicolas Cage', na=False)]

#Basic metrics
no_of_movies = len(df)
total_mins = df['Duration (min)'].sum()
df_sorted = df.dropna(how='any', axis=0).sort_values(by='Year', ascending=True)
first_movie = df_sorted['Title'].iloc[0]
first_year = df_sorted['Year'].iloc[0].astype(int)
last_movie = df_sorted['Title'].iloc[-1]
last_year = df_sorted['Year'].iloc[-1].astype(int)
highest_metascore_movie = df.loc[df['Rating'].idxmax(), 'Title']
highest_rating_movie = df.loc[df['Metascore'].idxmax(), 'Title']

#Process genre
split_genre = df['Genre'].str.split(',', expand=True)
split_genre.columns = ['Genre1','Genre2','Genre3']
split_genre = split_genre.apply(lambda col: col.str.strip() if col.dtypes == 'object' else col)

#Analyze performance of genres
genredf = df[['Year','Rating','Metascore']]
genredf = genredf.join(split_genre)
genredf_melted = pd.melt(genredf, id_vars=['Year','Rating', 'Metascore'],
                    value_vars=['Genre1', 'Genre2','Genre3'], 
                    var_name='attribute', value_name='Genre')
genredf_melted = genredf_melted.drop(columns=['attribute'])
genre_group = genredf_melted.groupby('Genre').agg(
    Count=('Genre', 'size'),               # Count of each genre
    Rating=('Rating', 'mean'),         # Average Rating per genre
    Metascore=('Metascore', 'mean')    # Average Metascore per genre
    ).reset_index()

#Create bins for time analysis
min_year = int(min(df['Year']))
max_year = int(max(df['Year']))
bins = list(range(min_year - (min_year % 5), max_year + 1, 5))
labels = [f"{x}-{x+4}" for x in bins[:-1]]

#Analyze metascore overtime
metascoredf = df[['Year', 'Metascore']]
metascoredf.dropna(how='any', axis=0, inplace=True)
metascoredf['Period'] = pd.cut(metascoredf['Year'], bins=bins, labels=labels, right=False)
metascore_group = metascoredf.groupby('Period')['Metascore'].mean().reset_index()

#Analyze genre overtime
genre_year = genredf_melted[['Year', 'Genre']]
genre_year['Period'] = pd.cut(genre_year['Year'], bins=bins, labels=labels, right=False)
genre_year_group = genre_year.groupby(['Period', 'Genre']).size().reset_index(name='Count')
max_count_per_period = genre_year_group.groupby('Period')['Count'].transform('max')
max_genres = genre_year_group[genre_year_group['Count'] == max_count_per_period]
max_genres_combined = max_genres.groupby('Period')['Genre'].apply(', '.join).reset_index()

#Combine metascore and genre
year_metascore_genre = pd.merge(metascore_group, max_genres_combined, on='Period', how='left')
year_metascore_genre['Genre'] = year_metascore_genre.apply(lambda row: None if pd.isnull(row['Metascore']) else row['Genre'], axis=1)

#Analyze director performance
directordf = df[['Director', 'Genre', 'Rating', 'Metascore']]
directordf = directordf[directordf['Genre'].str.contains('Comedy|Drama|Romance', na=False)]
directordf = directordf.drop(columns=['Genre'])
director_group = directordf.groupby('Director').mean()

#Analyze movie's descriptions and reviews
stopwords = stopwords.words('english') #use the NLTK stopwords
adtl = ["nicolas", "cage", "movie", "film", 'would', 'could', 'character','great','good','many','much','best','first','little','excellent']
stopwords = stopwords + adtl

descrevdf = df[['Genre','Description','Review']]
descrevdf = descrevdf.drop(columns=['Genre']).join(split_genre)
descrevdf_melted = pd.melt(descrevdf, id_vars=['Description','Review',], value_vars=['Genre1', 'Genre2','Genre3'], 
                    var_name='attribute', value_name='Genre')
descrevdf_melted = descrevdf_melted.drop(columns=['attribute'])

#Drama movie description analysis
dramadf = descrevdf_melted.loc[descrevdf_melted['Genre'] == 'Drama']
dramadesc = ""
for i in range(len(dramadf)):
    dramadesc = dramadesc + " " + dramadf['Description'].iloc[i]
dramadesc = dramadesc.replace('\n', '')

nltk.sent_tokenize(dramadesc)
dramadesc_tokens = nltk.word_tokenize(dramadesc)
dramadesc_words1 = [w.lower() for w in dramadesc_tokens]
dramadesc_words2 = [w for w in dramadesc_words1 if w.isalpha()]
dramadesc_nostopwords = [w for w in dramadesc_words2 if w not in stopwords]
dramadesc_tagged_tokens = pos_tag(dramadesc_nostopwords)
drama_noun = [word for word, tag in dramadesc_tagged_tokens if tag in ['NN', 'NNS', 'NNP', 'NNPS']]
dramadesc_freq = FreqDist(drama_noun)


#Drama movie review analysis
dramarev = ""
for i in range(len(dramadf)):
    dramarev = dramarev + " " + dramadf['Review'].iloc[i]
dramarev = dramarev.replace('\n', '')

nltk.sent_tokenize(dramarev)
dramarev_tokens = nltk.word_tokenize(dramarev)
dramarev_words1 = [w.lower() for w in dramarev_tokens] 
dramarev_words2 = [w for w in dramarev_words1 if w.isalpha()]
dramarev_nostopwords = [w for w in dramarev_words2 if w not in stopwords]
dramarev_tagged_tokens = pos_tag(dramarev_nostopwords)
drama_adj = [word for word, tag in dramarev_tagged_tokens if tag in ['JJ', 'JJR', 'JJS']]
dramarev_freq = FreqDist(drama_adj)


#Comedy movie description analysis
comedydf = descrevdf_melted.loc[descrevdf_melted['Genre'] == 'Comedy']
comedydesc = ""
for i in range(len(comedydf)):
    comedydesc = comedydesc + " " + comedydf['Description'].iloc[i]

nltk.sent_tokenize(comedydesc)
comedydesc_tokens = nltk.word_tokenize(comedydesc)
comedydesc_words1 = [w.lower() for w in comedydesc_tokens]
comedydesc_words2 = [w for w in comedydesc_words1 if w.isalpha()]
comedydesc_nostopwords = [w for w in comedydesc_words2 if w not in stopwords]
comedydesc_tagged_tokens = pos_tag(comedydesc_nostopwords)
comedy_noun = [word for word, tag in comedydesc_tagged_tokens if tag in ['NN', 'NNS', 'NNP', 'NNPS']]
comedydesc_freq = FreqDist(comedy_noun)

#Comedy movie review analysis
comedyrev = ""
for i in range(len(comedydf)):
    comedyrev = comedyrev + " " + comedydf['Review'].iloc[i]
nltk.sent_tokenize(comedyrev)
comedyrev_tokens = nltk.word_tokenize(comedyrev)
comedyrev_words1 = [w.lower() for w in comedyrev_tokens]
comedyrev_words2 = [w for w in comedyrev_words1 if w.isalpha()]
comedyrev_nostopwords = [w for w in comedyrev_words2 if w not in stopwords]
comedyrev_tagged_tokens = pos_tag(comedyrev_nostopwords)
comedy_adj = [word for word, tag in comedyrev_tagged_tokens if tag in ['JJ', 'JJR', 'JJS']]
comedyrev_freq = FreqDist(comedy_adj)