# Dependencies
import pandas as pd
from flask import Flask, jsonify, request

from api.docker.cb_filtering import cb_filter

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


if __name__ == '__main__':
    df_rating = pd.read_csv('./data/ratings_small.csv')
    df_movie = pd.read_csv('./data/movies_metadata.csv')

    # content-based filtering
    links_small = pd.read_csv('./data/links_small.csv')
    credits = pd.read_csv('./data/credits.csv')
    keywords = pd.read_csv('./data/keywords.csv')
    smd, cosine_sim = cb_filter(df_movie, links_small, credits, keywords)
    smd = smd.reset_index()
    titles = smd['title']
    indices = pd.Series(smd.index, index=smd['title'])

    app.run(debug=True, host='0.0.0.0')
