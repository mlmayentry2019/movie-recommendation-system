# Dependencies
import joblib
import pandas as pd
import os
cwd = os.getcwd()
print(cwd)

from cb_filtering import cb_filter
from collaborative_filtering import collab_filter

print('Loading ratings_small..')

df_rating = pd.read_csv('./data/ratings_small.csv')
print('Loading movies_metadata..')
df_movie = pd.read_csv('./data/movies_metadata.csv')

# content-based filtering
print('Loading links_small..')
links_small = pd.read_csv('./data/links_small.csv')
print('Loading credits..')
credits = pd.read_csv('./data/credits.csv')
print('Loading keywords..')
keywords = pd.read_csv('./data/keywords.csv')

smd, cosine_sim = cb_filter(df_movie, links_small, credits, keywords)
joblib.dump(smd, 'smd.pkl')
joblib.dump(cosine_sim, 'cosine_sim.pkl')

svd, id_map = collab_filter(df_movie, df_rating, links_small, credits, keywords, smd)
joblib.dump(svd, 'svd.pkl')
joblib.dump(id_map, 'id_map.pkl')
