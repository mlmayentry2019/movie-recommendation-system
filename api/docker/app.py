# Dependencies
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from top_trend import top_movies

import sys
sys.path.append('/app')

# Your API definition
app = Flask(__name__)


@app.route('/top_trend', methods=['GET'])
def topTrend():
    return top_movies(df_movie).to_json()


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
    idx = indices[title]
    #tmdbId = id_map.loc[title]['id']
    indices_map = id_map.set_index('id')
    #movie_id = id_map.loc[title]['movieId']

    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'id']]
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending=False)
    #return movies.head(10)
    movie_titles = movies.head(10)['title']
    return movie_titles.to_json(orient="records")

if __name__ == '__main__':
    print('Loading ratings_small..')
    df_rating = pd.read_csv('./data/ratings_small.csv')
    print('Loading movies_metadata..')
    df_movie = pd.read_csv('./data/movies_metadata.csv')

    # content-based filtering
    # smd, cosine_sim = cb_filter(df_movie, links_small, credits, keywords)
    smd = joblib.load("./smd.pkl")
    cosine_sim = joblib.load("./cosine_sim.pkl")
    
    # svd, id_map = collab_filter(df_movie, df_rating, links_small, credits, keywords, smd)
    svd = joblib.load("./svd.pkl")
    id_map = joblib.load("./id_map.pkl")

    smd = smd.reset_index()
    titles = smd['title']
    indices = pd.Series(smd.index, index=smd['title'])

    #print(hybrid(1, 'Avatar'))
    app.run(debug=True, host='0.0.0.0')