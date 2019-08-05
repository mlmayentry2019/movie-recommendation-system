# Dependencies
import pandas as pd
from flask import Flask, jsonify, request

import sys
sys.path.append('/app')

#if __name__ == "__main__" and __package__ is None:
#    __package__ = "app.movie"

from cb_filtering import cb_filter
from collaborative_filtering import collab_filter
# Your API definition
app = Flask(__name__)


@app.route('/top_trend', methods=['GET'])
def topTrend():
    top_rating = df_rating.nlargest(20, ['rating', 'timestamp'])
    top_rating_list = top_rating['movieId'].astype(str).tolist()

    df_movie['id'] = df_movie['id'].astype(str)
    top_trend_movies = df_movie[df_movie['id'].isin(top_rating_list)]
    return top_trend_movies.to_json()


@app.route('/content-based', methods=['POST'])
def get_recommendations():
    json_ = request.json
    print(json_)
    idx = indices[json_['title']]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    movie_titles = (titles.iloc[movie_indices]).head(10)
    return movie_titles.to_json(orient="records")

@app.route('/collaborative', methods=['POST'])
def hybrid():
    json_ = request.json
    print(json_)
    userId = json_['userId']
    title = json_['title']
    idx = indices_collab[title]
    #tmdbId = id_map.loc[title]['id']
    indices_map = id_map.set_index('id')
    #movie_id = id_map.loc[title]['movieId']
    
    sim_scores = list(enumerate(cosine_sim_collab[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    
    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending=False)
    #return movies.head(10)
    movie_titles = (movies.iloc[movie_indices]).head(10)
    return movie_titles.to_json(orient="records")

if __name__ == '__main__':
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
    smd = smd.reset_index()
    titles = smd['title']
    indices = pd.Series(smd.index, index=smd['title'])

    #svd, cosine_sim_collab, id_map, indices_collab = collab_filter(df_movie, df_rating, links_small, credits, keywords)

    #print(hybrid(1, 'Avatar'))
    app.run(debug=True, host='0.0.0.0')